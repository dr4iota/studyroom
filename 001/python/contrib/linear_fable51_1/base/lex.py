"""``fable51-b-lex``: iterative lexicographic enumeration (multiset next-permutation).

Idea
----
The label sequence (which thread supplies the next node) is a permutation of the
multiset of thread labels. Starting from the sorted sequence ``0^m_0 1^m_1 ...``, the
classical *next permutation* step (Narayana Pandita) produces the lexicographically next
multiset permutation in place:

1. find the largest ``i`` with ``w[i] < w[i+1]`` (none: last permutation);
2. find the largest ``j > i`` with ``w[j] > w[i]``; swap ``w[i], w[j]``;
3. reverse the suffix ``w[i+1:]`` (it was non-increasing, now non-decreasing).

Node indices are kept in a parallel array; only the changed suffix is re-labelled with
the remaining nodes of each thread in chain order.

Order: lexicographic in thread labels (thread 0's nodes as early as possible first).
Time per output: ``O(n)`` worst case (the suffix scan/reversal plus building the output
tuple); the scan alone is ``O(1)`` amortized for balanced multiplicities.
Memory: ``O(n)`` beyond the output tuple. Non-recursive.
Not a Gray code (a step can move many nodes).
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import BASE, base_chains


def lex_interleavings(chains: list[list[int]]) -> Iterator[Linearization]:
    """Interleavings of ``chains`` in lexicographic order of the chain-label sequence."""
    labels = [t for t, c in enumerate(chains) for _ in c]
    n = len(labels)
    ids = [x for c in chains for x in c]
    sizes = [len(c) for c in chains]
    cnt = [0] * len(chains)
    yield tuple(ids)
    while True:
        i = n - 2
        while i >= 0 and labels[i] >= labels[i + 1]:
            i -= 1
        if i < 0:
            return
        j = n - 1
        while labels[j] <= labels[i]:
            j -= 1
        labels[i], labels[j] = labels[j], labels[i]
        labels[i + 1 :] = labels[: i : -1] if i + 1 < n else []
        # Re-label positions i.. with each thread's remaining nodes, in chain order.
        for k in range(i, n):
            cnt[labels[k]] += 1
        for k in range(i, n):
            t = labels[k]
            ids[k] = chains[t][sizes[t] - cnt[t]]
            cnt[t] -= 1
        yield tuple(ids)


@register
class FableLex(LinEnumerator):
    name = "fable51-b-lex"
    description = "iterative lexicographic multiset next-permutation over thread labels"
    capabilities = BASE

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return lex_interleavings(base_chains(setup))
