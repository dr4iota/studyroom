"""Exact possibility-set solver for case ``sr`` (sync points, RCWs, no observations).

Method
------
A full schedule ``(L, pi)`` only matters through its *effect order* (the order of the
effect points). An effect order ``sigma`` (a total order of the actions) is realizable
by some full schedule iff it extends the real-time order

    a -> b   iff   done(a) < start(b)

where ``<`` is the order of the trace poset ``P`` (mode ``all``) or the order of the
given linearization ``L`` (mode ``fixed``).

Proof sketch (mode ``all``): add one effect node ``e_a`` per action with
``start(a) < e_a < done(a)`` and chain the effect nodes in the order ``sigma``. The
augmented graph is acyclic iff no path goes from some ``e_x`` back to an ``e_y`` with
``y`` earlier in ``sigma``; the only way to go "backwards" is
``e_x < done(x) <_P start(y) < e_y`` with ``y`` before ``x`` in ``sigma``, which is exactly
a violation of the real-time order. Any linear extension of the acyclic augmented graph
gives ``L`` and effect points. Mode ``fixed``: intervals with distinct integer endpoints
admit strictly increasing points in order ``sigma`` iff ``sigma`` extends the interval
order.

So ``Poss`` is the set of values obtained by running the atomic semantics along every
linear extension of the real-time order. We explore these by DFS over states
``(executed downset, block contents, still-needed read values)`` with memoisation;
every reachable state extends to a complete schedule, so every value recorded on a
transition (reads/RCWs) or at a complete state (final contents) is realized, and every
realizable value is recorded.
"""

from __future__ import annotations

from harness import terms as T
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class DownsetSolver(Solver):
    name = "opus55_1-sr-downset"
    description = "DFS over downsets of the real-time order with memoised block contents (exact Poss)"
    capabilities = SolverCapabilities(
        rcw=True,
        sync=True,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup, linearization=None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        acts = list(setup.actions.values())
        n = len(acts)
        amap = setup.actions
        poset = setup.poset

        # ------------------------------------------------------------ real-time order
        start_of = [poset.start_node[a.id] for a in acts]
        done_of = [poset.done_node[a.id] for a in acts]
        pred = [0] * n
        if linearization is None:
            N = len(poset)
            desc = [0] * N
            for x in reversed(poset.topological_order()):
                m = 0
                for y in poset.succs[x]:
                    m |= desc[y] | (1 << y)
                desc[x] = m
            for i in range(n):
                d = desc[done_of[i]]
                for j in range(n):
                    if i != j and (d >> start_of[j]) & 1:
                        pred[j] |= 1 << i
        else:
            pos = poset.positions(linearization)
            for i in range(n):
                pd = pos[done_of[i]]
                for j in range(n):
                    if i != j and pd < pos[start_of[j]]:
                        pred[j] |= 1 << i

        # ------------------------------------------------------------ data dependencies
        content_deps_memo: dict[str, frozenset] = {}

        def content_deps(x: str) -> frozenset:
            """Reads that the content of write/rcw ``x`` depends on (transitively)."""
            r = content_deps_memo.get(x)
            if r is not None:
                return r
            a = amap[x]
            out: set[str] = set()
            if a.data is not None:
                for ref in T.refs(a.data):
                    b = amap[ref]
                    if b.kind == "read":
                        out.add(ref)
                    else:
                        out |= content_deps(ref)
            r = frozenset(out)
            content_deps_memo[x] = r
            return r

        def expr_deps(e) -> set:
            out: set[str] = set()
            if e is None:
                return out
            for ref in T.refs(e):
                b = amap[ref]
                if b.kind == "read":
                    out.add(ref)
                else:
                    out |= content_deps(ref)
            return out

        deps: dict[int, set] = {}
        referenced: set[str] = set()
        for i, a in enumerate(acts):
            if a.kind != "read":
                d = set(content_deps(a.id)) | expr_deps(a.expect)
                deps[i] = d
                referenced |= d
        slot_ids = sorted(referenced, key=lambda r: list(amap).index(r))
        slot = {r: k for k, r in enumerate(slot_ids)}
        nslots = len(slot_ids)
        depmask = [0] * n  # bitmask of read slots each writer needs
        for i, d in deps.items():
            m = 0
            for r in d:
                m |= 1 << slot[r]
            depmask[i] = m
        writers = [i for i in range(n) if acts[i].kind != "read"]
        slot_of_action = [slot.get(a.id, -1) for a in acts]

        # static (read-independent) content / expected values
        static_content: dict[int, T.Term] = {}
        static_expect: dict[int, T.Term] = {}
        for i in writers:
            a = acts[i]
            if not content_deps(a.id):
                static_content[i] = self._content(a.id, amap, None, slot)
            if a.kind == "rcw" and not expr_deps(a.expect):
                static_expect[i] = self._eval(a.expect, amap, None, slot)

        need_cache: dict[int, int] = {}

        def needed(S: int) -> int:
            m = need_cache.get(S)
            if m is None:
                m = 0
                for i in writers:
                    if not (S >> i) & 1:
                        m |= depmask[i]
                need_cache[S] = m
            return m

        # ------------------------------------------------------------ search
        results: dict[str, set] = {a.id: set() for a in acts if a.kind != "write"}
        final: dict[int, set] = {b: set() for b in range(setup.blocks)}
        full = (1 << n) - 1
        kinds = [a.kind for a in acts]
        blocks_of = [a.block for a in acts]
        ids = [a.id for a in acts]

        init_state = (0, tuple(setup.init), (None,) * nslots)
        seen = {init_state}
        stack = [init_state]
        while stack:
            S, cont, rv = stack.pop()
            if S == full:
                for b, v in enumerate(cont):
                    final[b].add(v)
                continue
            for i in range(n):
                if (S >> i) & 1 or pred[i] & ~S:
                    continue
                S2 = S | (1 << i)
                b = blocks_of[i]
                cur = cont[b]
                k = kinds[i]
                new_cont = cont
                new_rv = rv
                if k == "read":
                    results[ids[i]].add(cur)
                    s = slot_of_action[i]
                    if s >= 0:
                        lst = list(rv)
                        lst[s] = cur
                        new_rv = tuple(lst)
                else:
                    if k == "rcw":
                        results[ids[i]].add(cur)
                        exp = static_expect.get(i)
                        if exp is None:
                            exp = self._eval(acts[i].expect, amap, rv, slot)
                        do_write = cur == exp
                    else:
                        do_write = True
                    if do_write:
                        val = static_content.get(i)
                        if val is None:
                            val = self._content(ids[i], amap, rv, slot)
                        if val != cur:
                            lst = list(cont)
                            lst[b] = val
                            new_cont = tuple(lst)
                # drop read values no longer needed
                if nslots:
                    need = needed(S2)
                    if any(v is not None and not (need >> s) & 1 for s, v in enumerate(new_rv)):
                        new_rv = tuple(v if (need >> s) & 1 else None for s, v in enumerate(new_rv))
                st = (S2, new_cont, new_rv)
                if st not in seen:
                    seen.add(st)
                    stack.append(st)

        return Outcomes(mode, True, results, final)

    # ---------------------------------------------------------------- evaluation
    @staticmethod
    def _eval(e, amap, rv, slot):
        def lookup(x: str):
            a = amap[x]
            if a.kind == "read":
                return rv[slot[x]]
            return DownsetSolver._content(x, amap, rv, slot)

        return T.substitute(e, lookup)

    @staticmethod
    def _content(x, amap, rv, slot):
        a = amap[x]
        if a.data is None:
            return T.Unk(x)
        return DownsetSolver._eval(a.data, amap, rv, slot)
