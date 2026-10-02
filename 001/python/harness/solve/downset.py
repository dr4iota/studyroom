"""Exact solver by search over down-sets of the action order (harness reference).

Every effect order admissible for some linearization of ``P`` is a linear extension of
the action order ``a ≺ b ⟺ end(a) <_P start(b)``, and conversely. In mode ``fixed``, it
is ``pos_L(end(a)) < pos_L(start(b))``. So ``Poss`` is computed over linear extensions
of ``≺`` alone, with no enumeration of linearizations. The state after a set of effects
is:
- the executed set (a down-set of ``≺``);
- the block contents;
- the results of executed reads that some unexecuted write or RCW still refers to.

Distinct paths reaching the same state are merged.

With observations, a value counts only on an edge into a state from which a complete,
consistent execution exists. A memoised ``completable`` check marks those states.

This is the harness's oracle for setups too large for ``brute`` (e.g. unrolled loops).
It is validated against ``brute`` in ``tests/test_downset.py``. Exponential in the width
of ``≺`` in the worst case.
"""

from __future__ import annotations

import sys
from functools import lru_cache

from .. import terms as T
from ..model import Setup
from ..poset import Linearization
from ..registry import register
from .api import Outcomes, Solver, SolverCapabilities


def _reach(setup: Setup) -> list[int]:
    """reach[x] = bitmask of nodes reachable from node x (strictly after it) in P."""
    P = setup.poset
    order = P.topological_order()
    reach = [0] * len(P)
    for x in reversed(order):
        m = 0
        for y in P.succs[x]:
            m |= (1 << y) | reach[y]
        reach[x] = m
    return reach


def solve_downset(setup: Setup, linearization: Linearization | None = None) -> Outcomes:
    P = setup.poset
    acts = list(setup.actions.values())
    n = len(acts)
    idx = {a.id: i for i, a in enumerate(acts)}
    if linearization is None:
        reach = _reach(setup)
        before = lambda a, b: bool(reach[P.done_node[a.id]] >> P.start_node[b.id] & 1)  # noqa: E731
    else:
        pos = P.positions(linearization)
        before = lambda a, b: pos[P.done_node[a.id]] < pos[P.start_node[b.id]]  # noqa: E731
    pred = [0] * n
    for j, b in enumerate(acts):
        for i, a in enumerate(acts):
            if i != j and before(a, b):
                pred[j] |= 1 << i

    # reads each write/RCW needs (transitively, through references to other writes)
    def needs(aid: str, seen: frozenset = frozenset()) -> frozenset:
        a = setup.actions[aid]
        out = set()
        for e in (a.data, a.expect):
            if e is None:
                continue
            for r in T.refs(e):
                b = setup.actions[r]
                if b.kind == "read":
                    out.add(r)
                elif r not in seen:
                    out |= needs(r, seen | {aid})
        return frozenset(out)

    need = {a.id: needs(a.id) for a in acts if a.writes}
    full = (1 << n) - 1
    flag = setup.semantics.rcw_result == "flag"

    def live_reads(mask: int) -> frozenset:
        out = set()
        for a in acts:
            if a.writes and not mask >> idx[a.id] & 1:
                out |= need[a.id]
        return frozenset(out)

    def value_of(rv: dict, aid: str) -> T.Term:
        a = setup.actions[aid]
        if a.kind == "read":
            return rv[aid]
        return T.Unk(aid) if a.data is None else T.substitute(a.data, lambda r: value_of(rv, r))

    def step(state, i):
        """Apply action i; return (result or None, new state) or None if inconsistent."""
        mask, content, rvals = state
        a = acts[i]
        rv = dict(rvals)
        content = list(content)
        b = a.block
        old = content[b]
        result = None
        if a.kind == "read":
            result = old
            if a.observed is not None and a.observed != old:
                return None
            rv[a.id] = old
        elif a.kind == "write":
            content[b] = value_of(rv, a.id)
        else:
            result = old
            success = old == T.substitute(a.expect, lambda r: value_of(rv, r))
            if success:
                content[b] = value_of(rv, a.id)
            if a.observed is not None:
                if (a.observed != ("ok" if success else "fail")) if flag else (a.observed != old):
                    return None
        mask |= 1 << i
        live = live_reads(mask)
        rvals = tuple(sorted(((k, v) for k, v in rv.items() if k in live), key=lambda kv: kv[0]))
        return result, (mask, tuple(content), rvals)

    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10 * n + 1000))
    results: dict[str, set] = {a.id: set() for a in acts if a.returns}
    final: dict[int, set] = {b: set() for b in range(setup.blocks)}

    @lru_cache(maxsize=None)
    def completable(state) -> bool:
        mask, content, _ = state
        if mask == full:
            for b, v in enumerate(content):
                final[b].add(v)
            return True
        ok = False
        for i in range(n):
            if not mask >> i & 1 and pred[i] & ~mask == 0:
                nxt = step(state, i)
                if nxt is None:
                    continue
                res, child = nxt
                if completable(child):
                    ok = True
                    if res is not None:
                        results[acts[i].id].add(res)
        return ok

    start = (0, tuple(setup.init), ())
    consistent = completable(start)
    completable.cache_clear()
    mode = "fixed" if linearization is not None else "all"
    if not consistent:
        return Outcomes(mode, False)
    return Outcomes(mode, True, results, final)


@register
class DownsetSolver(Solver):
    name = "downset"
    description = "reference: search over down-sets of the action order, merged states"
    capabilities = SolverCapabilities(rcw=True, sync=True, observed_reads=True,
                                      modes=frozenset({"all", "fixed"}), witnesses=False)

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        return solve_downset(setup, linearization)
