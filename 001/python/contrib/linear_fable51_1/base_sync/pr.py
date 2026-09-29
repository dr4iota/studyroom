"""``fable51-s-pr``: Pruesse–Ruskey Gray code, one **or two** adjacent transpositions per step.

Reference: G. Pruesse and F. Ruskey, *Generating linear extensions fast*, SIAM J.
Comput. 23 (1994) 373–386; the presentation follows F. Ruskey, *Combinatorial
Generation* (draft, 2001), §5.10, Algorithms 5.22 (PreProcess) and 5.23 (GenLE).

Idea
----
Preprocessing strips the poset from the bottom: while it has a unique minimal element,
that element is fixed; otherwise two minimal elements are removed as the pair
``(a_i, b_i)``. This gives the initial extension ``le`` and ``MaxPair`` pairs. The
recursive ``GenLE(i)`` walks pair ``i`` rightwards through the elements after it (``b_i``
row by row, ``a_i`` sweeping right and back in each row) and calls ``GenLE(i-1)`` after
every move, so that the inner pairs move only while the outer pairs stand still. A
*sign* bit (``Switch(0)``) doubles the list: the walk is a Hamiltonian path in the
prism ``G(P) x K2`` of the adjacent-transposition graph, every step being one
transposition or a sign flip, and each extension is visited once with each sign.
Because the prism is bipartite, taking **every other** signed extension yields every
extension of ``P`` exactly once, and consecutive outputs are then at distance one or
two in the transposition graph (Ruskey, Lemma 5.11 / Theorem 5.8).

Handling of sync: nothing special. ``sync.k`` nodes are ordinary poset elements, and
``before``/``after`` edges are ordinary cover relations; comparability is looked up in
the transitive closure (a bitmask per node).

Cost
----
Constant amortized time per signed extension (each ``GenLE(i)`` call performs at least
one move, every move produces one signed extension; Ruskey Thm 5.7), hence ``O(1)``
amortized per output plus ``O(n)`` to materialise the tuple. In this Python version the
recursion is a chain of generators of depth ``MaxPair <= n/2``, so each yield costs
``O(depth)`` frame resumptions. Memory: ``O(n)`` arrays plus the ``O(n^2)``-bit closure.
Deterministic: pairs are the two smallest available node indices.

Property (tested): consecutive outputs differ by exactly one or two adjacent
transpositions ("delay 2"); ``gray_code`` stays False because the API flag promises
exactly one.
"""

from __future__ import annotations

import heapq
from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization, TracePoset
from abio.registry import register

from .common import SYNC, closure_above


def preprocess(P: TracePoset) -> tuple[list[int], list[int], list[int]]:
    """Ruskey Algorithm 5.22: ``(le, a, b)`` with ``a[i]``/``b[i]`` the ``i``-th pair (1-based).

    Minimal elements are taken smallest node index first, so the result is deterministic.
    """
    n = len(P)
    indeg = [len(p) for p in P.preds]
    heap = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(heap)
    le: list[int] = []
    a: list[int] = [-1]
    b: list[int] = [-1]

    def remove(x: int) -> None:
        le.append(x)
        for y in P.succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(heap, y)

    while heap:
        if len(heap) == 1:
            remove(heapq.heappop(heap))
        else:
            x = heapq.heappop(heap)
            y = heapq.heappop(heap)
            a.append(x)
            b.append(y)
            remove(x)
            remove(y)
    if len(le) != n:
        raise ValueError("poset has a cycle")
    return le, a, b


def linear_extensions(P: TracePoset) -> Iterator[Linearization]:
    """Every linear extension of ``P`` once; consecutive ones differ by 1 or 2 adjacent swaps."""
    n = len(P)
    if n == 0:
        yield ()
        return
    above = closure_above(P)
    le, a, b = preprocess(P)
    li = [0] * n  # inverse of le
    for j, x in enumerate(le):
        li[x] = j
    maxpair = len(a) - 1

    def right_b(i: int) -> bool:
        x = b[i]
        j = li[x] + 1
        return j < n and not (above[x] >> le[j]) & 1

    def right_a(i: int) -> bool:
        x = a[i]
        j = li[x] + 1
        if j >= n:
            return False
        y = le[j]
        return y != b[i] and not (above[x] >> y) & 1

    def move(x: int, d: int) -> None:
        j = li[x]
        k = j + d
        y = le[k]
        le[j], le[k] = y, x
        li[x], li[y] = k, j

    def switch(i: int) -> bool:
        """Transpose the (adjacent) pair ``i``; ``i == 0`` is the sign flip. Returns True if the array changed."""
        if i == 0:
            return False
        x, y = a[i], b[i]
        j, k = li[x], li[y]
        le[j], le[k] = y, x
        li[x], li[y] = k, j
        a[i], b[i] = y, x  # a[i] stays the leftmost of the pair
        return True

    def gen(i: int) -> Iterator[bool]:
        if i == 0:
            return
        yield from gen(i - 1)
        mrb = 0
        typical = False
        while right_b(i):
            mrb += 1
            move(b[i], 1)
            yield True
            yield from gen(i - 1)
            mra = 0
            if right_a(i):
                typical = True
                while True:
                    mra += 1
                    move(a[i], 1)
                    yield True
                    yield from gen(i - 1)
                    if not right_a(i):
                        break
            if typical:
                yield switch(i - 1)
                yield from gen(i - 1)
                mla = mra - 1 if mrb & 1 else mra + 1
                for _ in range(mla):
                    move(a[i], -1)
                    yield True
                    yield from gen(i - 1)
        if typical and mrb & 1:
            move(a[i], -1)
            yield True
        else:
            yield switch(i - 1)
        yield from gen(i - 1)
        for _ in range(mrb):
            move(b[i], -1)
            yield True
            yield from gen(i - 1)

    def walk() -> Iterator[bool]:
        # Calling sequence GenLE(MaxPair); Switch(MaxPair); GenLE(MaxPair).
        yield from gen(maxpair)
        yield switch(maxpair)
        yield from gen(maxpair)

    # Signed list l_1, l_2, ...; output l_1, l_3, l_5, ... (Ruskey Theorem 5.8).
    yield tuple(le)
    odd = False
    for _ in walk():
        odd = not odd
        if not odd:
            yield tuple(le)


@register
class FableSyncPR(LinEnumerator):
    name = "fable51-s-pr"
    description = "Pruesse-Ruskey: consecutive outputs differ by 1 or 2 adjacent swaps; CAT"
    capabilities = SYNC
    gray_code = False  # the flag promises exactly one transposition; this delivers one or two

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return linear_extensions(setup.poset)
