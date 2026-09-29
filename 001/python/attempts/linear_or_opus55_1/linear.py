"""Feasible-linearization enumerator and counter for case ``or`` (K = 0, observed
results, RCW actions).

Method: depth-first search over prefixes of the thread interleaving. For each prefix we
keep the set of all reachable *simulation states* of the atomic semantics, where an
action's effect point may be placed anywhere between its start and its end. A state is
``(fired, blocks, vals)``:

* ``fired``  bitmask of open (started, not ended) tracked actions whose effect happened;
* ``blocks`` current content of every block;
* ``vals``   per action: the value a read returned, or the evaluated content of a write
             (for an RCW: ``(content, expected)``), kept only while still needed.

After a start node the set is closed under firing any pending effect; at an end node
only states in which that action has fired survive. A prefix is extendable iff its state
set is non-empty and some completion exists; this is memoised (``alive``) so that the
enumerator never enters a dead branch.
"""

from __future__ import annotations

import sys
from math import factorial
from typing import Iterator

from harness import terms as T
from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.registry import register

_MEMO_CAP = 1_000_000


class _Model:
    def __init__(self, setup: Setup) -> None:
        P = setup.poset
        self.chains = [list(c) for c in P.thread_chains]
        self.T = len(self.chains)
        self.L = tuple(len(c) for c in self.chains)
        acts = list(setup.actions.values())
        self.acts = acts
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        self.idx = idx
        self.flag = setup.semantics.rcw_result == "flag"
        self.has_obs = any(a.observed is not None for a in acts)

        self.kind = [a.kind for a in acts]
        self.block = [a.block for a in acts]
        self.thr = [a.thread for a in acts]
        self.data = [a.data for a in acts]
        self.expect = [a.expect for a in acts]
        self.obs = [a.observed for a in acts]
        self.ids = [a.id for a in acts]

        # node -> (action index, is_start)
        self.node_act = [0] * len(P)
        self.node_start = [False] * len(P)
        for a in acts:
            i = idx[a.id]
            self.node_act[P.start_node[a.id]] = i
            self.node_start[P.start_node[a.id]] = True
            self.node_act[P.done_node[a.id]] = i
        self.done_pos = [P.pos_in_chain[P.done_node[a.id]] for a in acts]

        # references
        referrers: list[list[int]] = [[] for _ in range(n)]
        for i, a in enumerate(acts):
            rs: set[str] = set()
            for e in (a.data, a.expect):
                if e is not None:
                    rs |= T.refs(e)
            for r in rs:
                referrers[idx[r]].append(i)
        self.referenced = [bool(referrers[i]) for i in range(n)]
        self.lastref_pos = [
            max((P.pos_in_chain[P.start_node[acts[j].id]] for j in referrers[i]), default=-1) for i in range(n)
        ]

        # which actions must be simulated
        important_ret = [
            (a.kind != "write") and (a.observed is not None or (a.kind == "read" and self.referenced[i]))
            for i, a in enumerate(acts)
        ]
        imp_block = set(acts[i].block for i in range(n) if important_ret[i])
        self.tracked = [
            important_ret[i] or (acts[i].kind != "read" and acts[i].block in imp_block) for i in range(n)
        ]
        # whether a value is stored in vals
        self.store = [
            self.referenced[i] if acts[i].kind == "read" else (self.tracked[i] or self.referenced[i]) for i in range(n)
        ]
        self.valued = [i for i in range(n) if self.store[i]]
        self.init_state = (0, tuple(setup.init), tuple([None] * n))
        self.ends = self.L

    # ------------------------------------------------------------------ semantics

    def _lookup(self, vals):
        kind, idx = self.kind, self.idx

        def lk(rid: str):
            x = idx[rid]
            v = vals[x]
            if kind[x] == "rcw":
                return v[0]
            return v

        return lk

    def _fire(self, s, j):
        fired, blocks, vals = s
        b = self.block[j]
        k = self.kind[j]
        if k == "write":
            nb = list(blocks)
            nb[b] = vals[j]
            return (fired | (1 << j), tuple(nb), vals)
        if k == "read":
            v = blocks[b]
            o = self.obs[j]
            if o is not None and v != o:
                return None
            if self.referenced[j]:
                nv = list(vals)
                nv[j] = v
                vals = tuple(nv)
            return (fired | (1 << j), blocks, vals)
        # rcw
        old = blocks[b]
        c, e = vals[j]
        ok = old == e
        o = self.obs[j]
        if o is not None:
            if self.flag and isinstance(o, str):
                if ok != (o == "ok"):
                    return None
            elif old != o:
                return None
        if ok:
            nb = list(blocks)
            nb[b] = c
            blocks = tuple(nb)
        return (fired | (1 << j), blocks, vals)

    def _canon(self, s, pos):
        fired, blocks, vals = s
        changed = False
        nv = None
        for x in self.valued:
            if vals[x] is None:
                continue
            p = pos[self.thr[x]]
            if p <= self.lastref_pos[x]:
                continue  # a referrer has not started yet
            if (
                self.tracked[x]
                and self.kind[x] != "read"
                and not (fired >> x) & 1
                and p <= self.done_pos[x]
            ):
                continue  # effect still pending
            if nv is None:
                nv = list(vals)
            nv[x] = None
            changed = True
        if changed:
            return (fired, blocks, tuple(nv))
        return s

    def step(self, pos, op, states, t):
        n = self.chains[t][pos[t]]
        i = self.node_act[n]
        lp = list(pos)
        lp[t] += 1
        npos = tuple(lp)
        bit = 1 << i
        if self.node_start[n]:
            new = set()
            if self.store[i]:
                k = self.kind[i]
                for s in states:
                    fired, blocks, vals = s
                    lk = self._lookup(vals)
                    d = self.data[i]
                    c = T.Unk(self.ids[i]) if d is None else T.substitute(d, lk)
                    if k == "rcw":
                        c = (c, T.substitute(self.expect[i], lk))
                    nv = list(vals)
                    nv[i] = c
                    new.add((fired, blocks, tuple(nv)))
            else:
                new = set(states)
            if self.tracked[i]:
                op |= bit
                res = set()
                stack = list(new)
                while stack:
                    s = stack.pop()
                    if s in res:
                        continue
                    res.add(s)
                    pend = op & ~s[0]
                    while pend:
                        low = pend & -pend
                        pend ^= low
                        s2 = self._fire(s, low.bit_length() - 1)
                        if s2 is not None and s2 not in res:
                            stack.append(s2)
                new = res
        else:
            if self.tracked[i]:
                op &= ~bit
                new = set((f & ~bit, b, v) for (f, b, v) in states if f & bit)
            else:
                new = states
        out = frozenset(self._canon(s, npos) for s in new)
        return npos, op, out

    # ------------------------------------------------------------------ search

    def root(self):
        pos = tuple([0] * self.T)
        return pos, 0, frozenset([self._canon(self.init_state, pos)])


class _Search:
    def __init__(self, m: _Model) -> None:
        self.m = m
        self.memo: dict = {}

    def alive(self, pos, op, st) -> bool:
        m = self.m
        if pos == m.ends:
            return True
        key = (pos, st)
        r = self.memo.get(key)
        if r is not None:
            return r
        r = False
        for t in range(m.T):
            if pos[t] < m.L[t]:
                np_, no, ns = m.step(pos, op, st, t)
                if ns and self.alive(np_, no, ns):
                    r = True
                    break
        if len(self.memo) >= _MEMO_CAP:
            self.memo.clear()
        self.memo[key] = r
        return r

    def count(self, pos, op, st) -> int:
        m = self.m
        if pos == m.ends:
            return 1
        key = (pos, st)
        r = self.memo.get(key)
        if r is not None:
            return r
        r = 0
        for t in range(m.T):
            if pos[t] < m.L[t]:
                np_, no, ns = m.step(pos, op, st, t)
                if ns:
                    r += self.count(np_, no, ns)
        if len(self.memo) >= _MEMO_CAP:
            self.memo.clear()
        self.memo[key] = r
        return r


def _raise_limit(nodes: int) -> None:
    need = 4 * nodes + 1000
    if sys.getrecursionlimit() < need:
        sys.setrecursionlimit(need)


def _interleavings(chains: list[list[int]]) -> Iterator[tuple[int, ...]]:
    Tn = len(chains)
    L = [len(c) for c in chains]
    total = sum(L)
    if total == 0:
        yield ()
        return
    pos = [0] * Tn
    path: list[int] = []
    tstack: list[int] = []  # thread chosen at each depth
    t = 0
    while True:
        # find next thread >= t that can advance
        while t < Tn and pos[t] >= L[t]:
            t += 1
        if t < Tn:
            path.append(chains[t][pos[t]])
            pos[t] += 1
            tstack.append(t)
            if len(path) == total:
                yield tuple(path)
                # backtrack one level
                tt = tstack.pop()
                path.pop()
                pos[tt] -= 1
                t = tt + 1
            else:
                t = 0
            continue
        # no thread left at this depth: backtrack
        if not tstack:
            return
        tt = tstack.pop()
        path.pop()
        pos[tt] -= 1
        t = tt + 1


CAPS = Capabilities(rcw=True, sync=False, observed_reads=True)


@register
class FeasibleLinEnumerator(LinEnumerator):
    name = "opus55_1-or-enum"
    description = "DFS over interleavings with reachable effect-state sets and memoised dead-branch pruning"
    capabilities = CAPS

    def enumerate(self, setup: Setup) -> Iterator[tuple[int, ...]]:
        m = _Model(setup)
        if not m.has_obs:
            yield from _interleavings(m.chains)
            return
        _raise_limit(len(setup.poset))
        S = _Search(m)
        pos, op, st = m.root()
        if not st or not S.alive(pos, op, st):
            return
        if pos == m.ends:
            yield ()
            return
        frames = [[pos, op, st, 0]]
        path: list[int] = []
        while frames:
            fr = frames[-1]
            pos, op, st, t = fr
            pushed = False
            while t < m.T:
                if pos[t] < m.L[t]:
                    np_, no, ns = m.step(pos, op, st, t)
                    if ns and S.alive(np_, no, ns):
                        fr[3] = t + 1
                        path.append(m.chains[t][pos[t]])
                        if np_ == m.ends:
                            yield tuple(path)
                            path.pop()
                            t += 1
                            continue
                        frames.append([np_, no, ns, 0])
                        pushed = True
                        break
                t += 1
            if not pushed:
                frames.pop()
                if frames:
                    path.pop()


@register
class FeasibleLinCounter(LinCounter):
    name = "opus55_1-or-count"
    description = "Memoised count over (thread positions, reachable effect-state set); |Lin(P)| by multinomial"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        m = _Model(setup)
        L = m.L
        lin = factorial(sum(L))
        for x in L:
            lin //= factorial(x)
        if not m.has_obs:
            return CountResult(linearizations=lin, feasible=None, method="multinomial")
        _raise_limit(len(setup.poset))
        S = _Search(m)
        pos, op, st = m.root()
        feas = S.count(pos, op, st) if st else 0
        return CountResult(linearizations=lin, feasible=feas, method="state-set-dp")
