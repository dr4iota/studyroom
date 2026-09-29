"""``fable51-b-unrank``: ranked enumeration by multinomial unranking, and ``fable51-b-count``.

Idea
----
Index ``Lin(P)`` by rank in lexicographic order of the label sequence. The number of
label sequences with multiplicities ``c`` is the multinomial ``M(c) = n! / prod c_t!``,
and the sequences starting with label ``t`` number ``M(c) * c_t / n``. Unranking walks
the ``n`` positions, at each one skipping over the labels whose block of sequences lies
before the rank (``O(N)`` big-integer operations per position). Every output is computed
independently from its rank, so the enumeration can start anywhere, stop anywhere and
stride (``--opt start=... --opt stop=... --opt step=...``): the natural way to split a huge
``Lin(P)`` across processes or to resume. ``rank`` is the inverse (used by the tests).

Order: lexicographic in thread labels (same as ``fable51-b-lex``).
Time per output: ``O(n * N)`` arithmetic operations on integers of ``O(n log n)`` bits.
Memory: ``O(n + N)``. Non-recursive.
Not a Gray code.

``fable51-b-count`` is the trivial exact counter for this case: the multinomial coefficient
of the chain lengths.
"""

from __future__ import annotations

from typing import Iterator, Sequence

from abio.lin.api import CountResult, LinCounter, LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import BASE, base_chains, labels_to_nodes, multinomial


def unrank(rank: int, counts: Sequence[int]) -> list[int]:
    """The label sequence of lexicographic rank ``rank`` (``0 <= rank < M(counts)``)."""
    c = list(counts)
    n = sum(c)
    total = multinomial(c)
    if not 0 <= rank < total:
        raise ValueError(f"rank {rank} out of range [0, {total})")
    out = []
    for _ in range(n):
        for t in range(len(c)):
            if c[t] == 0:
                continue
            block = total * c[t] // n  # sequences with the remaining multiset starting with t
            if rank < block:
                out.append(t)
                total = block
                c[t] -= 1
                n -= 1
                break
            rank -= block
        else:  # pragma: no cover - unreachable when rank is in range
            raise AssertionError("unrank ran out of labels")
    return out


def rank(labels: Sequence[int], counts: Sequence[int]) -> int:
    """Lexicographic rank of ``labels`` among the permutations of the multiset ``counts``."""
    c = list(counts)
    n = sum(c)
    total = multinomial(c)
    r = 0
    for x in labels:
        for t in range(x):
            if c[t]:
                r += total * c[t] // n
        total = total * c[x] // n
        c[x] -= 1
        n -= 1
    return r


def ranked_interleavings(chains: list[list[int]], start: int = 0, stop: int | None = None,
                         step: int = 1) -> Iterator[Linearization]:
    counts = [len(c) for c in chains]
    total = multinomial(counts)
    if stop is None or stop > total:
        stop = total
    if step <= 0:
        raise ValueError("step must be positive")
    for r in range(max(start, 0), stop, step):
        yield labels_to_nodes(unrank(r, counts), chains)


@register
class FableUnrank(LinEnumerator):
    name = "fable51-b-unrank"
    description = "ranked lexicographic enumeration by multinomial unranking (start/stop/step)"
    capabilities = BASE
    options = {"start": "first rank to output (default 0)",
               "stop": "one past the last rank (default |Lin(P)|)",
               "step": "rank stride (default 1)"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        o = self.opts
        return ranked_interleavings(base_chains(setup), int(o.get("start", 0)),
                                    None if o.get("stop") is None else int(o["stop"]),
                                    int(o.get("step", 1)))


@register
class FableCount(LinCounter):
    name = "fable51-b-count"
    description = "exact count: multinomial coefficient of the thread chain lengths"
    capabilities = BASE

    def count(self, setup: Setup) -> CountResult:
        return CountResult(multinomial([len(c) for c in base_chains(setup)]), None, "multinomial")
