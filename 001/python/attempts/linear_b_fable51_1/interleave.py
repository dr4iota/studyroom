"""Case b: no sync points, no observations.

With ``K = 0`` the trace poset is a disjoint union of chains, one per thread (the
program order of that thread's start/done steps), and ``Lin(P)`` is exactly the set of
interleavings of those chains.  Write data never adds order (a referenced read always
completes earlier in program order), so ``LinFeas(P) = Lin(P)``.

An interleaving is determined by the *word* of chain labels it reads off (position
``p`` holds the ``c``-th node of chain ``w[p]`` where ``c`` is the number of earlier
occurrences of ``w[p]``).  The enumerator walks these words in lexicographic order with
the classic "next multiset permutation" step, and rebuilds only the changed suffix of the
node tuple.  The counter returns the multinomial coefficient.
"""

from __future__ import annotations

import math
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

CAPS = Capabilities(rcw=False, sync=False, observed_reads=False)


def _chains(setup: Setup) -> list[list[int]]:
    """The non-empty chains of the poset (thread chains; no sync nodes in case b)."""
    return [list(c) for c in setup.poset.chains if c]


@register
class InterleaveEnumerator(LinEnumerator):
    name = "fable51_1-b-interleave"
    description = "Interleavings of the thread chains, in lexicographic order of the chain-label word"
    capabilities = CAPS
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        chains = _chains(setup)
        k = len(chains)
        lens = [len(c) for c in chains]
        n = sum(lens)

        # First word: all labels of chain 0, then chain 1, ...  (lexicographically least).
        word: list[int] = []
        out: list[int] = []
        for ci, c in enumerate(chains):
            word.extend([ci] * len(c))
            out.extend(c)
        yield tuple(out)  # for n == 0 this is the single empty linearization
        if n == 0 or k <= 1:
            return

        while True:
            # Scan the non-increasing suffix from the right, counting its labels.
            rem = [0] * k  # rem[c] = occurrences of label c in word[i:]
            i = n - 1
            rem[word[i]] += 1
            while i > 0 and word[i - 1] >= word[i]:
                i -= 1
                rem[word[i]] += 1
            if i == 0:
                return  # word is non-increasing everywhere: last permutation
            i -= 1  # now word[i] < word[i + 1]
            wi = word[i]
            rem[wi] += 1  # rem now counts word[i:]

            # Smallest label > word[i] present in the suffix moves to position i.
            c2 = wi + 1
            while rem[c2] == 0:
                c2 += 1
            word[i] = c2
            rem[c2] -= 1  # rem now counts the new word[i + 1:]

            # Node at i: chain c2 had lens[c2] - rem[c2] - 1 nodes before position i.
            tail = [chains[c2][lens[c2] - rem[c2] - 1]]
            tail_word: list[int] = []
            # The new suffix word[i + 1:] is the ascending arrangement of rem, so the
            # nodes are each chain's remaining nodes, chains in ascending order.
            for c in range(k):
                r = rem[c]
                if r:
                    tail_word.extend([c] * r)
                    tail.extend(chains[c][lens[c] - r:])
            word[i + 1:] = tail_word
            out[i:] = tail
            yield tuple(out)


@register
class MultinomialCounter(LinCounter):
    name = "fable51_1-b-multinomial"
    description = "|Lin(P)| as the multinomial coefficient of the thread chain lengths"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        total = 0
        result = 1
        for c in _chains(setup):
            total += len(c)
            result *= math.comb(total, len(c))
        return CountResult(linearizations=result, method="multinomial")
