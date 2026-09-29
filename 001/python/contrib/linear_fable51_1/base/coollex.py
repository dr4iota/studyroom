"""``fable51-b-coollex``: loopless cool-lex enumeration by prefix shifts (Williams 2009).

Idea
----
A. Williams, *Loopless generation of multiset permutations using a constant number of
variables by prefix shifts* (SODA 2009). Successive permutations of the label sequence
differ by a **prefix shift**: one element is moved to the front and the elements it
jumps over move one place right. With the sequence in a linked list this is an ``O(1)``
pointer update, and the rule that picks the element is a constant number of comparisons:

* let ``x_1 >= x_2 >= ... >= x_i < x_{i+1}`` be the longest non-increasing prefix;
* move ``x_{i+2}`` to the front if it exists and ``x_i >= x_{i+2}``, else move ``x_{i+1}``.

The order is cyclic; we start at the non-increasing arrangement ``(N-1)^m ... 1^m 0^m``
(whose successor moves the last element to the front) and stop just before returning to
it. Thread labels are compared as integers, so "largest" means the highest thread index.

Time per output: ``O(1)`` worst case for the successor (loopless), plus ``O(n)`` to
walk the list and materialize the tuple of node indices.
Memory: ``O(n)`` (two integer arrays and three cursors). Non-recursive.
Not an adjacent-transposition Gray code, but a minimal change of its own kind: each
step is one cyclic rotation of a prefix.
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import BASE, base_chains


def coollex_interleavings(chains: list[list[int]]) -> Iterator[Linearization]:
    """Interleavings of ``chains`` in cool-lex order of the chain-label sequence."""
    sizes = [len(c) for c in chains]
    n = sum(sizes)
    if n == 0:
        yield ()
        return
    # Non-increasing label list; the cool-lex order is cyclic and we start here.
    val = [t for t in range(len(chains) - 1, -1, -1) for _ in range(sizes[t])]
    nxt = list(range(1, n)) + [-1]  # nxt[k] = index of the node after node k, -1 = end
    head = 0
    cnt = [0] * len(chains)

    def emit() -> Linearization:
        for t in range(len(cnt)):
            cnt[t] = 0
        out = []
        k = head
        while k != -1:
            t = val[k]
            out.append(chains[t][cnt[t]])
            cnt[t] += 1
            k = nxt[k]
        return tuple(out)

    yield emit()
    if n == 1:
        return
    # Invariant inside the loop: i is the last node of the longest non-increasing
    # prefix and j = i.next. For the sorted start the first shift must move the last
    # element to the front, which the rule below does from i = second-to-last, j = last.
    # The loop stops when the successor would be the sorted arrangement again.
    i, j = n - 2, n - 1
    while nxt[j] != -1 or val[j] < val[head]:
        if nxt[j] != -1 and val[i] >= val[nxt[j]]:
            s = j
        else:
            s = i
        t = nxt[s]  # the element moved to the front
        nxt[s] = nxt[t]
        nxt[t] = head
        if val[t] < val[head]:
            i = t
        head = t
        j = nxt[i]
        yield emit()


@register
class FableCoolLex(LinEnumerator):
    name = "fable51-b-coollex"
    description = "loopless cool-lex order: each step is a prefix shift of the label sequence"
    capabilities = BASE

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return coollex_interleavings(base_chains(setup))
