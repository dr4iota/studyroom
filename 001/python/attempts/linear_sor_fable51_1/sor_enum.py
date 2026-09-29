"""Case ``sor``: enumerate and count feasible linearizations (spec §3, §5).

Method
------
Under a linearization ``L`` every action has an interval ``[pos(start), pos(done)]``.
The effect orders that some choice of distinct effect points realises are exactly the
linear extensions of the *interval order* ``a < b  iff  done(a) precedes start(b)``
(assign points greedily along the order; every constraint is a strict integer gap, so
there is always room).  ``L`` is feasible iff one of those effect orders reproduces
every observed result under the atomic block semantics.

We build ``L`` node by node (a DFS over the linear extensions of the trace poset) and
carry, for the current prefix, the **set of all simulation configurations** reachable
by effecting the currently open actions in any order.  Placing ``start(a)`` closes the
set under effecting ``a`` (and then anything open); placing ``done(a)`` keeps only the
configurations in which ``a`` has effected; an empty set prunes the whole subtree.  A
configuration is ``(effected-bitmask, block contents, values of remembered reads)``.

Blocks are coupled only through unobserved reads whose values flow into later
writes/RCWs, so the configuration set is kept per coupled group of blocks (the global
set is their product, never materialised).  Actions and blocks that cannot influence any
observation are ignored, and inside a configuration a block nobody relevant will read
again, or a read value nothing will evaluate again, is erased (the corresponding actions
become no-ops and are marked effected), so equivalent configurations merge.

The counter memoises the same search on ``(placed nodes, configuration sets)``.
"""

from __future__ import annotations

import math
import sys
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.terms import Unk, refs, substitute

PREFIX = "fable51_1-sor-"

_READ, _WRITE, _RCW = 0, 1, 2
_OBS_NONE, _OBS_TERM, _OBS_OK, _OBS_FAIL = 0, 1, 2, 3
_MEMO_LIMIT = 2_000_000  # entries; the memo is cleared beyond this to bound memory


def _read_deps(setup: Setup) -> dict[str, frozenset[str]]:
    """For every action, the reads its content and (for an RCW) its expected value depend on.

    References to writers are followed to the reads *their* contents depend on.
    """
    acts = setup.actions
    cdeps: dict[str, frozenset[str]] = {}

    def content_deps(aid: str) -> frozenset[str]:
        d = cdeps.get(aid)
        if d is not None:
            return d
        out: set[str] = set()
        e = acts[aid].data
        if e is not None:
            for r in refs(e):
                if acts[r].kind == "read":
                    out.add(r)
                else:
                    out |= content_deps(r)
        d = frozenset(out)
        cdeps[aid] = d
        return d

    deps: dict[str, frozenset[str]] = {}
    for aid, a in acts.items():
        d = set(content_deps(aid))
        if a.expect is not None:
            for r in refs(a.expect):
                if acts[r].kind == "read":
                    d.add(r)
                else:
                    d |= content_deps(r)
        deps[aid] = frozenset(d)
    return deps


class _Comp:
    """One coupled group of blocks; its configuration set evolves independently.

    A configuration is ``(eff, contents, vals)``:

    ``eff``       bitmask over this group's relevant actions: effected (or made a no-op);
    ``contents``  one interned term id per block of the group, ``None`` once no relevant
                  reader of the block remains;
    ``vals``      one interned term id per remembered read, ``None`` when unknown or
                  no longer needed.
    """

    def __init__(self, setup, blocks, action_ids, tracked_ids, deps, intern, terms) -> None:
        acts = setup.actions
        self._acts = acts
        self._intern = intern
        self._terms = terms
        self.nb = len(blocks)
        self.nt = len(tracked_ids)
        bidx = {b: j for j, b in enumerate(blocks)}
        self.tidx = {r: i for i, r in enumerate(tracked_ids)}
        self.bit = {aid: k for k, aid in enumerate(action_ids)}
        self.a_id = list(action_ids)
        self.a_kind: list[int] = []
        self.a_blk: list[int] = []
        self.a_obs_mode: list[int] = []
        self.a_obs: list[int | None] = []
        self.a_tidx: list[int] = []
        self.a_dep: list[tuple[int, ...]] = []
        self.readers_mask = [0] * self.nb
        self.writers_mask = [0] * self.nb
        self.users_mask = [0] * self.nt
        for k, aid in enumerate(action_ids):
            a = acts[aid]
            kind = _READ if a.kind == "read" else _WRITE if a.kind == "write" else _RCW
            j = bidx[a.block]
            mode, obs = _OBS_NONE, None
            if a.observed is not None:
                if isinstance(a.observed, str):  # rcw_result: flag
                    mode = _OBS_OK if a.observed == "ok" else _OBS_FAIL
                else:
                    mode, obs = _OBS_TERM, intern(a.observed)
            ti = self.tidx.get(aid, -1)
            self.a_kind.append(kind)
            self.a_blk.append(j)
            self.a_obs_mode.append(mode)
            self.a_obs.append(obs)
            self.a_tidx.append(ti)
            if mode != _OBS_NONE or ti >= 0:
                self.readers_mask[j] |= 1 << k
            if kind != _READ:
                self.writers_mask[j] |= 1 << k
            dl = []
            for r in deps[aid]:
                i = self.tidx.get(r)
                if i is not None:
                    dl.append(i)
                    self.users_mask[i] |= 1 << k
            self.a_dep.append(tuple(sorted(dl)))
        self.read_bit = [1 << self.bit[r] for r in tracked_ids]
        self._ccache: list[dict] = [{} for _ in action_ids]
        self._ecache: list[dict] = [{} for _ in action_ids]
        init = tuple(intern(setup.init[b]) for b in blocks)
        self.S0 = frozenset([self._canon(0, init, (None,) * self.nt)])

    # ------------------------------------------------------------ expression values

    def _value(self, x: str, vals):
        a = self._acts[x]
        if a.kind == "read":
            if a.observed is not None:
                return a.observed
            return self._terms[vals[self.tidx[x]]]
        return self._raw_content(x, vals)

    def _raw_content(self, x: str, vals):
        e = self._acts[x].data
        if e is None:
            return Unk(x)
        return substitute(e, lambda y: self._value(y, vals))

    def _content(self, k: int, vals) -> int:
        key = tuple([vals[i] for i in self.a_dep[k]])
        cache = self._ccache[k]
        r = cache.get(key)
        if r is None:
            r = self._intern(self._raw_content(self.a_id[k], vals))
            cache[key] = r
        return r

    def _expect(self, k: int, vals) -> int:
        key = tuple([vals[i] for i in self.a_dep[k]])
        cache = self._ecache[k]
        r = cache.get(key)
        if r is None:
            e = self._acts[self.a_id[k]].expect
            r = self._intern(substitute(e, lambda y: self._value(y, vals)))
            cache[key] = r
        return r

    # ------------------------------------------------------------ simulation

    def _canon(self, eff: int, contents, vals):
        """Erase what can no longer matter; dead actions count as effected."""
        rm, wm, um, rb = self.readers_mask, self.writers_mask, self.users_mask, self.read_bit
        changed = True
        while changed:
            changed = False
            for j in range(self.nb):
                if contents[j] is not None and not (rm[j] & ~eff):
                    contents = contents[:j] + (None,) + contents[j + 1:]
                    eff |= wm[j]
                    changed = True
            for i in range(self.nt):
                if not (um[i] & ~eff):
                    b = rb[i]
                    if vals[i] is not None or not (eff & b):
                        vals = vals[:i] + (None,) + vals[i + 1:]
                        eff |= b
                        changed = True
        return (eff, contents, vals)

    def _effect(self, c, k: int):
        """Configuration after action ``k`` takes effect; None if an observation fails."""
        eff, contents, vals = c
        kind = self.a_kind[k]
        j = self.a_blk[k]
        cur = contents[j]
        if cur is not None:
            if kind == _READ:
                if self.a_obs_mode[k] == _OBS_TERM:
                    if cur != self.a_obs[k]:
                        return None
                else:
                    ti = self.a_tidx[k]
                    if ti >= 0:
                        vals = vals[:ti] + (cur,) + vals[ti + 1:]
            elif kind == _WRITE:
                new = self._content(k, vals)
                contents = contents[:j] + (new,) + contents[j + 1:]
            else:  # RCW: result is the old content; writes only when old == expected
                exp = self._expect(k, vals)
                mode = self.a_obs_mode[k]
                if mode == _OBS_TERM:
                    if cur != self.a_obs[k]:
                        return None
                elif mode == _OBS_OK:
                    if cur != exp:
                        return None
                elif mode == _OBS_FAIL:
                    if cur == exp:
                        return None
                if cur == exp:
                    new = self._content(k, vals)
                    contents = contents[:j] + (new,) + contents[j + 1:]
        return self._canon(eff | (1 << k), contents, vals)

    def close_start(self, S, om: int, k: int):
        """``S`` closed under effects of ``om`` minus ``k``; return it closed under ``om``."""
        bit = 1 << k
        out = set(S)
        work = []
        effect = self._effect
        for c in S:
            if not (c[0] & bit):
                nc = effect(c, k)
                if nc is not None and nc not in out:
                    out.add(nc)
                    work.append(nc)
        while work:
            c = work.pop()
            avail = om & ~c[0]
            while avail:
                low = avail & -avail
                avail ^= low
                nc = effect(c, low.bit_length() - 1)
                if nc is not None and nc not in out:
                    out.add(nc)
                    work.append(nc)
        return frozenset(out)


class _Engine:
    """Relevance analysis, block grouping, and the two searches."""

    def __init__(self, setup: Setup, observe: bool = True) -> None:
        self.setup = setup
        P = setup.poset
        self.poset = P
        self.n = len(P)
        acts = setup.actions
        self._tid: dict = {}
        self.terms: list = []
        deps = _read_deps(setup)

        observed = [aid for aid, a in acts.items() if a.observed is not None] if observe else []
        rel_actions: set[str] = set()
        rel_blocks: set[int] = set()
        tracked: set[str] = set()
        work = [("reader", aid) for aid in observed]
        while work:
            what, v = work.pop()
            if what == "reader":  # an observed action or a remembered read
                work.append(("action", v))
                work.append(("block", acts[v].block))
            elif what == "action":
                if v in rel_actions:
                    continue
                rel_actions.add(v)
                for r in deps[v]:
                    if acts[r].observed is None and r not in tracked:
                        tracked.add(r)
                        work.append(("reader", r))
            else:
                if v in rel_blocks:
                    continue
                rel_blocks.add(v)
                for w in acts.values():
                    if w.writes and w.block == v:
                        work.append(("action", w.id))
        rel_list = [aid for aid in acts if aid in rel_actions]
        tr_list = [aid for aid in acts if aid in tracked]

        parent = {b: b for b in rel_blocks}

        def find(b: int) -> int:
            while parent[b] != b:
                parent[b] = parent[parent[b]]
                b = parent[b]
            return b

        for u in rel_list:
            bu = acts[u].block
            for r in deps[u]:
                if r in tracked:
                    ra, rb = find(acts[r].block), find(bu)
                    if ra != rb:
                        parent[ra] = rb
        groups: dict[int, list[int]] = {}
        for b in sorted(rel_blocks):
            groups.setdefault(find(b), []).append(b)
        comps: list[_Comp] = []
        for root in sorted(groups):
            blocks = groups[root]
            bset = set(blocks)
            aids = [aid for aid in rel_list if acts[aid].block in bset]
            trs = [r for r in tr_list if acts[r].block in bset]
            comps.append(_Comp(setup, blocks, aids, trs, deps, self._intern, self.terms))
        self.comps = comps
        self.trivial = not comps

        comp_of_action: dict[str, int] = {}
        for ci, c in enumerate(comps):
            for aid in c.a_id:
                comp_of_action[aid] = ci
        self.node_comp: list[int] = []
        self.node_bit: list[int] = []
        self.node_start: list[bool] = []
        for x in range(self.n):
            aid = P.action[x]
            kind = P.kind[x]
            if kind in ("start", "done") and aid in comp_of_action:
                ci = comp_of_action[aid]
                self.node_comp.append(ci)
                self.node_bit.append(comps[ci].bit[aid])
            else:
                self.node_comp.append(-1)
                self.node_bit.append(-1)
            self.node_start.append(kind == "start")
        self.S0 = tuple(c.S0 for c in comps)
        self.om0 = (0,) * len(comps)

    def _intern(self, t) -> int:
        i = self._tid.get(t)
        if i is None:
            i = len(self.terms)
            self._tid[t] = i
            self.terms.append(t)
        return i

    def _transition(self, S, om, x: int):
        """State after placing node ``x``; ``(None, None)`` when no completion is feasible."""
        ci = self.node_comp[x]
        if ci < 0:
            return S, om
        k = self.node_bit[x]
        bit = 1 << k
        if self.node_start[x]:
            om_c = om[ci] | bit
            S_c = self.comps[ci].close_start(S[ci], om_c, k)
        else:
            S_c = frozenset([c for c in S[ci] if c[0] & bit])
            if not S_c:
                return None, None
            om_c = om[ci] & ~bit
        return S[:ci] + (S_c,) + S[ci + 1:], om[:ci] + (om_c,) + om[ci + 1:]

    # ------------------------------------------------------------ enumeration

    def linearizations(self) -> Iterator[Linearization]:
        n = self.n
        if n == 0:
            yield ()
            return
        succs = self.poset.succs
        indeg = [len(p) for p in self.poset.preds]
        ready = {x for x in range(n) if indeg[x] == 0}
        order: list[int] = []
        transition = self._transition
        # frame: [candidates, next index, S, om, node placed to enter this frame, nodes it readied]
        frames = [[sorted(ready), 0, self.S0, self.om0, -1, []]]
        while frames:
            fr = frames[-1]
            cands = fr[0]
            i = fr[1]
            if i == len(cands):
                frames.pop()
                x = fr[4]
                if x >= 0:
                    order.pop()
                    for y in fr[5]:
                        ready.discard(y)
                    for y in succs[x]:
                        indeg[y] += 1
                    ready.add(x)
                continue
            fr[1] = i + 1
            x = cands[i]
            S2, om2 = transition(fr[2], fr[3], x)
            if S2 is None:
                continue
            order.append(x)
            ready.discard(x)
            added = []
            for y in succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    ready.add(y)
                    added.append(y)
            if len(order) == n:
                yield tuple(order)
                order.pop()
                for y in added:
                    ready.discard(y)
                for y in succs[x]:
                    indeg[y] += 1
                ready.add(x)
                continue
            frames.append([sorted(ready), 0, S2, om2, x, added])

    # ------------------------------------------------------------ counting

    def count(self) -> int:
        n = self.n
        succs = self.poset.succs
        indeg = [len(p) for p in self.poset.preds]
        ready = {x for x in range(n) if indeg[x] == 0}
        full = (1 << n) - 1
        memo: dict = {}
        trivial = self.trivial
        transition = self._transition
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 2000))

        def rec(placed: int, S, om) -> int:
            if placed == full:
                return 1
            key = placed if trivial else (placed, S)
            v = memo.get(key)
            if v is not None:
                return v
            total = 0
            for x in sorted(ready):
                S2, om2 = transition(S, om, x)
                if S2 is None:
                    continue
                ready.discard(x)
                added = []
                for y in succs[x]:
                    indeg[y] -= 1
                    if indeg[y] == 0:
                        ready.add(y)
                        added.append(y)
                total += rec(placed | (1 << x), S2, om2)
                for y in added:
                    ready.discard(y)
                for y in succs[x]:
                    indeg[y] += 1
                ready.add(x)
            if len(memo) >= _MEMO_LIMIT:
                memo.clear()
            memo[key] = total
            return total

        return rec(0, self.S0, self.om0)


def _count_lin(setup: Setup) -> int:
    """``|Lin(P)|``: a multinomial when P is a disjoint union of chains, else an ideal DP."""
    P = setup.poset
    if all(not P.preds[s] and not P.succs[s] for s in P.sync_nodes):
        r = math.factorial(len(P))
        for c in P.chains:
            r //= math.factorial(len(c))
        return r
    return _Engine(setup, observe=False).count()


@register
class SorEnumerator(LinEnumerator):
    name = PREFIX + "enum"
    description = "DFS over linear extensions carrying the set of reachable effect-order configurations; prunes infeasible prefixes"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=True)
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return _Engine(setup).linearizations()


@register
class SorCounter(LinCounter):
    name = PREFIX + "count"
    description = "Memoised DP on (placed nodes, configuration sets); |Lin(P)| by multinomial or ideal DP"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=True)

    def count(self, setup: Setup) -> CountResult:
        lin = _count_lin(setup)
        eng = _Engine(setup)
        feas = lin if eng.trivial else eng.count()
        return CountResult(linearizations=lin, feasible=feas, method="configset-dp")
