"""Enumerate / count LinFeas(P) for case o (no sync points, observed reads allowed).

Method: depth-first search over interleavings of the thread chains. Along a prefix we
carry the exact set of reachable "configurations" of the atomic-register simulation:

    (mem, pending, env)

    mem      content of every block (None for a block no relevant read will ever see
             again, so that equivalent states compare equal)
    pending  actions that have started but have not yet taken effect
    env      values still needed later: read results referenced by writes that have
             not started yet, and contents of writes (pending, or referenced later)

A start adds the action to ``pending``. At the end of action ``a`` every config in which
``a`` is still pending is expanded by effecting any sequence of other pending actions
and then ``a``. This realises exactly the effect orders that are linear extensions of
the interval order of L, which are exactly the orders realisable by distinct effect
points inside the intervals. A prefix is extendable iff its config set is non-empty and
some completion keeps it non-empty; completions depend only on (chain positions,
config set), so dead subtrees are memoised by that key.

Reads that are unobserved and whose value no relevant write uses, and writes to blocks
no relevant read looks at, are ignored by the simulation.
"""

from __future__ import annotations

from math import comb
from typing import Iterator

from harness import terms as T
from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.registry import register

_DEAD_CAP = 1_500_000
_MEMO_CAP = 3_000_000


class _Engine:
    def __init__(self, setup) -> None:
        P = setup.poset
        chains = [list(c) for c in P.chains if len(c) > 0]
        self.chains = chains
        self.lens = [len(c) for c in chains]
        self.n_ch = len(chains)
        self.total = sum(self.lens)
        where: dict[int, tuple[int, int]] = {}
        for ci, c in enumerate(chains):
            for j, x in enumerate(c):
                where[x] = (ci, j)
        self.node_chain = {x: ci for x, (ci, _) in where.items()}

        acts = setup.actions
        reads = [a for a in acts.values() if a.kind == "read"]
        writes = [a for a in acts.values() if a.kind != "read"]
        observed_reads = {a.id for a in reads if a.observed is not None}

        # ---- relevance fixed point
        rel_blocks = {acts[r].block for r in observed_reads}
        while True:
            rel_writes = {a.id for a in writes if a.block in rel_blocks}
            valued: set[str] = set()
            todo = list(rel_writes)
            done_w: set[str] = set()
            while todo:
                w = todo.pop()
                if w in done_w:
                    continue
                done_w.add(w)
                d = acts[w].data
                if d is None:
                    continue
                for r in T.refs(d):
                    if r not in valued:
                        valued.add(r)
                        if acts[r].kind != "read":
                            todo.append(r)
            rel_reads = observed_reads | {r for r in valued if acts[r].kind == "read"}
            nb = rel_blocks | {acts[r].block for r in rel_reads}
            if nb == rel_blocks:
                break
            rel_blocks = nb

        tracked_ids = rel_reads | rel_writes
        slotted = valued | rel_writes  # everything whose value/content is stored in env
        self.trivial = not tracked_ids

        ids = [aid for aid in acts if aid in tracked_ids or aid in valued]
        idx = {aid: i for i, aid in enumerate(ids)}
        slotmap: dict[str, int] = {}
        for aid in ids:
            if aid in slotted:
                slotmap[aid] = len(slotmap)
        self.slotmap = slotmap
        self.n_slots = len(slotmap)

        n = len(ids)
        self.is_write = [False] * n
        self.block = [0] * n
        self.ci = [0] * n
        self.slot = [-1] * n
        self.obs = [None] * n
        self.lastref = [-1] * n
        self.data = [None] * n
        self.unk = [None] * n
        self.tracked = [False] * n
        self.drops: list[list[int]] = [[] for _ in range(n)]
        spos = [0] * n
        dpos = [0] * n
        for aid in ids:
            i = idx[aid]
            a = acts[aid]
            ci, sp = where[P.start_node[aid]]
            _, dp = where[P.done_node[aid]]
            spos[i], dpos[i] = sp, dp
            self.is_write[i] = a.kind != "read"
            self.block[i] = a.block
            self.ci[i] = ci
            self.slot[i] = slotmap.get(aid, -1)
            self.obs[i] = a.observed
            self.data[i] = a.data
            self.unk[i] = T.Unk(aid)
            self.tracked[i] = aid in tracked_ids
        # last slotted referrer of every valued action
        for aid in ids:
            i = idx[aid]
            if self.is_write[i] and aid in slotted and self.data[i] is not None:
                for r in T.refs(self.data[i]):
                    j = idx[r]
                    if spos[i] > self.lastref[j]:
                        self.lastref[j] = spos[i]
        for aid in ids:
            i = idx[aid]
            if self.is_write[i] and aid in slotted and self.data[i] is not None:
                for r in sorted(T.refs(self.data[i])):
                    j = idx[r]
                    if self.lastref[j] == spos[i]:
                        self.drops[i].append(j)

        # per block: for every chain, the position of the last relevant read's done node
        bl: dict[int, dict[int, int]] = {}
        for r in rel_reads:
            i = idx[r]
            d = bl.setdefault(self.block[i], {})
            c = self.ci[i]
            if dpos[i] > d.get(c, -1):
                d[c] = dpos[i]
        self.block_last = {b: sorted(d.items()) for b, d in bl.items()}

        ops: list = [None] * len(P)
        for aid in ids:
            i = idx[aid]
            s, d = P.start_node[aid], P.done_node[aid]
            if self.is_write[i]:
                ops[s] = (0, i)
                if self.tracked[i]:
                    ops[d] = (2, i)
            elif self.tracked[i]:
                ops[s] = (1, i)
                ops[d] = (2, i)
        self.ops = ops

        mem0 = tuple(setup.init[b] if b in self.block_last else None for b in range(setup.blocks))
        self.S0 = frozenset({(mem0, frozenset(), (None,) * self.n_slots)})

    # ------------------------------------------------------------------ transitions

    def step(self, S, node, vec):
        op = self.ops[node]
        if op is None:
            return S
        k, x = op
        if k == 0:
            return self._wstart(S, x)
        if k == 1:
            add = frozenset((x,))
            return frozenset((m, p | add, e) for (m, p, e) in S)
        return self._end(S, x, vec)

    def _wstart(self, S, x):
        data = self.data[x]
        s = self.slot[x]
        b = self.block[x]
        tracked = self.tracked[x]
        has_ref = self.lastref[x] >= 0
        drops = self.drops[x]
        slot = self.slot
        slotmap = self.slotmap
        add = frozenset((x,))
        out = set()
        for m, p, e in S:
            if data is None:
                content = self.unk[x]
            else:
                content = T.substitute(data, lambda r, e=e: e[slotmap[r]])
            pend = tracked and m[b] is not None
            el = list(e)
            if pend or has_ref:
                el[s] = content
            for r in drops:
                if r not in p:
                    el[slot[r]] = None
            out.add((m, p | add if pend else p, tuple(el)))
        return frozenset(out)

    def _effect(self, cfg, x, vec):
        m, p, e = cfg
        p2 = p - frozenset((x,))
        b = self.block[x]
        s = self.slot[x]
        if self.is_write[x]:
            if m[b] is not None:
                m = m[:b] + (e[s],) + m[b + 1:]
            if vec[self.ci[x]] > self.lastref[x]:
                e = e[:s] + (None,) + e[s + 1:]
            return (m, p2, e)
        v = m[b]
        o = self.obs[x]
        if o is not None and v != o:
            return None
        if s >= 0:
            e = e[:s] + (v,) + e[s + 1:]
        return (m, p2, e)

    def _end(self, S, a, vec):
        out = set()
        effect = self._effect
        for c in S:
            if a not in c[1]:
                out.add(c)
                continue
            seen = {c}
            frontier = [c]
            while frontier:
                y = frontier.pop()
                z = effect(y, a, vec)
                if z is not None:
                    out.add(z)
                for bx in y[1]:
                    if bx != a:
                        z = effect(y, bx, vec)
                        if z is not None and z not in seen:
                            seen.add(z)
                            frontier.append(z)
        if not self.is_write[a] and out:
            b = self.block[a]
            ca = self.ci[a]
            alive = False
            for c2, lp in self.block_last[b]:
                v = vec[c2] + (1 if c2 == ca else 0)
                if v <= lp:
                    alive = True
                    break
            if not alive:
                new = set()
                for m, p, e in out:
                    drop = [y for y in p if self.is_write[y] and self.block[y] == b]
                    if drop:
                        el = list(e)
                        for y in drop:
                            cy = self.ci[y]
                            vy = vec[cy] + (1 if cy == ca else 0)
                            if vy > self.lastref[y]:
                                el[self.slot[y]] = None
                        e = tuple(el)
                        p = p - frozenset(drop)
                    m = m[:b] + (None,) + m[b + 1:]
                    new.add((m, p, e))
                out = new
        return frozenset(out)

    # ------------------------------------------------------------------ enumeration

    def enumerate(self) -> Iterator[tuple[int, ...]]:
        if self.total == 0:
            yield ()
            return
        if self.trivial:
            yield from self._interleavings()
            return
        chains, lens, n_ch, total = self.chains, self.lens, self.n_ch, self.total
        step = self.step
        node_chain = self.node_chain
        vec = [0] * n_ch
        prefix: list[int] = []
        dead: set = set()
        stack = [[self.S0, 0, False]]
        while stack:
            fr = stack[-1]
            t = fr[1]
            while t < n_ch and vec[t] >= lens[t]:
                t += 1
            if t >= n_ch:
                stack.pop()
                produced = fr[2]
                if not produced:
                    if len(dead) >= _DEAD_CAP:
                        dead.clear()
                    dead.add((tuple(vec), fr[0]))
                if stack:
                    if produced:
                        stack[-1][2] = True
                    node = prefix.pop()
                    vec[node_chain[node]] -= 1
                continue
            fr[1] = t + 1
            node = chains[t][vec[t]]
            S2 = step(fr[0], node, vec)
            if not S2:
                continue
            vec[t] += 1
            prefix.append(node)
            if len(prefix) == total:
                yield tuple(prefix)
                fr[2] = True
                prefix.pop()
                vec[t] -= 1
                continue
            key = (tuple(vec), S2)
            if key in dead:
                prefix.pop()
                vec[t] -= 1
                continue
            stack.append([S2, 0, False])

    def _interleavings(self) -> Iterator[tuple[int, ...]]:
        chains, lens, n_ch, total = self.chains, self.lens, self.n_ch, self.total
        vec = [0] * n_ch
        prefix: list[int] = []
        tstack: list[int] = []  # chain chosen at each depth
        nxt = [0]  # next chain to try at each depth
        while nxt:
            t = nxt[-1]
            while t < n_ch and vec[t] >= lens[t]:
                t += 1
            if t >= n_ch:
                nxt.pop()
                if tstack:
                    c = tstack.pop()
                    vec[c] -= 1
                    prefix.pop()
                continue
            nxt[-1] = t + 1
            prefix.append(chains[t][vec[t]])
            vec[t] += 1
            if len(prefix) == total:
                yield tuple(prefix)
                prefix.pop()
                vec[t] -= 1
                continue
            tstack.append(t)
            nxt.append(0)

    # ------------------------------------------------------------------ counting

    def n_linearizations(self) -> int:
        r, s = 1, 0
        for L in self.lens:
            s += L
            r *= comb(s, L)
        return r

    def count_feasible(self) -> int:
        if self.total == 0:
            return 1
        if self.trivial:
            return self.n_linearizations()
        chains, lens, n_ch, total = self.chains, self.lens, self.n_ch, self.total
        step = self.step
        memo: dict = {}
        stack = [[(0,) * n_ch, self.S0, 0, 0]]
        result = 0
        while stack:
            fr = stack[-1]
            vec = fr[0]
            t = fr[2]
            while t < n_ch and vec[t] >= lens[t]:
                t += 1
            if t >= n_ch:
                stack.pop()
                acc = fr[3]
                if len(memo) >= _MEMO_CAP:
                    memo.clear()
                memo[(vec, fr[1])] = acc
                if stack:
                    stack[-1][3] += acc
                else:
                    result = acc
                continue
            fr[2] = t + 1
            node = chains[t][vec[t]]
            S2 = step(fr[1], node, vec)
            if not S2:
                continue
            if len(stack) == total:
                fr[3] += 1
                continue
            v2 = vec[:t] + (vec[t] + 1,) + vec[t + 1:]
            key = (v2, S2)
            c = memo.get(key)
            if c is not None:
                fr[3] += c
                continue
            stack.append([v2, S2, 0, 0])
        return result


@register
class FeasibleEnumerator(LinEnumerator):
    name = "opus55_1-o-enum"
    description = "DFS over interleavings carrying the exact set of atomic-simulation states; dead-prefix memo"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=True)
    gray_code = False

    def enumerate(self, setup) -> Iterator[tuple[int, ...]]:
        return _Engine(setup).enumerate()


@register
class FeasibleCounter(LinCounter):
    name = "opus55_1-o-count"
    description = "Memoised DP over (chain positions, set of atomic-simulation states)"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=True)

    def count(self, setup) -> CountResult:
        eng = _Engine(setup)
        lin = eng.n_linearizations()
        has_obs = any(a.observed is not None for a in setup.actions.values())
        feas = eng.count_feasible() if has_obs else None
        return CountResult(linearizations=lin, feasible=feas, method="state-set-dp")
