"""Linear-extension enumerators for the trace poset with sync (``K >= 0``).

With sync the poset is ``N`` thread chains plus ``K`` virtual nodes ``sync.k`` joined by
cross edges, so thread-word interleaving (the base-case trick of ``contrib.linear_opus55_1.base``) no
longer suffices. Every algorithm here works on the general DAG ``setup.poset``
(``preds``/``succs``) and is therefore correct for any poset, including ``K = 0``.

A fact used throughout: two elements that are *adjacent* in a linear extension are
comparable iff one covers the other, and every cover relation is an edge of any DAG
that generates the order. So "may these two neighbours be swapped" is answered by one
bit test in a per-node successor bitmask (``succmask[x] >> y & 1``), with no transitive
closure.

All algorithms emit a fresh ``tuple`` per output, which alone costs ``O(n)`` (in C).
The time per output quoted in each docstring is the combinatorial work of moving from
one linearization to the next, excluding that copy.

Algorithms (registered with the ``opus55-s-`` prefix):

``opus55-s-vr``     Varol-Rotem / Knuth 7.2.1.2 Algorithm V on the general poset
``opus55-s-pr``     Pruesse-Ruskey: Hamilton path in the prism of the transposition graph,
                  every other vertex output. Consecutive outputs differ by ONE OR TWO
                  adjacent transpositions. CAT.
``opus55-s-tree``   Ono-Nakano style family tree (reverse search) with the alternating
                  pre/post-order walk: consecutive outputs differ by AT MOST THREE
                  adjacent transpositions. CAT.
``opus55-s-seg``    splits the poset at cut nodes (nodes comparable to all others, e.g. a
                  full ``at`` barrier) into independent segments and enumerates the
                  product lazily, each segment by Varol-Rotem.
``opus55-s-segcount`` (counter) product over segments of a down-set DP.

No enumerator sets ``gray_code = True``: already for two chains of length 2 (no sync) the
transposition graph is bipartite with colour classes 4 and 2, so no listing with exactly
one adjacent transposition per step exists in general (see ``contrib.linear_opus55_1.base``).
"""

from __future__ import annotations

import heapq
from bisect import bisect_right
from typing import Iterator, Sequence

from abio.capabilities import Capabilities
from abio.lin.api import CountResult, LinCounter, LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

SYNC = Capabilities(rcw=False, sync=True, observed_reads=False)


# --------------------------------------------------------------------------------------
# DAG helpers
# --------------------------------------------------------------------------------------


def _topo(n: int, succs: Sequence[Sequence[int]]) -> list[int]:
    """Deterministic topological order (Kahn, smallest ready node first)."""
    indeg = [0] * n
    for x in range(n):
        for y in succs[x]:
            indeg[y] += 1
    ready = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(ready)
    out = []
    while ready:
        x = heapq.heappop(ready)
        out.append(x)
        for y in succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(ready, y)
    if len(out) != n:
        raise ValueError("poset has a cycle")
    return out


def _relabel(n: int, succs: Sequence[Sequence[int]]) -> tuple[list[int], list[int]]:
    """Ranks ``0..n-1`` in a topological order: returns (node_of_rank, succmask by rank)."""
    order = _topo(n, succs)
    rank = [0] * n
    for r, x in enumerate(order):
        rank[x] = r
    sm = [0] * n
    for x in range(n):
        m = 0
        for y in succs[x]:
            m |= 1 << rank[y]
        sm[rank[x]] = m
    return order, sm


def _dag(setup: Setup) -> tuple[int, list[list[int]]]:
    P = setup.poset
    return len(P), [list(s) for s in P.succs]


# --------------------------------------------------------------------------------------
# 1. Varol-Rotem (Knuth's Algorithm V) on a general poset
# --------------------------------------------------------------------------------------


def varol_rotem(n: int, succs: Sequence[Sequence[int]], nodes: Sequence[int] | None = None) -> Iterator[Linearization]:
    """Varol-Rotem: the highest-ranked element that can, moves one step left; else rotate home.

    Ranks ``1..n`` come from a topological order (the first output). Step V4-V6 of
    Knuth's Algorithm V: take ``k = n``; if the left neighbour ``l`` of ``k`` is not
    below ``k`` (one bit test, see the module docstring) swap them and output;
    otherwise rotate ``k`` back to its home position ``k`` and retry with ``k - 1``.
    Non-recursive. Time: ``O(n)`` worst case per output (rotations); in practice about
    ``O(1)`` amortized (Varol-Rotem 1981; not CAT in the worst case). Memory ``O(n)``.
    Most steps are one adjacent transposition, but not all: no adjacency claim.
    ``nodes`` maps local ids to output ids (default identity).
    """
    if n == 0:
        yield ()
        return
    order, sm0 = _relabel(n, succs)
    if nodes is not None:
        order = [nodes[x] for x in order]
    # shift to 1-based ranks; rank 0 is a sentinel below everything
    sm = [0] + [m << 1 for m in sm0]
    a = list(range(n + 1))  # a[pos] = rank at position pos
    ai = list(range(n + 1))  # inverse
    node = [-1] + order
    out = list(order)  # out[pos-1] = node at pos
    yield tuple(out)
    while True:
        k = n
        while k > 0:
            j = ai[k]
            l = a[j - 1]
            if l != 0 and not (sm[l] >> k) & 1:
                a[j - 1], a[j] = k, l
                ai[k], ai[l] = j - 1, j
                out[j - 2], out[j - 1] = out[j - 1], out[j - 2]
                yield tuple(out)
                break
            if j < k:  # rotate k from position j back home to position k
                a[j:k] = a[j + 1 : k + 1]
                for p in range(j, k):
                    ai[a[p]] = p
                out[j - 1 : k - 1] = out[j:k]
                a[k] = ai[k] = k
                out[k - 1] = node[k]
            k -= 1
        else:
            return


# --------------------------------------------------------------------------------------
# 2. Pruesse-Ruskey (prism Hamilton path), one or two adjacent transpositions per step
# --------------------------------------------------------------------------------------


def _pair_decomposition(n: int, succs: Sequence[Sequence[int]]) -> tuple[list[int], list[tuple[int, int]]]:
    """Greedy removal of minimal elements: two at a time (a pair) when >= 2 are minimal,
    otherwise the unique minimal one (a fixed singleton). Returns (initial order, pairs)."""
    indeg = [0] * n
    for x in range(n):
        for y in succs[x]:
            indeg[y] += 1
    ready = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(ready)
    order: list[int] = []
    pairs: list[tuple[int, int]] = []
    while ready:
        take = [heapq.heappop(ready)]
        if ready:
            take.append(heapq.heappop(ready))
            pairs.append((take[0], take[1]))
        for x in take:
            order.append(x)
            for y in succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    heapq.heappush(ready, y)
    if len(order) != n:
        raise ValueError("poset has a cycle")
    return order, pairs


def pruesse_ruskey(n: int, succs: Sequence[Sequence[int]]) -> Iterator[Linearization]:
    """Pruesse-Ruskey (SIAM J. Comput. 1994): consecutive outputs differ by 1 or 2 adjacent transpositions.

    Decomposition: repeatedly remove two minimal elements ``(a_i, b_i)`` (a pair), or the
    unique minimal element (a fixed singleton); the removal order is the first
    extension, pair ``i`` sitting adjacent at its *home* positions.

    ``GenLE(i)`` walks the pair-``i`` placements ``(alpha, beta)`` (gaps of ``a_i`` and
    ``b_i`` in the arrangement of the later elements, ``a_i`` never passing ``b_i``)
    boustrophedon-wise, visiting every placement twice, once for each orientation of pair
    ``i-1`` (``Switch(i-1)``: swap ``a_{i-1}, b_{i-1}``, adjacent at home at that moment),
    and recursing into ``GenLE(i-1)`` at every visit. ``Switch(0)`` flips a virtual sign.
    By induction ``GenLE(i)`` is a Hamilton path, from home to home-with-pair-``i-1``-
    switched, over every arrangement with pair ``i`` in its current orientation times
    both signs. The main program runs ``GenLE(k); Switch(k); GenLE(k)``: a Hamilton path
    of the prism ``G(P) x K2`` (``G(P)``: extensions, adjacent-transposition edges).

    The prism is bipartite (colour = parity of the permutation + sign) and every step
    (a Move / ``Switch(i >= 1)`` is a transposition, ``Switch(0)`` a rung) changes the
    colour, so the path alternates colours; outputting every other vertex outputs each
    extension exactly once, and two consecutive outputs are two prism steps apart:
    one or two adjacent transpositions.

    Time: CAT, ``O(1)`` amortized per output for the moves (every ``GenLE(i)`` makes at
    least two calls to ``GenLE(i-1)``), plus the Python ``yield from`` delegation through
    the ``k <= n/2`` recursion levels (C-level, but ``O(k)`` per output). Memory ``O(n)``.
    """
    order, pairs = _pair_decomposition(n, succs)
    k = len(pairs)
    sm = [0] * n
    for x in range(n):
        for y in succs[x]:
            sm[x] |= 1 << y
    arr = list(order)
    pos = [0] * n
    for p, x in enumerate(arr):
        pos[x] = p
    A = [-1] + [p[0] for p in pairs]  # current role holders, 1-based
    B = [-1] + [p[1] for p in pairs]
    par = [0]  # colour of the current prism vertex relative to the start

    def swap_at(p: int) -> None:
        x, y = arr[p], arr[p + 1]
        arr[p], arr[p + 1] = y, x
        pos[x], pos[y] = p + 1, p
        par[0] ^= 1

    def right_b(i: int) -> bool:
        x = B[i]
        p = pos[x] + 1
        return p < n and not (sm[x] >> arr[p]) & 1

    def right_a(i: int) -> bool:
        x = A[i]
        p = pos[x] + 1
        if p >= n:
            return False
        y = arr[p]
        return y != B[i] and not (sm[x] >> y) & 1

    def switch(i: int) -> None:
        if i == 0:
            par[0] ^= 1
            return
        a, b = A[i], B[i]
        swap_at(min(pos[a], pos[b]))
        A[i], B[i] = b, a

    def gen1() -> Iterator[Linearization]:
        """GenLE(1) with the GenLE(0) visits inlined (same moves as gen(1))."""
        i = 1
        if not par[0]:
            yield tuple(arr)
        mrb = 0
        typical = False
        while right_b(i):
            mrb += 1
            swap_at(pos[B[i]])
            if not par[0]:
                yield tuple(arr)
            mra = 0
            if right_a(i):
                typical = True
                while True:
                    mra += 1
                    swap_at(pos[A[i]])
                    if not par[0]:
                        yield tuple(arr)
                    if not right_a(i):
                        break
            if typical:
                par[0] ^= 1
                if not par[0]:
                    yield tuple(arr)
                mla = mra - 1 if mrb & 1 else mra + 1
                for _ in range(mla):
                    swap_at(pos[A[i]] - 1)
                    if not par[0]:
                        yield tuple(arr)
        if typical and mrb & 1:
            swap_at(pos[A[i]] - 1)
        else:
            par[0] ^= 1
        if not par[0]:
            yield tuple(arr)
        for _ in range(mrb):
            swap_at(pos[B[i]] - 1)
            if not par[0]:
                yield tuple(arr)

    def gen(i: int) -> Iterator[Linearization]:
        if i == 1:
            yield from gen1()
            return
        sub = i - 1
        yield from gen(sub)
        mrb = 0
        typical = False
        while right_b(i):
            mrb += 1
            swap_at(pos[B[i]])
            yield from gen(sub)
            mra = 0
            if right_a(i):
                typical = True
                while True:
                    mra += 1
                    swap_at(pos[A[i]])
                    yield from gen(sub)
                    if not right_a(i):
                        break
            if typical:
                switch(sub)
                yield from gen(sub)
                mla = mra - 1 if mrb & 1 else mra + 1
                for _ in range(mla):
                    swap_at(pos[A[i]] - 1)
                    yield from gen(sub)
        if typical and mrb & 1:
            swap_at(pos[A[i]] - 1)
        else:
            switch(sub)
        yield from gen(sub)
        for _ in range(mrb):
            swap_at(pos[B[i]] - 1)
            yield from gen(sub)

    if k == 0:
        yield tuple(arr)
        return
    yield from gen(k)
    switch(k)
    yield from gen(k)


# --------------------------------------------------------------------------------------
# 3. Family tree (reverse search, Ono-Nakano style), alternating pre/post order
# --------------------------------------------------------------------------------------


def family_tree(n: int, succs: Sequence[Sequence[int]]) -> Iterator[Linearization]:
    """Reverse search over a family tree of linear extensions; <= 3 adjacent transpositions per step.

    Relabel by a topological order so the root is the identity ``0 1 .. n-1``. For a
    non-root extension ``pi`` let ``i`` be the first position with ``pi[i] != i``;
    element ``i`` sits further right, its left neighbour has a larger label and so is
    incomparable to it: the *parent* of ``pi`` moves element ``i`` one step left. The
    children of a node with first-difference index ``i`` are exactly

    * move element ``i`` one step right (same ``i``), if its right neighbour is incomparable;
    * swap positions ``i-1, i`` (elements ``i-1`` and ``pi[i]``) if incomparable (index ``i-1``);
    * swap elements ``j, j+1`` at positions ``j, j+1`` for every ``j <= i-2`` with
      ``j, j+1`` incomparable (index ``j``), read from a precomputed sorted list.

    so each child costs ``O(1)`` to produce and the tree walk is CAT. The walk outputs a
    node on entry at even depth and on exit at odd depth, so consecutive outputs are at
    tree distance at most 3 (the cube of a tree is Hamiltonian-connected, Sekanina), and
    each tree edge is one adjacent transposition.

    Time: ``O(1)`` amortized per output. Memory: ``O(n + d)`` where the stack depth ``d``
    is at most the number of inversions of an extension, ``<= n(n-1)/2``. Iterative.
    """
    if n == 0:
        yield ()
        return
    order, sm = _relabel(n, succs)
    arr = list(range(n))  # labels by position
    pos = list(range(n))
    out = list(order)  # node ids by position
    sw = [j for j in range(n - 1) if not (sm[j] >> (j + 1)) & 1]

    def swap(p: int) -> None:
        x, y = arr[p], arr[p + 1]
        arr[p], arr[p + 1] = y, x
        pos[x], pos[y] = p + 1, p
        out[p], out[p + 1] = out[p + 1], out[p]

    yield tuple(out)
    # frame: [i, stage, idx, count_of_rule3_children, via (swap position that created it)]
    stack = [[n, 0, 0, bisect_right(sw, n - 2), -1]]
    while stack:
        f = stack[-1]
        i = f[0]
        p = -1
        ni = -1
        if f[1] == 0:
            f[1] = 1
            if i < n:
                q = pos[i]
                if q + 1 < n and not (sm[i] >> arr[q + 1]) & 1:
                    p, ni = q, i
        if p < 0 and f[1] == 1:
            f[1] = 2
            if 0 < i < n and not (sm[i - 1] >> arr[i]) & 1:
                p, ni = i - 1, i - 1
        if p < 0 and f[2] < f[3]:
            p = ni = sw[f[2]]
            f[2] += 1
        if p >= 0:
            swap(p)
            stack.append([ni, 0, 0, bisect_right(sw, ni - 2), p])
            if not (len(stack) - 1) & 1:
                yield tuple(out)
        else:
            if (len(stack) - 1) & 1:
                yield tuple(out)
            stack.pop()
            if f[4] >= 0:
                swap(f[4])


# --------------------------------------------------------------------------------------
# 4. Cut-node segmentation (barriers) with a lazy product
# --------------------------------------------------------------------------------------


def segments(n: int, succs: Sequence[Sequence[int]]) -> tuple[list[int], list[list[int]]]:
    """Cut nodes (comparable to every other node) in order, and the segments between them.

    ``Lin(P) = Lin(S_0) . c_1 . Lin(S_1) . c_2 ... c_m . Lin(S_m)``: every segment is
    entirely above the previous cut and below the next. Segments list nodes in a
    topological order. Reachability by bitsets: ``O(n * edges / wordsize)``.
    """
    order = _topo(n, succs)
    preds: list[list[int]] = [[] for _ in range(n)]
    for x in range(n):
        for y in succs[x]:
            preds[y].append(x)
    down = [0] * n
    for x in order:
        m = 0
        for p in preds[x]:
            m |= down[p] | (1 << p)
        down[x] = m
    up = [0] * n
    for x in reversed(order):
        m = 0
        for s in succs[x]:
            m |= up[s] | (1 << s)
        up[x] = m
    cuts = [x for x in order if (down[x] | up[x]).bit_count() == n - 1]
    cutmask = 0
    for c in cuts:
        cutmask |= 1 << c
    segs: list[list[int]] = [[] for _ in range(len(cuts) + 1)]
    for x in order:
        if not (cutmask >> x) & 1:
            segs[(down[x] & cutmask).bit_count()].append(x)
    return cuts, segs


def _sub(seg: list[int], succs: Sequence[Sequence[int]]) -> list[list[int]]:
    loc = {x: i for i, x in enumerate(seg)}
    return [[loc[y] for y in succs[x] if y in loc] for x in seg]


def segmented(n: int, succs: Sequence[Sequence[int]]) -> Iterator[Linearization]:
    """Lazy odometer product over the cut segments, each enumerated by Varol-Rotem.

    The last segment changes fastest; when it is exhausted it is restarted and the
    previous one advances. Time: amortized ``O(1)`` segment work per output plus the
    ``O(n)`` concatenation (same order as the tuple copy); the prefix before the changed
    segment is reused. Memory ``O(n)``. For a chain of barriers this avoids Varol-Rotem
    rotations across segment boundaries, but in CPython the extra generator layer makes it
    about 0.6-0.7x the speed of plain ``opus55-s-vr`` (measured); its value is structural.
    """
    cuts, segs = segments(n, succs)
    subs = [(len(s), _sub(s, succs), s) for s in segs]
    m = len(subs)

    def fresh(j: int) -> Iterator[Linearization]:
        ln, sc, s = subs[j]
        return varol_rotem(ln, sc, s)

    its = [fresh(j) for j in range(m)]
    cur = [next(it) for it in its]
    glue = [(c,) for c in cuts] + [()]

    # pre[j] = concatenation of segments 0..j-1 with their cuts; rebuilt from the
    # lowest segment that changed, so the common step touches one segment only.
    pre: list[tuple] = [()] * (m + 1)

    def rebuild(j: int) -> None:
        for q in range(j, m):
            pre[q + 1] = pre[q] + cur[q] + glue[q]

    rebuild(0)
    yield pre[m]
    while True:
        j = m - 1
        while j >= 0:
            nxt = next(its[j], None)
            if nxt is not None:
                cur[j] = nxt
                break
            its[j] = fresh(j)
            cur[j] = next(its[j])
            j -= 1
        if j < 0:
            return
        rebuild(j)
        yield pre[m]


def count_downsets_dp(n: int, succs: Sequence[Sequence[int]]) -> int:
    """|Lin| by forward DP over down-sets (bitmasks), level by level (``O(#down-sets * n)``)."""
    if n == 0:
        return 1
    predmask = [0] * n
    for x in range(n):
        for y in succs[x]:
            predmask[y] |= 1 << x
    full = (1 << n) - 1
    layer = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for d, w in layer.items():
            rest = full & ~d
            while rest:
                low = rest & -rest
                x = low.bit_length() - 1
                rest ^= low
                if predmask[x] & d == predmask[x]:
                    e = d | low
                    nxt[e] = nxt.get(e, 0) + w
        layer = nxt
    return layer[full]


def count_segmented(n: int, succs: Sequence[Sequence[int]]) -> int:
    _, segs = segments(n, succs)
    r = 1
    for s in segs:
        r *= count_downsets_dp(len(s), _sub(s, succs))
    return r


# --------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------


@register
class OpusSyncVarolRotem(LinEnumerator):
    name = "opus55-s-vr"
    description = "Varol-Rotem (Knuth Alg. V) on the general poset, sync aware"
    capabilities = SYNC

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return varol_rotem(*_dag(setup))


@register
class OpusSyncPruesseRuskey(LinEnumerator):
    name = "opus55-s-pr"
    description = "Pruesse-Ruskey prism Gray code: 1 or 2 adjacent transpositions per step, CAT"
    capabilities = SYNC
    gray_code = False  # 1 or 2 transpositions; exactly-1 is impossible in general

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return pruesse_ruskey(*_dag(setup))


@register
class OpusSyncFamilyTree(LinEnumerator):
    name = "opus55-s-tree"
    description = "family-tree reverse search, pre/post alternation: <= 3 adjacent transpositions per step, CAT"
    capabilities = SYNC

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return family_tree(*_dag(setup))


@register
class OpusSyncSegmented(LinEnumerator):
    name = "opus55-s-seg"
    description = "split at cut nodes (barriers), lazy product of per-segment Varol-Rotem"
    capabilities = SYNC

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return segmented(*_dag(setup))


@register
class OpusSyncSegCount(LinCounter):
    name = "opus55-s-segcount"
    description = "exact count: product over cut segments of a down-set DP"
    capabilities = SYNC

    def count(self, setup: Setup) -> CountResult:
        return CountResult(count_segmented(*_dag(setup)), None, "segmented-downset-dp")
