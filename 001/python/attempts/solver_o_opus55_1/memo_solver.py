"""Exact possibility-set solver for case `o` (reads, writes, observed reads, no sync).

Reduction (see SOURCES.md): a total order sigma of the actions is the effect order of
some full schedule (L, pi) iff sigma extends the relation

    a <_Q b  iff  done(a) <_P start(b)            (mode "all")
    a <_Q b  iff  pos_L(done(a)) < pos_L(start(b)) (mode "fixed", given L)

The solver explores all linear extensions of Q with a memoised DFS over states
(set of executed actions, block contents, values of reads still needed by pending
writes), pruning reads whose value contradicts an observation. A state is live when
some completion reaches the end; values are collected only on edges into live states.
"""

from __future__ import annotations

import sys

from harness import terms as T
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class MemoSolver(Solver):
    name = "opus55_1-o-memo"
    description = "Memoised DFS over effect orders (linear extensions of the end<start order) with observation pruning"
    capabilities = SolverCapabilities(
        rcw=False,
        sync=False,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup, linearization=None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        acts = list(setup.actions.values())
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        P = setup.poset

        # ---------------------------------------------------------------- order Q
        pred = [0] * n
        if linearization is None:
            nn = len(P)
            desc = [0] * nn
            for x in reversed(P.topological_order()):
                d = 1 << x
                for y in P.succs[x]:
                    d |= desc[y]
                desc[x] = d
            for i, a in enumerate(acts):
                sa = P.start_node[a.id]
                for j, b in enumerate(acts):
                    if j != i and (desc[P.done_node[b.id]] >> sa) & 1:
                        pred[i] |= 1 << j
        else:
            pos = P.positions(linearization)
            for i, a in enumerate(acts):
                sa = pos[P.start_node[a.id]]
                for j, b in enumerate(acts):
                    if j != i and pos[P.done_node[b.id]] < sa:
                        pred[i] |= 1 << j

        # ---------------------------------------------------------------- terms
        tid: dict = {}
        tl: list = []

        def intern(t) -> int:
            k = tid.get(t)
            if k is None:
                k = len(tl)
                tid[t] = k
                tl.append(t)
            return k

        isread = [a.kind == "read" for a in acts]
        block = [a.block for a in acts]
        obs = [intern(a.observed) if (a.kind == "read" and a.observed is not None) else None for a in acts]

        # reads each write depends on (transitively through referenced writes)
        need_memo: dict[int, frozenset] = {}

        def need(i: int) -> frozenset:
            r = need_memo.get(i)
            if r is not None:
                return r
            s: set[int] = set()
            e = acts[i].data
            if e is not None:
                for ref in T.refs(e):
                    j = idx[ref]
                    if isread[j]:
                        s.add(j)
                    else:
                        s |= need(j)
            r = frozenset(s)
            need_memo[i] = r
            return r

        slot = [-1] * n
        slot_reads: list[int] = []
        for i in range(n):
            if not isread[i]:
                for j in need(i):
                    if slot[j] < 0:
                        slot[j] = len(slot_reads)
                        slot_reads.append(j)
        nslots = len(slot_reads)
        cmask = [0] * nslots
        wslots: list[list[int]] = [[] for _ in range(n)]
        for i in range(n):
            if not isread[i]:
                for j in need(i):
                    k = slot[j]
                    cmask[k] |= 1 << i
                    wslots[i].append(k)

        static = [None] * n
        for i in range(n):
            if not isread[i] and not need(i):
                static[i] = intern(setup.static_content(acts[i].id))

        def content_term(i: int, vals: tuple):
            a = acts[i]
            if a.data is None:
                return T.Unk(a.id)

            def lookup(x: str):
                j = idx[x]
                if isread[j]:
                    return tl[vals[slot[j]]]
                return content_term(j, vals)

            return T.substitute(a.data, lookup)

        wcache: dict = {}

        def content(i: int, vals: tuple) -> int:
            s = static[i]
            if s is not None:
                return s
            key = (i, tuple(vals[k] for k in wslots[i]))
            c = wcache.get(key)
            if c is None:
                c = intern(content_term(i, vals))
                wcache[key] = c
            return c

        # ---------------------------------------------------------------- search
        full = (1 << n) - 1
        memo: dict = {}
        res: list[set] = [set() for _ in range(n)]
        finals: set = set()

        def dfs(mask: int, cont: tuple, vals: tuple) -> bool:
            key = (mask, cont, vals)
            r = memo.get(key)
            if r is not None:
                return r
            if mask == full:
                finals.add(cont)
                memo[key] = True
                return True
            live = False
            m = full & ~mask
            while m:
                low = m & -m
                m ^= low
                i = low.bit_length() - 1
                if pred[i] & ~mask:
                    continue
                b = block[i]
                nmask = mask | low
                if isread[i]:
                    v = cont[b]
                    o = obs[i]
                    if o is not None and v != o:
                        continue
                    k = slot[i]
                    nvals = vals if k < 0 else vals[:k] + (v,) + vals[k + 1:]
                    if dfs(nmask, cont, nvals):
                        live = True
                        res[i].add(v)
                else:
                    c = content(i, vals)
                    ncont = cont[:b] + (c,) + cont[b + 1:]
                    nvals = vals
                    if wslots[i]:
                        lv = list(vals)
                        for k in wslots[i]:
                            if (nmask & cmask[k]) == cmask[k]:
                                lv[k] = -1
                        nvals = tuple(lv)
                    if dfs(nmask, ncont, nvals):
                        live = True
            memo[key] = live
            return live

        old = sys.getrecursionlimit()
        if old < 20000 + 4 * n:
            sys.setrecursionlimit(20000 + 4 * n)
        try:
            init = tuple(intern(t) for t in setup.init)
            ok = dfs(0, init, (-1,) * nslots)
        finally:
            sys.setrecursionlimit(old)

        if not ok:
            return Outcomes(mode, False)
        results = {a.id: {tl[v] for v in res[i]} for i, a in enumerate(acts) if isread[i]}
        final = {bb: {tl[c[bb]] for c in finals} for bb in range(setup.blocks)}
        return Outcomes(mode, True, results, final)
