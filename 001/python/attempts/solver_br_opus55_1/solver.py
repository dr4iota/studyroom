"""Exact possibility-set solver for case br (reads, writes, RCWs; no sync, no observations).

Reduction (see SOURCES.md): an effect order sigma (a total order of the actions) is
realisable by some full schedule iff sigma extends the precedence relation
``a -> b  iff  end(a) < start(b)`` (in P for mode "all", in the fixed L for mode "fixed").
So Poss is the union, over all linear extensions of that relation, of the results of
executing the actions atomically in that order. We explore those executions by a DFS
over memoised states (executed set, block contents, values of reads still needed).
"""

from __future__ import annotations

from harness import terms as T
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class EffectOrderSolver(Solver):
    name = "opus55_1-br-effect-dp"
    description = "Memoised DFS over effect orders extending the end-before-start precedence (exact Poss)."
    capabilities = SolverCapabilities(
        rcw=True,
        sync=False,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup, linearization=None) -> Outcomes:
        acts = list(setup.actions.values())
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        poset = setup.poset
        mode = "all" if linearization is None else "fixed"

        # ---------------------------------------------------------- precedence relation
        if linearization is None:
            reach = [0] * len(poset)
            for u in reversed(poset.topological_order()):
                r = 0
                for v in poset.succs[u]:
                    r |= (1 << v) | reach[v]
                reach[u] = r

            def before(a, b) -> bool:
                return bool((reach[poset.done_node[a.id]] >> poset.start_node[b.id]) & 1)
        else:
            pos = poset.positions(linearization)

            def before(a, b) -> bool:
                return pos[poset.done_node[a.id]] < pos[poset.start_node[b.id]]

        pred = [0] * n
        for j, b in enumerate(acts):
            m = 0
            for i, a in enumerate(acts):
                if i != j and before(a, b):
                    m |= 1 << i
            pred[j] = m

        # ---------------------------------------------------------- read dependencies
        cdeps_memo: dict[int, int] = {}

        def expr_deps(e) -> int:
            m = 0
            if e is None:
                return 0
            for x in T.refs(e):
                j = idx[x]
                if acts[j].kind == "read":
                    m |= 1 << j
                else:
                    m |= content_deps(j)
            return m

        def content_deps(i: int) -> int:
            r = cdeps_memo.get(i)
            if r is None:
                r = expr_deps(acts[i].data) if acts[i].kind != "read" else 0
                cdeps_memo[i] = r
            return r

        def bits(m: int) -> list[int]:
            return [j for j in range(n) if (m >> j) & 1]

        cdeps = [0] * n
        edeps = [0] * n
        alldeps = [0] * n
        for i, a in enumerate(acts):
            if a.kind != "read":
                cdeps[i] = content_deps(i)
                if a.kind == "rcw":
                    edeps[i] = expr_deps(a.expect)
                alldeps[i] = cdeps[i] | edeps[i]
        cdeps_list = [bits(m) for m in cdeps]
        edeps_list = [bits(m) for m in edeps]
        writer_idx = [i for i, a in enumerate(acts) if a.kind != "read"]

        need_cache: dict[int, int] = {}

        def need(mask: int) -> int:
            r = need_cache.get(mask)
            if r is None:
                r = 0
                for i in writer_idx:
                    if not (mask >> i) & 1:
                        r |= alldeps[i]
                r &= mask
                need_cache[mask] = r
            return r

        # ---------------------------------------------------------- term interning
        terms: list = []
        tid: dict = {}

        def intern(t) -> int:
            k = tid.get(t)
            if k is None:
                k = len(terms)
                tid[t] = k
                terms.append(t)
            return k

        ccache: dict = {}
        ecache: dict = {}

        def look(x: str, vals):
            j = idx[x]
            if acts[j].kind == "read":
                return terms[vals[j]]
            return terms[content(j, vals)]

        def content(i: int, vals) -> int:
            key = (i, tuple(vals[j] for j in cdeps_list[i]))
            r = ccache.get(key)
            if r is None:
                a = acts[i]
                if a.data is None:
                    r = intern(T.Unk(a.id))
                else:
                    r = intern(T.substitute(a.data, lambda x: look(x, vals)))
                ccache[key] = r
            return r

        def expect(i: int, vals) -> int:
            key = (i, tuple(vals[j] for j in edeps_list[i]))
            r = ecache.get(key)
            if r is None:
                r = intern(T.substitute(acts[i].expect, lambda x: look(x, vals)))
                ecache[key] = r
            return r

        # ---------------------------------------------------------- exploration
        blocks = [a.block for a in acts]
        kinds = [a.kind for a in acts]
        full = (1 << n) - 1
        res: list[set[int]] = [set() for _ in range(n)]
        fin: list[set[int]] = [set() for _ in range(setup.blocks)]

        start = (0, tuple(intern(t) for t in setup.init), tuple([-1] * n))
        seen = {start}
        stack = [start]
        while stack:
            mask, cont, vals = stack.pop()
            if mask == full:
                for b, v in enumerate(cont):
                    fin[b].add(v)
                continue
            for i in range(n):
                if (mask >> i) & 1 or pred[i] & ~mask:
                    continue
                k = blocks[i]
                kind = kinds[i]
                nmask = mask | (1 << i)
                ncont = cont
                if kind == "read":
                    v = cont[k]
                    res[i].add(v)
                elif kind == "write":
                    c = content(i, vals)
                    if c != cont[k]:
                        lst = list(cont)
                        lst[k] = c
                        ncont = tuple(lst)
                else:  # rcw
                    v = cont[k]
                    res[i].add(v)
                    if v == expect(i, vals):
                        c = content(i, vals)
                        if c != v:
                            lst = list(cont)
                            lst[k] = c
                            ncont = tuple(lst)
                nd = need(nmask)
                if kind == "read":
                    nv = tuple((cont[k] if j == i else vals[j]) if (nd >> j) & 1 else -1 for j in range(n))
                else:
                    nv = tuple(vals[j] if (nd >> j) & 1 else -1 for j in range(n))
                ns = (nmask, ncont, nv)
                if ns not in seen:
                    seen.add(ns)
                    stack.append(ns)

        out = Outcomes(mode, True)
        for i, a in enumerate(acts):
            if a.kind != "write":
                out.results[a.id] = {terms[v] for v in res[i]}
        for b in range(setup.blocks):
            out.final[b] = {terms[v] for v in fin[b]}
        return out
