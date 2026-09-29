"""Enumerator of ``Lin(P)`` for case ``s`` (sync points, no observations).

With no observed reads ``LinFeas(P) = Lin(P)``, so this lists every linear extension of
the trace poset ``setup.poset`` exactly once.

Method: the Varol–Rotem algorithm (Knuth's Algorithm V).  Nodes are relabelled so that a
fixed topological order is the identity; starting from it, the largest label is moved
left by adjacent swaps while the element to its left is not a predecessor.  When it can
move no further it is put back at its home position and the next smaller label is moved
one step, after which the larger labels start over.  Every move produces a new,
distinct linear extension, so each output costs one swap plus the ``tuple`` copy.

Only *direct* predecessors need to be checked: the array is always a linear extension,
and a transitive predecessor of an adjacent element must be a direct one (any
intermediate element of the chain would have to sit between the two).
"""

from __future__ import annotations

import heapq
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization, TracePoset
from harness.registry import register


def topological_order(poset: TracePoset) -> list[int]:
    """Deterministic topological order: Kahn's algorithm, smallest ready index first."""
    n = len(poset)
    indeg = [len(p) for p in poset.preds]
    ready = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(ready)
    out: list[int] = []
    succs = poset.succs
    while ready:
        x = heapq.heappop(ready)
        out.append(x)
        for y in succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(ready, y)
    return out


@register
class VarolRotemEnumerator(LinEnumerator):
    name = "fable51_1-s-varol-rotem"
    description = "Varol-Rotem enumeration of Lin(P): adjacent left moves from a topological order"
    capabilities = Capabilities(rcw=False, sync=True, observed_reads=False)
    gray_code = False  # a "put back" step can shift several elements between two outputs

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        poset = setup.poset
        n = len(poset)
        if n == 0:
            yield ()
            return

        order = topological_order(poset)  # rank -> node; identity is a linearization
        # blocked[v][u] == 1 iff u is a direct predecessor of v (u may not pass v).
        blocked = [bytearray(n) for _ in range(n)]
        preds = poset.preds
        for v in range(n):
            row = blocked[v]
            for u in preds[v]:
                row[u] = 1

        a = list(order)  # a[position] = node
        pos = [0] * n  # pos[node] = position
        for i, v in enumerate(order):
            pos[v] = i

        yield tuple(a)

        last = n - 1
        k = last  # rank of the element being moved; its home position is k
        while True:
            v = order[k]
            j = pos[v]
            if j > 0:
                left = a[j - 1]
                if not blocked[v][left]:
                    # Move v one step left: a new linear extension.
                    a[j - 1] = v
                    a[j] = left
                    pos[v] = j - 1
                    pos[left] = j
                    yield tuple(a)
                    k = last
                    continue
            # v cannot move further: put it back at its home position k, shifting the
            # elements it had passed one step left, then move on to the next rank.
            while j < k:
                left = a[j + 1]
                a[j] = left
                pos[left] = j
                j += 1
            a[k] = v
            pos[v] = k
            k -= 1
            if k < 0:
                return
