"""``fable51-s-vr``: Varol–Rotem iterative enumeration by left shifts (Knuth, TAOCP 7.2.1.2, Alg. V).

Reference: Y. L. Varol and D. Rotem, *An algorithm to generate all topological sorting
arrangements*, Comput. J. 24 (1981) 83–84.

Idea
----
Number the nodes ``0..n-1`` by a topological order, so ``x ≺ y`` implies
``label(x) < label(y)`` and the identity is a linear extension. Keep the current
extension ``a[1..n]`` (``a[0]`` is a sentinel that blocks everything) and the position
of every label. Repeatedly try to move the largest label ``k = n-1`` one step left: the
move is legal iff the label ``y`` immediately to its left is not a predecessor of ``k``
(looked up in the transitive closure; since ``y < k`` the only possible relation is
``y ≺ k``). Each successful move is a new extension. When ``k`` cannot move, shift it
back to its home position ``k+1`` (right of every smaller label) and continue with
``k-1``; after any successful move restart with ``k = n-1``. Invariant: when label
``k`` is being tried, labels ``> k`` sit at their homes ``k+2..n`` and labels ``< k``
occupy the other positions in a valid relative order, so every visited arrangement is
an extension, and each one is visited once (the sequence of positions is an
odometer over the "left-shift counts" of the labels).

Sync needs nothing special: sync nodes and ``before``/``after`` edges are just more
relations in the closure.

Cost
----
Every successful shift produces one output; restoring ``k`` costs as many swaps as it
made going left, so swaps are ``O(1)`` amortized per output. The failing tests after an
output (``k = n-1, n-2, ...`` until one moves) are ``O(n)`` in the worst case, so the
per-output bound is ``O(n)`` worst case, ``O(1)`` amortized on most inputs, plus
``O(n)`` to materialise the tuple. Memory ``O(n)`` plus the ``O(n^2)``-bit closure.
Iterative (no recursion), deterministic, lazy. No adjacency property is claimed: a
restore step moves one node over several positions.
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization, TracePoset
from abio.registry import register

from .common import SYNC, closure_above, relabel_closure, topo_labels


def linear_extensions(P: TracePoset) -> Iterator[Linearization]:
    n = len(P)
    if n == 0:
        yield ()
        return
    nodes, label_of = topo_labels(P)
    up = relabel_closure(closure_above(P, nodes), nodes, label_of)
    # below[l] = bitmask of labels that must precede label l
    below = [0] * n
    for l in range(n):
        bits = up[l]
        while bits:
            low = bits & -bits
            below[low.bit_length() - 1] |= 1 << l
            bits ^= low
    a = [-1] + list(range(n))  # a[0] sentinel
    pos = list(range(1, n + 1))  # pos[label] = index in a
    cur = list(nodes)  # cur[j-1] = node at position j
    yield tuple(cur)
    k = n - 1
    while True:
        j = pos[k]
        y = a[j - 1]
        if y >= 0 and not (below[k] >> y) & 1:
            a[j - 1], a[j] = k, y
            pos[k], pos[y] = j - 1, j
            cur[j - 2], cur[j - 1] = cur[j - 1], cur[j - 2]
            yield tuple(cur)
            k = n - 1
            continue
        # restore k to its home position k+1 (right of every smaller label)
        home = k + 1
        while j < home:
            y = a[j + 1]
            a[j], a[j + 1] = y, k
            pos[y] = j
            cur[j - 1], cur[j] = cur[j], cur[j - 1]
            j += 1
        pos[k] = home
        k -= 1
        if k < 0:
            return


@register
class FableSyncVR(LinEnumerator):
    name = "fable51-s-vr"
    description = "Varol-Rotem left shifts (Knuth Alg. V), iterative, O(n) worst case per output"
    capabilities = SYNC

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return linear_extensions(setup.poset)
