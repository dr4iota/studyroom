"""Exact possibility-set solver for case `so` (sync points + observed reads).

Idea: a full schedule (L, pi) only matters through its effect order (the order of the
effect points). Over all linearizations of P, an effect order sigma is realizable iff it
is a linear extension of the relation  a -> b  iff  end(a) <_P start(b).  For one fixed
L, the relation is  a -> b  iff  pos_L(end(a)) < pos_L(start(b)).  We explore all such
effect orders by a memoized DFS over states (executed set, block contents, live read
values needed by pending writes), pruning on observed reads.
"""

from __future__ import annotations

import sys

from harness import terms as T
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


def _reach_masks(poset) -> list[int]:
    """reach[u]: bitmask of nodes v with u < v (strictly) in P."""
    n = len(poset)
    order = poset.topological_order()
    reach = [0] * n
    for u in reversed(order):
        m = 0
        for v in poset.succs[u]:
            m |= (1 << v) | reach[v]
        reach[u] = m
    return reach


@register
class ExactSolver(Solver):
    name = "opus55_1-so-exact"
    description = "Memoized DFS over realizable effect orders with observation pruning (exact Poss, all/fixed)."
    capabilities = SolverCapabilities(
        rcw=False, sync=True, observed_reads=True, modes=frozenset({"all", "fixed"}), witnesses=False
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        poset = setup.poset
        acts = list(setup.actions.values())
        na = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        sn = [poset.start_node[a.id] for a in acts]
        dn = [poset.done_node[a.id] for a in acts]

        # precedence: pred[i] = mask of actions j that must take effect before i
        pred = [0] * na
        if linearization is None:
            reach = _reach_masks(poset)
            for i in range(na):
                for j in range(na):
                    if i != j and (reach[dn[j]] >> sn[i]) & 1:
                        pred[i] |= 1 << j
        else:
            pos = poset.positions(linearization)
            for i in range(na):
                for j in range(na):
                    if i != j and pos[dn[j]] < pos[sn[i]]:
                        pred[i] |= 1 << j

        is_read = [a.kind == "read" for a in acts]
        blocks = [a.block for a in acts]
        observed = [a.observed for a in acts]

        # Transitive read dependencies of each write's content.
        def read_deps(aid: str, seen: set[str]) -> set[str]:
            a = setup.actions[aid]
            out: set[str] = set()
            if a.data is None:
                return out
            for r in T.refs(a.data):
                if r in seen:
                    continue
                seen.add(r)
                if setup.actions[r].kind == "read":
                    out.add(r)
                else:
                    out |= read_deps(r, seen)
            return out

        dependents = [0] * na  # for each read: mask of writes depending on it
        for i, a in enumerate(acts):
            if not is_read[i]:
                for r in read_deps(a.id, set()):
                    dependents[idx[r]] |= 1 << i
        needed = [i for i in range(na) if is_read[i] and dependents[i]]
        slot = {i: k for k, i in enumerate(needed)}

        static_cache: dict[str, T.Term] = {}

        def content(i: int, env: tuple) -> T.Term:
            a = acts[i]
            if a.data is None:
                return T.Unk(a.id)
            if not dependents_any_read[i]:
                c = static_cache.get(a.id)
                if c is None:
                    c = setup.static_content(a.id)
                    static_cache[a.id] = c
                return c

            def lookup(x: str) -> T.Term:
                j = idx[x]
                if is_read[j]:
                    v = env[slot[j]]
                    assert v is not None
                    return v
                return content(j, env)

            return T.substitute(a.data, lookup)

        dependents_any_read = [False] * na
        for i, a in enumerate(acts):
            if not is_read[i] and a.data is not None:
                dependents_any_read[i] = any((dependents[j] >> i) & 1 for j in needed)

        full = (1 << na) - 1
        results: dict[str, set] = {a.id: set() for a in acts if is_read[idx[a.id]]}
        final: dict[int, set] = {b: set() for b in range(setup.blocks)}
        memo: dict[tuple, bool] = {}

        old_limit = sys.getrecursionlimit()
        if old_limit < 10000:
            sys.setrecursionlimit(10000)

        def good(mask: int, cont: tuple, env: tuple) -> bool:
            key = (mask, cont, env)
            g = memo.get(key)
            if g is not None:
                return g
            if mask == full:
                for b, v in enumerate(cont):
                    final[b].add(v)
                memo[key] = True
                return True
            any_good = False
            for i in range(na):
                bit = 1 << i
                if mask & bit or (pred[i] & ~mask):
                    continue
                nmask = mask | bit
                b = blocks[i]
                if is_read[i]:
                    v = cont[b]
                    ob = observed[i]
                    if ob is not None and ob != v:
                        continue
                    ncont = cont
                    nenv = env
                    if i in slot:
                        l = list(env)
                        l[slot[i]] = v if dependents[i] & ~nmask else None
                        nenv = tuple(l)
                else:
                    c = content(i, env)
                    l = list(cont)
                    l[b] = c
                    ncont = tuple(l)
                    nenv = env
                    if needed:
                        el = list(env)
                        changed = False
                        for j in needed:
                            if (dependents[j] >> i) & 1 and el[slot[j]] is not None and not (dependents[j] & ~nmask):
                                el[slot[j]] = None
                                changed = True
                        if changed:
                            nenv = tuple(el)
                if good(nmask, ncont, nenv):
                    any_good = True
                    if is_read[i]:
                        results[acts[i].id].add(cont[b])
            memo[key] = any_good
            return any_good

        try:
            ok = good(0, tuple(setup.init), tuple([None] * len(needed)))
        finally:
            sys.setrecursionlimit(old_limit)

        if not ok:
            return Outcomes(mode, False)
        return Outcomes(mode, True, results, final)
