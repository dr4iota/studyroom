"""Reference enumerator: backtracking over minimal elements (Varol–Rotem style).

Repeatedly choose any node whose predecessors are all placed. Simple and obviously
correct; ``O(n)`` work per step of the search, no constant-amortized-time guarantee.
"""

from __future__ import annotations

from typing import Iterator

from ..capabilities import Capabilities
from ..model import Setup
from ..poset import Linearization
from ..registry import register
from .api import LinEnumerator


def linear_extensions(setup: Setup) -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    indeg = [len(p) for p in P.preds]
    avail = sorted(x for x in range(n) if indeg[x] == 0)
    order: list[int] = []

    def rec() -> Iterator[Linearization]:
        if len(order) == n:
            yield tuple(order)
            return
        for x in list(avail):
            avail.remove(x)
            order.append(x)
            freed = []
            for y in P.succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    freed.append(y)
            avail.extend(freed)
            yield from rec()
            for y in freed:
                avail.remove(y)
            for y in P.succs[x]:
                indeg[y] += 1
            order.pop()
            avail.append(x)
            avail.sort()

    yield from rec()


@register
class Backtrack(LinEnumerator):
    name = "backtrack"
    description = "reference: recursive choice of a minimal element"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=False)

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return linear_extensions(setup)
