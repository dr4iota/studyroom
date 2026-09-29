"""``fable51-b-gray``: minimal-change order, consecutive outputs differ by <= 2 adjacent swaps.

Why not ``gray_code = True``
----------------------------
A one-adjacent-transposition Gray code does **not** exist for this problem in general.
Each adjacent transposition flips the inversion parity of the label sequence, so the
adjacent-transposition graph on ``Lin(P)`` is bipartite, and a Hamiltonian path needs
the two colour classes to differ by at most one. Their difference is the q-multinomial
coefficient at ``q = -1``; for ``examples/base.setup.yaml`` (two chains of 6) the 924
linearizations split 472 / 452, so no such path exists. The best general guarantee is
Pruesse–Ruskey's: consecutive linear extensions differ by one *or two* adjacent
transpositions. That is what this enumerator delivers (``gray_code`` stays False
because the API flag promises exactly one).

Idea
----
Steinhaus–Johnson–Trotter over threads. Let the threads be ``0..N-1`` with ``m_t``
nodes each. The linearizations of threads ``0..k`` are produced from those of ``0..k-1``
by sweeping thread ``k``'s ``m_k`` tokens across each inner arrangement, alternately
forwards and backwards, so the inner arrangement changes only while the tokens are
*parked* at one end. A sweep is a Hamiltonian path over the ``C(s+m, m)`` placements of
the tokens (a binary string with ``s`` zeros = inner elements, ``t = m`` ones = tokens)
in which consecutive strings differ by <= 2 adjacent transpositions and whose two ends
have all zeros contiguous, so an inner change (itself <= 2 adjacent transpositions of
contiguous elements) is the same <= 2 transpositions of the whole sequence. The sweep is
the mutually recursive pair (``^R`` = reversed list, ``x·L`` = prefix every string)::

    C(s,t) = 1·C(s,t-1)^R , 0·D(s-1,t)       C(0,t) = [1^t]   C(s,0) = [0^s]
    D(s,t) = 1·C(s,t-1)   , 0·C(s-1,t)       D likewise

By induction ``C(s,t)`` starts at ``1 0^s 1^(t-1)`` and ends at ``0^s 1^t``, ``D(s,t)``
starts at ``1 1 0^s 1^(t-2)`` (``1 0^s`` for ``t = 1``) and ends at ``0^s 1^t``; the
junction inside ``C`` is ``1 1 0 ... -> 0 1 1 ...`` (two adjacent transpositions;
``1 0 -> 0 1`` when ``t = 1``) and inside ``D`` it is ``1 0 ... -> 0 1 ...`` (one).
Both lists are Hamiltonian because they split on the first bit.

Everything runs in place on one label array; each level is a generator that performs
its own swaps and yields once per transition. A level's window moves by one position
depending on where the enclosing level parked its tokens, so every level reads its
current window offset from a shared cell before touching the array.

Time per output: ``O(1)`` swaps plus ``O(n)`` to materialize the tuple (generator
delegation adds ``O(depth)``, depth <= N + n). Memory: ``O(n)`` array plus ``O(n)``
suspended generator frames. Deterministic.
Order: consecutive outputs differ by one or two adjacent transpositions (verified in
the tests); the first output is the arrangement where each thread ``k`` has one node
before and ``m_k - 1`` nodes after the threads ``< k``.
"""

from __future__ import annotations

from typing import Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

from .common import BASE, base_chains


def gray_interleavings(chains: list[list[int]]) -> Iterator[Linearization]:
    """Interleavings of ``chains``; consecutive outputs differ by <= 2 adjacent swaps."""
    labels = [t for t, c in enumerate(chains) if c]  # skip empty chains
    mult = [len(chains[t]) for t in labels]
    n = sum(mult)
    N = len(labels)
    # prefix sizes: size[k] = number of elements of levels 0..k-1
    size = [0] * (N + 1)
    for k in range(N):
        size[k + 1] = size[k] + mult[k]
    w = [0] * n  # label array; w[p] = index into `labels`
    bases = [0] * (N + 1)  # bases[k] = current offset of level k's window in w

    def init(k: int, base: int) -> None:
        # Level k's tokens start at 1 0^s 1^(t-1): one token first, the rest last.
        if k == 0:
            return
        m, s = mult[k - 1], size[k - 1]
        w[base] = k - 1
        for p in range(base + 1 + s, base + s + m):
            w[p] = k - 1
        init(k - 1, base + 1)

    init(N, 0)

    def swap(cell: int, a: int, b: int) -> None:
        off = bases[cell]
        w[off + a], w[off + b] = w[off + b], w[off + a]

    def genC(s: int, t: int, rel: int, cell: int, rev: bool) -> Iterator[None]:
        """Transitions of C(s,t) (or its reverse) on window positions rel..rel+s+t-1."""
        if s == 0 or t == 0:
            return
        if not rev:
            yield from genC(s, t - 1, rel + 1, cell, True)
            if t >= 2:
                swap(cell, rel + 1, rel + 2)
            swap(cell, rel, rel + 1)
            yield
            yield from genD(s - 1, t, rel + 1, cell, False)
        else:
            yield from genD(s - 1, t, rel + 1, cell, True)
            swap(cell, rel, rel + 1)
            if t >= 2:
                swap(cell, rel + 1, rel + 2)
            yield
            yield from genC(s, t - 1, rel + 1, cell, False)

    def genD(s: int, t: int, rel: int, cell: int, rev: bool) -> Iterator[None]:
        """Transitions of D(s,t) (or its reverse) on window positions rel..rel+s+t-1."""
        if s == 0 or t == 0:
            return
        if not rev:
            yield from genC(s, t - 1, rel + 1, cell, False)
            swap(cell, rel, rel + 1)
            yield
            yield from genC(s - 1, t, rel + 1, cell, False)
        else:
            yield from genC(s - 1, t, rel + 1, cell, True)
            swap(cell, rel, rel + 1)
            yield
            yield from genC(s, t - 1, rel + 1, cell, True)

    def level(k: int) -> Iterator[None]:
        """Transitions of the arrangement of levels 0..k-1 inside window bases[k]."""
        if k == 0:
            return
        m, s = mult[k - 1], size[k - 1]
        inner = level(k - 1)
        forward = True
        while True:
            yield from genC(s, m, 0, k, not forward)
            forward = not forward
            # Parked at 0^s 1^m after a forward sweep (inner window at the same offset),
            # at 1 0^s 1^(m-1) after a backward one (inner window shifted by one).
            bases[k - 1] = bases[k] + (0 if not forward else 1)
            try:
                next(inner)
            except StopIteration:
                return
            yield

    occ = [0] * len(chains)

    def emit() -> Linearization:
        for t in labels:
            occ[t] = 0
        out = []
        for x in w:
            t = labels[x]
            out.append(chains[t][occ[t]])
            occ[t] += 1
        return tuple(out)

    yield emit()
    for _ in level(N):
        yield emit()


def combination_list(s: int, t: int, family: str = "C") -> list[tuple[int, ...]]:
    """The lists C(s,t) / D(s,t) of the docstring, materialized (for tests and study)."""
    if s == 0:
        return [(1,) * t]
    if t == 0:
        return [(0,) * s]
    if family == "C":
        first = [(1,) + x for x in reversed(combination_list(s, t - 1, "C"))]
        second = [(0,) + x for x in combination_list(s - 1, t, "D")]
    else:
        first = [(1,) + x for x in combination_list(s, t - 1, "C")]
        second = [(0,) + x for x in combination_list(s - 1, t, "C")]
    return first + second


@register
class FableGray(LinEnumerator):
    name = "fable51-b-gray"
    description = "SJT over threads: consecutive outputs differ by one or two adjacent transpositions"
    capabilities = BASE
    gray_code = False  # one *or two* adjacent transpositions; exactly one is impossible in general

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return gray_interleavings(base_chains(setup))
