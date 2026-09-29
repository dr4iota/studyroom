"""Case b linearization enumerator and counter.

With K = 0 the trace poset is a disjoint union of the thread chains, so Lin(P) is the set
of interleavings of those chains. The enumerator walks the multiset permutations of the
chain labels in lexicographic order (classic "next permutation") and maps each label
sequence to node indices, remapping only the suffix that changed.

If the poset ever has an edge that is not a consecutive step of one chain (it should not
in case b), a generic linear-extension enumerator is used instead, so the output is
still exactly Lin(P).
"""

from __future__ import annotations

from math import factorial
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register


def _pure_chains(poset) -> list[list[int]] | None:
    """The non-empty chains if P is exactly their disjoint union, else None."""
    n = len(poset)
    chains = [list(c) for c in poset.chains if c]
    seen = [False] * n
    for c in chains:
        for x in c:
            if seen[x]:
                return None
            seen[x] = True
    if not all(seen):
        return None
    for c in chains:
        for j, x in enumerate(c):
            p = poset.preds[x]
            if j == 0:
                if p:
                    return None
            elif len(p) != 1 or p[0] != c[j - 1]:
                return None
    return chains


def _interleavings(chains: list[list[int]]) -> Iterator[Linearization]:
    m = len(chains)
    lens = [len(c) for c in chains]
    seq: list[int] = []
    for ci in range(m):
        seq.extend([ci] * lens[ci])
    n = len(seq)
    out = [0] * n
    k = 0
    for ci in range(m):
        for x in chains[ci]:
            out[k] = x
            k += 1
    yield tuple(out)
    if n < 2:
        return
    cnt = [0] * m
    while True:
        i = n - 2
        while i >= 0 and seq[i] >= seq[i + 1]:
            i -= 1
        if i < 0:
            return
        a = seq[i]
        j = n - 1
        while seq[j] <= a:
            j -= 1
        seq[i] = seq[j]
        seq[j] = a
        seq[i + 1:] = seq[:i:-1]
        for k in range(i, n):
            cnt[seq[k]] += 1
        for k in range(i, n):
            c = seq[k]
            out[k] = chains[c][lens[c] - cnt[c]]
            cnt[c] -= 1
        yield tuple(out)


def _generic(poset) -> Iterator[Linearization]:
    """Every linear extension of an arbitrary DAG, by DFS over minimal elements."""
    n = len(poset)
    indeg = [len(p) for p in poset.preds]
    succs = poset.succs
    out: list[int] = []
    avail = sorted(x for x in range(n) if indeg[x] == 0)

    def rec() -> Iterator[Linearization]:
        if len(out) == n:
            yield tuple(out)
            return
        for x in list(avail):
            avail.remove(x)
            out.append(x)
            added = []
            for y in succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    added.append(y)
            saved = list(avail)
            avail.extend(added)
            avail.sort()
            yield from rec()
            avail[:] = saved
            for y in succs[x]:
                indeg[y] += 1
            out.pop()
            # restore x at its sorted position
            avail.append(x)
            avail.sort()

    yield from rec()


def _generic_count(poset) -> int:
    n = len(poset)
    pm = [0] * n
    for v in range(n):
        for u in poset.preds[v]:
            pm[v] |= 1 << u
    full = (1 << n) - 1
    # ways[S] = number of ways to list the down-set S; extending S only increases the
    # bitmask, so processing down-sets in increasing numeric order is sound.
    ways = {0: 1}
    frontier = [0]
    while frontier:
        s = min(frontier)
        frontier.remove(s)
        w = ways[s]
        for x in range(n):
            b = 1 << x
            if not (s & b) and (pm[x] & s) == pm[x]:
                t = s | b
                if t not in ways:
                    ways[t] = 0
                    frontier.append(t)
                ways[t] += w
    return ways.get(full, 0)


@register
class ChainInterleaveEnumerator(LinEnumerator):
    name = "opus55_1-b-interleave"
    description = "Lexicographic multiset-permutation walk over thread chains (suffix remap)"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        poset = setup.poset
        chains = _pure_chains(poset)
        if chains is None:
            return _generic(poset)
        return _interleavings(chains)


@register
class MultinomialCounter(LinCounter):
    name = "opus55_1-b-multinomial"
    description = "Counts interleavings of thread chains by the multinomial coefficient"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)

    def count(self, setup: Setup) -> CountResult:
        poset = setup.poset
        chains = _pure_chains(poset)
        if chains is None:
            total = _generic_count(poset)
        else:
            total = factorial(sum(len(c) for c in chains))
            for c in chains:
                total //= factorial(len(c))
        return CountResult(linearizations=total, method="multinomial")
