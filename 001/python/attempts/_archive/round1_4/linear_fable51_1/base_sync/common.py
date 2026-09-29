"""Shared helpers for the ``fable51-s-*`` linearizers (base problem **plus sync**).

With sync points the trace poset is no longer a disjoint union of chains: it is the
``N`` thread chains plus ``K`` virtual ``sync.k`` nodes joined by ``before``/``after``
edges, and ``at`` events merge thread steps into the sync nodes. The algorithms here
therefore work on the general poset ``setup.poset`` (``preds``/``succs``) and only use
the chain structure as an optimisation. Everything is expressed on node indices.

Helpers:

* :func:`topo_labels` — a deterministic topological numbering (smallest node index
  first among the available ones), as ``nodes[label]``/``label_of[node]``;
* :func:`closure_above` — for every node, the bitmask of the nodes *strictly above* it
  (transitive closure), so "x ≺ y" is one shift-and-mask; ``O(n^2/wordsize)`` words.
"""

from __future__ import annotations

import heapq

from harness.capabilities import Capabilities
from harness.poset import TracePoset

SYNC = Capabilities(rcw=False, sync=True, observed_reads=False)


def topo_labels(P: TracePoset) -> tuple[list[int], list[int]]:
    """A topological numbering of ``P``: ``nodes[l]`` is the node with label ``l``.

    Deterministic: among the currently available (all predecessors placed) nodes the
    smallest node index comes first. Returns ``(nodes, label_of)``.
    """
    n = len(P)
    indeg = [len(p) for p in P.preds]
    heap = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(heap)
    nodes: list[int] = []
    while heap:
        x = heapq.heappop(heap)
        nodes.append(x)
        for y in P.succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(heap, y)
    if len(nodes) != n:
        raise ValueError("poset has a cycle")
    label_of = [0] * n
    for l, x in enumerate(nodes):
        label_of[x] = l
    return nodes, label_of


def closure_above(P: TracePoset, nodes: list[int] | None = None) -> list[int]:
    """``above[x]`` = bitmask over node indices of every ``y`` with ``x ≺ y`` (transitively)."""
    if nodes is None:
        nodes, _ = topo_labels(P)
    above = [0] * len(P)
    for x in reversed(nodes):
        m = 0
        for y in P.succs[x]:
            m |= (1 << y) | above[y]
        above[x] = m
    return above


class SubPoset:
    """An interval of ``P`` between two cut nodes, as a poset on local indices.

    Has the fields the algorithms read from a :class:`TracePoset`: ``preds``, ``succs``,
    ``chains``/``chain_of``/``pos_in_chain`` (the global chains restricted to the
    segment) and ``len``. ``nodes[i]`` is the global node of local index ``i``.
    """

    def __init__(self, P: TracePoset, nodes: list[int]) -> None:
        self.nodes = nodes
        local = {x: i for i, x in enumerate(nodes)}
        self.preds = [[local[p] for p in P.preds[x] if p in local] for x in nodes]
        self.succs = [[local[s] for s in P.succs[x] if s in local] for x in nodes]
        self.chains = [[local[x] for x in c if x in local] for c in P.chains]
        self.chains = [c for c in self.chains if c]
        self.chain_of = [0] * len(nodes)
        self.pos_in_chain = [0] * len(nodes)
        for ci, c in enumerate(self.chains):
            for j, x in enumerate(c):
                self.chain_of[x], self.pos_in_chain[x] = ci, j

    def __len__(self) -> int:
        return len(self.nodes)


def cut_segments(P: TracePoset) -> list[list[int]]:
    """Split ``P`` at its cut nodes into intervals whose linearizations concatenate.

    A *cut node* is comparable with every other node (a full ``at`` barrier is one, and
    so is any step that every other step is ordered against); it occupies the same
    position in every linearization, so ``Lin(P)`` is the concatenation product of the
    linearizations of the intervals between consecutive cut nodes. Returns the segments
    in order, each a sorted list of global nodes (cut nodes are singleton segments).
    """
    n = len(P)
    if n == 0:
        return []
    nodes, _ = topo_labels(P)
    above = closure_above(P, nodes)
    nbelow = [0] * n
    for x in range(n):
        bits = above[x]
        while bits:
            low = bits & -bits
            nbelow[low.bit_length() - 1] += 1
            bits ^= low
    cuts = sorted((nbelow[x], x) for x in range(n) if nbelow[x] + bin(above[x]).count("1") == n - 1)
    bounds = [-1] + [k for k, _ in cuts] + [n]
    segs: list[list[int]] = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        if i > 0:
            segs.append([cuts[i - 1][1]])
        seg = [x for x in range(n) if lo < nbelow[x] < hi]
        if seg:
            segs.append(seg)
    return segs


def relabel_closure(above: list[int], nodes: list[int], label_of: list[int]) -> list[int]:
    """The same closure expressed on labels: ``up[l]`` has bit ``l'`` iff ``nodes[l] ≺ nodes[l']``."""
    up = [0] * len(nodes)
    for l, x in enumerate(nodes):
        m, bits = 0, above[x]
        while bits:
            low = bits & -bits
            m |= 1 << label_of[low.bit_length() - 1]
            bits ^= low
        up[l] = m
    return up
