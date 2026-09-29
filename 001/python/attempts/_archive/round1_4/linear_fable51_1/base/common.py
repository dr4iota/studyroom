"""Shared helpers for the ``fable-*`` base-case linearizers.

In the base problem (reads/writes, ``K = 0``) the trace poset is a disjoint union of
``N`` chains, one per thread, so ``Lin(P)`` is the set of interleavings of the chains:
a linearization is determined by the *sequence of thread labels* (which thread's next
node comes at each position), and that sequence is a permutation of the multiset
``{0^m_0, 1^m_1, ..., (N-1)^m_{N-1}}`` with ``m_t = len(thread_chains[t])``. Every
algorithm here therefore enumerates multiset permutations of thread labels and maps
them back to node indices with :func:`labels_to_nodes`.
"""

from __future__ import annotations

from math import factorial
from typing import Sequence

from harness.capabilities import Capabilities
from harness.model import Setup
from harness.poset import Linearization

BASE = Capabilities(rcw=False, sync=False, observed_reads=False)


def base_chains(setup: Setup) -> list[list[int]]:
    """The thread chains of a base-problem setup, checked to cover every node.

    Empty threads yield empty chains (they contribute nothing to the interleaving).
    """
    P = setup.poset
    if P.sync_nodes:
        raise ValueError("fable-* linearizers handle the base problem only (no sync points)")
    chains = [list(c) for c in P.thread_chains]
    if sum(len(c) for c in chains) != len(P):
        raise ValueError("thread chains do not cover the poset")
    return chains


def labels_to_nodes(labels: Sequence[int], chains: Sequence[Sequence[int]]) -> Linearization:
    """Map a label sequence to node indices: the ``k``-th occurrence of ``t`` is ``chains[t][k]``."""
    occ = [0] * len(chains)
    out = []
    for t in labels:
        out.append(chains[t][occ[t]])
        occ[t] += 1
    return tuple(out)


def multinomial(counts: Sequence[int]) -> int:
    """Number of permutations of a multiset with the given multiplicities."""
    n = sum(counts)
    m = factorial(n)
    for c in counts:
        m //= factorial(c)
    return m
