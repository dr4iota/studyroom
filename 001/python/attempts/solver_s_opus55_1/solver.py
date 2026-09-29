"""Exact possibility-set solver for case s (sync points, no observed reads).

Reduction: an effect order sigma (a total order of the actions) is realizable by some
full schedule iff sigma is a linear extension of the "happens-before" order hb, where
a hb b iff done(a) precedes start(b) (in P for mode "all", in L for mode "fixed").
The values produced depend only on sigma, so we explore all linear extensions of hb
by a memoized search over downsets, keeping only the data that can still matter:

* the content of block b, only while some read of b is still pending;
* the value of a read, only while some pending write's content depends on it.

A block's final content is recorded as soon as no write to it is pending; a read's
value is recorded when it executes. Without observations every reachable state
extends to a complete schedule, so everything recorded is realizable.
"""

from __future__ import annotations

from harness import terms as T
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities

DEAD = -1


class _Interner:
    """Hash-consing of terms: equal terms get equal integer ids."""

    def __init__(self) -> None:
        self.table: dict = {}
        self.terms: list = []

    def _get(self, key, build):
        i = self.table.get(key)
        if i is None:
            i = len(self.terms)
            self.table[key] = i
            self.terms.append(build())
        return i

    def pair(self, l: int, r: int) -> int:
        return self._get(("p", l, r), lambda: T.Pair(self.terms[l], self.terms[r]))

    def term(self, t) -> int:
        if isinstance(t, T.Pair):
            return self.pair(self.term(t.left), self.term(t.right))
        if isinstance(t, T.Const):
            return self._get(("c", t.value), lambda: t)
        if isinstance(t, T.Init):
            return self._get(("i", t.block), lambda: t)
        if isinstance(t, T.Unk):
            return self._get(("u", t.action), lambda: t)
        raise TypeError(f"unexpected term node {t!r}")


@register
class DownsetSolver(Solver):
    name = "opus55_1-s-downset"
    description = "Exact Poss via memoized search over linear extensions of the happens-before order of actions"
    capabilities = SolverCapabilities(
        rcw=False,
        sync=True,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        acts = list(setup.actions.values())
        m = len(acts)
        nb = setup.blocks
        idx = {a.id: i for i, a in enumerate(acts)}
        P = setup.poset
        start = [P.start_node[a.id] for a in acts]
        done = [P.done_node[a.id] for a in acts]

        # ---------------------------------------------------------- happens-before
        if linearization is None:
            n = len(P)
            reach = [0] * n
            for x in reversed(P.topological_order()):
                r = 0
                for y in P.succs[x]:
                    r |= (1 << y) | reach[y]
                reach[x] = r

            def hb(i: int, j: int) -> bool:
                return bool((reach[done[i]] >> start[j]) & 1)
        else:
            pos = P.positions(linearization)

            def hb(i: int, j: int) -> bool:
                return pos[done[i]] < pos[start[j]]

        predmask = [0] * m
        for j in range(m):
            pm = 0
            for i in range(m):
                if i != j and hb(i, j):
                    pm |= 1 << i
            predmask[j] = pm

        # ---------------------------------------------------------- static structure
        wmask = [0] * nb
        rmask = [0] * nb
        for i, a in enumerate(acts):
            if a.kind == "read":
                rmask[a.block] |= 1 << i
            else:
                wmask[a.block] |= 1 << i

        # deps[w]: reads whose values the content of write w depends on (transitively)
        deps_cache: dict[int, frozenset] = {}

        def deps(i: int) -> frozenset:
            if i in deps_cache:
                return deps_cache[i]
            a = acts[i]
            out: set[int] = set()
            if a.data is not None:
                for r in T.refs(a.data):
                    j = idx[r]
                    if acts[j].kind == "read":
                        out.add(j)
                    else:
                        out |= deps(j)
            res = frozenset(out)
            deps_cache[i] = res
            return res

        dependents: dict[int, int] = {}  # read index -> mask of writes depending on it
        for i, a in enumerate(acts):
            if a.kind != "read":
                for r in deps(i):
                    dependents[r] = dependents.get(r, 0) | (1 << i)
        refreads = sorted(dependents)
        refpos = {r: p for p, r in enumerate(refreads)}
        refdep = [dependents[r] for r in refreads]
        nref = len(refreads)

        # ---------------------------------------------------------- values
        I = _Interner()
        content_cache: dict = {}

        def ev(e, rv) -> int:
            if isinstance(e, T.Pair):
                return I.pair(ev(e.left, rv), ev(e.right, rv))
            if isinstance(e, T.Ref):
                j = idx[e.action]
                if acts[j].kind == "read":
                    return rv[refpos[j]]
                return content(j, rv)
            return I.term(e)

        def content(i: int, rv) -> int:
            key = (i, rv)
            c = content_cache.get(key)
            if c is None:
                a = acts[i]
                if a.data is None:
                    c = I.term(T.Unk(a.id))
                else:
                    c = ev(a.data, rv)
                content_cache[key] = c
            return c

        res: list[set[int]] = [set() for _ in range(m)]
        fin: list[set[int]] = [set() for _ in range(nb)]
        full = (1 << m) - 1

        def canon(S: int, C: list, RV: list) -> tuple:
            notS = full & ~S
            for b in range(nb):
                if not (wmask[b] & notS) and C[b] != DEAD:
                    fin[b].add(C[b])
                if not (rmask[b] & notS):
                    C[b] = DEAD
            for p in range(nref):
                if not (refdep[p] & notS):
                    RV[p] = DEAD
            return (S, tuple(C), tuple(RV))

        init_c = [I.term(t) for t in setup.init]
        s0 = canon(0, init_c, [DEAD] * nref)
        seen = {s0}
        stack = [s0]
        while stack:
            S, C, RV = stack.pop()
            notS = full & ~S
            rest = notS
            while rest:
                low = rest & -rest
                rest ^= low
                j = low.bit_length() - 1
                if predmask[j] & notS:
                    continue
                a = acts[j]
                nC = list(C)
                nRV = list(RV)
                if a.kind == "read":
                    v = C[a.block]
                    res[j].add(v)
                    p = refpos.get(j)
                    if p is not None:
                        nRV[p] = v
                else:
                    nC[a.block] = content(j, RV)
                st = canon(S | low, nC, nRV)
                if st not in seen:
                    seen.add(st)
                    stack.append(st)

        terms = I.terms
        results = {a.id: {terms[v] for v in res[i]} for i, a in enumerate(acts) if a.kind == "read"}
        final = {b: {terms[v] for v in fin[b]} for b in range(nb)}
        return Outcomes(mode, True, results, final)
