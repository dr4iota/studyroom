"""Exact counter of ``|Lin(P)|`` for case ``s`` (sync points, no observations).

1. Split the poset into connected components (of the comparability graph).  Linear
   extensions of a disjoint union are the shuffles of the components' extensions, so
   ``|Lin(P)| = prod_j C(s_1 + ... + s_j, s_j) * |Lin(C_j)|`` where ``s_j = |C_j|``.
   This makes threads that never touch a sync point cost nothing.
2. Count each component by dynamic programming over its order ideals (downsets),
   layered by ideal size.  The state is the progress along each chain of the
   component (the harness chain partition: one chain per thread, one singleton per
   sync node); the value is the number of linear extensions of that ideal.  An element
   is addable iff all its direct predecessors on other chains are already in the ideal.
"""

from __future__ import annotations

import math

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter
from harness.model import Setup
from harness.poset import TracePoset
from harness.registry import register


def _count_component(poset: TracePoset, chains: list[list[int]]) -> int:
    m = len(chains)
    lens = [len(c) for c in chains]
    loc: dict[int, tuple[int, int]] = {}
    for ci, c in enumerate(chains):
        for p, v in enumerate(c):
            loc[v] = (ci, p)
    # need[ci][p]: (chain, position) of each direct predecessor of chains[ci][p] that
    # lies on another chain (same-chain predecessors are implied by the progress).
    need = [
        [[loc[u] for u in poset.preds[v] if loc[u][0] != ci] for v in c]
        for ci, c in enumerate(chains)
    ]
    total = sum(lens)
    cur: dict[tuple[int, ...], int] = {(0,) * m: 1}
    rng = range(m)
    for _ in range(total):
        nxt: dict[tuple[int, ...], int] = {}
        get = nxt.get
        for st, cnt in cur.items():
            for ci in rng:
                p = st[ci]
                if p == lens[ci]:
                    continue
                for pc, pp in need[ci][p]:
                    if st[pc] <= pp:
                        break
                else:
                    lst = list(st)
                    lst[ci] = p + 1
                    key = tuple(lst)
                    nxt[key] = get(key, 0) + cnt
        cur = nxt
    return cur[tuple(lens)]


def count_linear_extensions(poset: TracePoset) -> int:
    n = len(poset)
    if n == 0:
        return 1
    comp = [-1] * n
    ncomp = 0
    for s in range(n):
        if comp[s] != -1:
            continue
        comp[s] = ncomp
        stack = [s]
        while stack:
            x = stack.pop()
            for y in poset.preds[x]:
                if comp[y] == -1:
                    comp[y] = ncomp
                    stack.append(y)
            for y in poset.succs[x]:
                if comp[y] == -1:
                    comp[y] = ncomp
                    stack.append(y)
        ncomp += 1

    # Every harness chain lies inside one component (consecutive thread steps are
    # linked directly or through a sync node), so group chains by component.
    comp_chains: list[list[list[int]]] = [[] for _ in range(ncomp)]
    for c in poset.chains:
        if c:
            comp_chains[comp[c[0]]].append(c)

    total = 1
    placed = 0
    for chains in comp_chains:
        size = sum(len(c) for c in chains)
        if size == 0:
            continue
        total *= math.comb(placed + size, size) * _count_component(poset, chains)
        placed += size
    return total


@register
class IdealDPCounter(LinCounter):
    name = "fable51_1-s-ideal-dp"
    description = "Exact |Lin(P)|: components merged by binomials, each counted by DP over order ideals"
    capabilities = Capabilities(rcw=False, sync=True, observed_reads=False)

    def count(self, setup: Setup) -> CountResult:
        return CountResult(linearizations=count_linear_extensions(setup.poset), method="ideal-dp")
