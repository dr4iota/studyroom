"""``fable51-s-tree``: family-tree (reverse-search) enumeration, constant amortized time.

In the spirit of A. Ono and S. Nakano, *Constant time generation of linear extensions*,
FCT 2005 (the parent rule and its analysis below are our own derivation).

Idea
----
Label the nodes ``0..n-1`` by a topological order, so the identity is a linear
extension (the *root*). Write an extension as its label sequence ``e``. A *descent* is
a position ``j`` with ``e[j] > e[j+1]``; swapping a descent is always legal (``e[j+1] ≺
e[j]`` would contradict the labelling) and removes one inversion. Define

    parent(e) = e with its leftmost descent swapped.

Every extension other than the root has exactly one parent with fewer inversions, so
the parent pointers form a tree rooted at the identity; we enumerate it depth first.
The children of ``e`` (leftmost descent ``d``, or none) are the sequences obtained by
swapping an *ascent* ``j`` with ``e[j]`` and ``e[j+1]`` incomparable such that ``j``
becomes the leftmost descent:

* ``j <= d-1``: any incomparable ascent left of ``d`` (positions ``< j`` stay ascents;
  the new pair at ``j-1`` is an ascent because ``e[j-1] < e[j] < e[j+1]``);
* ``j = d+1``: allowed iff ``e[d+1] < e[d+2]``, ``e[d] < e[d+2]`` and the two are
  incomparable.

Let ``C(e) = {j < d-1 : e[j], e[j+1] incomparable}``. Every element of ``C(e)`` is a
child position, and for a child ``e'`` at position ``j'`` the set ``C(e')`` is a prefix
of ``C(e)`` (children at ``j' <= d-1``) or ``C(e)`` plus at most one new position
(child at ``d+1``). So ``C`` lives in one shared array with a length per tree level,
and the children of a node are found in ``O(#children + 1)`` time. A tree with ``e(P)``
nodes has ``e(P) - 1`` edges, hence the whole traversal is ``O(e(P))``: constant
amortized time per output (plus ``O(n)`` to materialise each tuple).

Sync needs nothing special: incomparability is read from the transitive closure.

Cost
----
``O(1)`` amortized per output plus ``O(n)`` per tuple; iterative DFS with an explicit
stack, so no recursion and ``O(depth)`` extra memory where depth <= number of
inversions <= n(n-1)/2; plus the ``O(n^2)``-bit closure. Deterministic and lazy.
Adjacency: parent and child differ by one adjacent transposition, but consecutive
outputs in DFS preorder may differ by up to ``2 * depth`` transpositions, so no Gray
property is claimed.
"""

from __future__ import annotations

from typing import Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization, TracePoset
from harness.registry import register

from .common import SYNC, closure_above, relabel_closure, topo_labels


def linear_extensions(P: TracePoset) -> Iterator[Linearization]:
    n = len(P)
    if n == 0:
        yield ()
        return
    nodes, label_of = topo_labels(P)
    up = relabel_closure(closure_above(P, nodes), nodes, label_of)
    e = list(range(n))  # current extension as labels
    cur = list(nodes)  # the same as node indices
    cand = [0] * n  # shared candidate array; a tree level owns the prefix cand[:clen]

    def kids_of(d: int, clen: int) -> list[tuple[int, int, int]]:
        """Children of the current node: ``(position, child's clen, value to append or -1)``."""
        kids = []
        for idx in range(clen):
            j = cand[idx]
            kids.append((j, idx - (1 if idx > 0 and cand[idx - 1] == j - 1 else 0), -1))
        if d >= 0:
            left_ok = d >= 1 and not (up[e[d - 1]] >> e[d]) & 1
            if left_ok:
                kids.append((d - 1, clen - (1 if clen > 0 and cand[clen - 1] == d - 2 else 0), -1))
            if d + 2 < n and e[d + 1] < e[d + 2] and e[d] < e[d + 2] and not (up[e[d + 1]] >> e[d + 2]) & 1:
                kids.append((d + 1, clen + 1, d - 1) if left_ok else (d + 1, clen, -1))
        return kids

    clen = 0
    for j in range(n - 1):
        if not (up[e[j]] >> e[j + 1]) & 1:
            cand[clen] = j
            clen += 1
    yield tuple(cur)
    # frame: [kids, next index, swapped position (-1 for the root), pushed index, saved value]
    stack = [[kids_of(-1, clen), 0, -1, -1, -1]]
    while stack:
        fr = stack[-1]
        if fr[1] < len(fr[0]):
            j, newlen, pushval = fr[0][fr[1]]
            fr[1] += 1
            pushpos = saved = -1
            if pushval >= 0:
                pushpos = newlen - 1
                saved = cand[pushpos]
                cand[pushpos] = pushval
            e[j], e[j + 1] = e[j + 1], e[j]
            cur[j], cur[j + 1] = cur[j + 1], cur[j]
            yield tuple(cur)
            stack.append([kids_of(j, newlen), 0, j, pushpos, saved])
        else:
            stack.pop()
            j = fr[2]
            if j >= 0:
                e[j], e[j + 1] = e[j + 1], e[j]
                cur[j], cur[j + 1] = cur[j + 1], cur[j]
                if fr[3] >= 0:
                    cand[fr[3]] = fr[4]


@register
class FableSyncTree(LinEnumerator):
    name = "fable51-s-tree"
    description = "family tree (parent = swap leftmost descent), iterative DFS, CAT"
    capabilities = SYNC

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return linear_extensions(setup.poset)
