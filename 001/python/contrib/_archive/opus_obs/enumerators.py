"""Enumerators and counters of ``LinFeas(P)`` (feasible linearizations given observed reads).

Scope: Read/Write, sync (any mix of before/after/at), observed read results, write data
constant / ``"*"`` / expressions over earlier writes. Read-dependent write data is NOT
supported (``data_from_reads=False``).

All feasibility reasoning is in :mod:`contrib._archive.opus_obs.core`: per block, ``F(R)`` decides
whether a relation ``R`` on the block's relevant actions (writes + observed reads) admits
a reads-from assignment satisfying (i)-(iii); ``F(<_L)`` is exactly the feasibility of
``L`` and ``F`` is antitone in ``R``. Unobserved reads and blocks without observed reads
never matter.

Two bounds on the unknown interval order of a partial object are used:

* **prefix lower bound** (``opus-o-prune``, ``opus-o-memo``, ``opus-o-dpcount``). In a
  prefix of a linearization, ``x < y`` is already *certain* if ``e(x)`` is placed and
  ``s(y)`` was not placed before it (it will come later), or if ``e(x) <_P s(y)``. Every
  completion's ``<`` contains this set ``R0``; if ``F(R0)`` fails for some block, no
  completion is feasible. ``R0`` only grows when the end of a relevant action is placed,
  so ``F`` is re-evaluated only there. When the last relevant end is placed, ``R0`` is
  the exact ``<`` restricted to relevant actions, so leaves need no further test.

* **poset bounds** (``opus-o-split``, ``opus-o-splitcount``). For a poset ``Q`` extending
  ``P``, ``R0(Q) = {(x, y): e(x) <_Q s(y)}`` is in every ``<_L`` (``L in Lin(Q)``) and
  ``R1(Q) = {(x, y): not s(y) <_Q e(x)}`` contains every ``<_L``. ``F(R0)`` false: all of
  ``Lin(Q)`` is infeasible. ``F(R1)`` true: all of ``Lin(Q)`` is feasible.

Every algorithm yields fresh tuples; tuple construction is ``O(n)`` and is not counted in
the per-output costs quoted below. ``n`` = poset nodes, ``w`` = width of ``P``
(``<= N + K``), ``m`` = relevant actions, ``T_F`` = cost of one ``F`` evaluation
(``O(sum_b R_b W_b)`` when reads-from is unambiguous, exponential in the number of
ambiguous observed reads in the worst case; see core).
"""

from __future__ import annotations

import heapq
from typing import Iterator, Sequence

from abio.capabilities import Capabilities
from abio.lin.api import CountResult, LinCounter, LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .core import ObsModel

CAPS = Capabilities(rcw=False, sync=True, observed_reads=True)


# --------------------------------------------------------------------------------------
# Plain linear-extension machinery (copied from contrib.linear_opus55_1.base_sync, self-contained)
# --------------------------------------------------------------------------------------


def _topo(n: int, succs: Sequence[Sequence[int]]) -> list[int]:
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


def varol_rotem(n: int, succs: Sequence[Sequence[int]]) -> Iterator[Linearization]:
    """Varol-Rotem / Knuth Algorithm V on a DAG (see contrib.linear_opus55_1.base_sync). ~O(1) amortized."""
    if n == 0:
        yield ()
        return
    order = _topo(n, succs)
    rank = [0] * n
    for r, x in enumerate(order):
        rank[x] = r
    sm = [0] * (n + 1)
    for x in range(n):
        m = 0
        for y in succs[x]:
            m |= 1 << (rank[y] + 1)
        sm[rank[x] + 1] = m
    a = list(range(n + 1))
    ai = list(range(n + 1))
    node = [-1] + order
    out = list(order)
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
            if j < k:
                a[j:k] = a[j + 1 : k + 1]
                for p in range(j, k):
                    ai[a[p]] = p
                out[j - 1 : k - 1] = out[j:k]
                a[k] = ai[k] = k
                out[k - 1] = node[k]
            k -= 1
        else:
            return


def count_downsets(n: int, predmask: Sequence[int]) -> int:
    """|Lin| by forward DP over down-sets (bitmasks): ``O(#down-sets * n)``."""
    if n == 0:
        return 1
    full = (1 << n) - 1
    layer = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for d, c in layer.items():
            rest = full & ~d
            while rest:
                low = rest & -rest
                rest ^= low
                x = low.bit_length() - 1
                if predmask[x] & d == predmask[x]:
                    e = d | low
                    nxt[e] = nxt.get(e, 0) + c
        layer = nxt
    return layer[full]


def _reach(n: int, succs: Sequence[Sequence[int]]) -> list[int]:
    """``reach[x]`` = bitmask of nodes strictly above ``x``."""
    reach = [0] * n
    for x in reversed(_topo(n, succs)):
        m = 0
        for y in succs[x]:
            m |= reach[y] | (1 << y)
        reach[x] = m
    return reach


# --------------------------------------------------------------------------------------
# Shared prefix-search state (prune / memo / dpcount)
# --------------------------------------------------------------------------------------


class _Prefix:
    """Relevant-action bookkeeping for prefix searches.

    ``role[node]`` is ``None`` or ``(bi, x, is_end)``: node is the start/end of local
    action ``x`` of relevant block ``bi``. ``R0[bi][x]`` is the prefix lower bound of the
    successor mask of ``x`` (module docstring): ``forced`` until ``e(x)`` is placed, then
    the set of block actions not started at that moment.
    """

    def __init__(self, setup: Setup, model: ObsModel) -> None:
        P = setup.poset
        n = len(P)
        self.n = n
        self.preds = [0] * n
        for v in range(n):
            for u in P.preds[v]:
                self.preds[v] |= 1 << u
        self.succs = [list(s) for s in P.succs]
        reach = _reach(n, self.succs)
        self.blocks = model.blocks
        self.role: list[tuple[int, int, bool] | None] = [None] * n
        self.R0: list[list[int]] = []
        for bi, bp in enumerate(self.blocks):
            forced = []
            for x in range(bp.n):
                m = 0
                for y in range(bp.n):
                    if y != x and (reach[bp.enode[x]] >> bp.snode[y]) & 1:
                        m |= 1 << y
                forced.append(m)
                self.role[bp.snode[x]] = (bi, x, False)
                self.role[bp.enode[x]] = (bi, x, True)
            self.R0.append(forced)
        self.started = [0] * len(self.blocks)

    def root_ok(self) -> bool:
        return all(bp.feasible(self.R0[bi]) for bi, bp in enumerate(self.blocks))

    def place(self, v: int) -> tuple[bool, int]:
        """Apply node ``v``; returns (still possibly feasible, undo token)."""
        r = self.role[v]
        if r is None:
            return True, -1
        bi, x, is_end = r
        if not is_end:
            self.started[bi] |= 1 << x
            return True, -1
        bp = self.blocks[bi]
        old = self.R0[bi][x]
        self.R0[bi][x] = bp.full & ~self.started[bi]
        return bp.feasible(self.R0[bi]), old

    def unplace(self, v: int, token: int) -> None:
        r = self.role[v]
        if r is None:
            return
        bi, x, is_end = r
        if is_end:
            self.R0[bi][x] = token
        else:
            self.started[bi] &= ~(1 << x)

    def key(self) -> tuple:
        """The part of the state that, with the down-set, determines the future."""
        return tuple(m for row in self.R0 for m in row)


# --------------------------------------------------------------------------------------
# 1. Filter: Varol-Rotem + exact fixed-L test
# --------------------------------------------------------------------------------------


def enum_filter(setup: Setup) -> Iterator[Linearization]:
    """Every ``L`` of ``Lin(P)`` (Varol-Rotem), kept iff the exact fixed-``L`` test holds.

    Criterion: the core Theorem/Corollary (exact). Time: ``O(1)`` amortized to produce
    each candidate, plus ``O(n + sum_b m_b^2) + T_F`` to test it, for every element of
    ``Lin(P)`` (accepted or rejected). Memory ``O(n + m)``.
    """
    model = ObsModel(setup)
    P = setup.poset
    n = len(P)
    it = varol_rotem(n, [list(s) for s in P.succs])
    if model.trivial:
        yield from it
        return
    if model.hopeless:
        return
    pos = [0] * n
    for o in it:
        for i, x in enumerate(o):
            pos[x] = i
        if model.feasible_positions(pos):
            yield o


# --------------------------------------------------------------------------------------
# 2. Prune: prefix DFS with the antitone lower-bound test
# --------------------------------------------------------------------------------------


def enum_prune(setup: Setup) -> Iterator[Linearization]:
    """DFS over prefixes (minimal-element choice, ascending node index), cutting a prefix
    as soon as ``F(R0)`` fails for the block whose relevant action just ended.

    Correctness: ``R0`` is contained in the interval order of every completion and ``F``
    is antitone, so no feasible ``L`` is cut; after the last relevant end ``R0`` is exact,
    so every leaf is feasible (no leaf test). Each ``L`` is one root-leaf path: no
    duplicates. Not dead-end free (``R0`` misses pairs a completion must add).
    Time: ``O(w)`` per search node plus ``T_F`` at each relevant end node; per output
    ``O(n (w + T_F))`` worst case, plus the work in cut subtrees (each cut node costs one
    ``F``). Memory ``O(n + m)`` (recursion depth ``n``).
    """
    model = ObsModel(setup)
    if model.hopeless:
        return
    st = _Prefix(setup, model)
    if not st.root_ok():
        return
    n = st.n
    preds, succs = st.preds, st.succs
    order: list[int] = []
    done = 0

    def rec(avail: list[int]) -> Iterator[Linearization]:
        nonlocal done
        if len(order) == n:
            yield tuple(order)
            return
        for i, v in enumerate(avail):
            ok, tok = st.place(v)
            if ok:
                done |= 1 << v
                order.append(v)
                nav = avail[:i] + avail[i + 1 :]
                for y in succs[v]:
                    if preds[y] & done == preds[y]:
                        nav.append(y)
                nav.sort()
                yield from rec(nav)
                order.pop()
                done &= ~(1 << v)
            st.unplace(v, tok)

    yield from rec(sorted(x for x in range(n) if not preds[x]))


# --------------------------------------------------------------------------------------
# 3. Memo: prefix DFS + dead-state memo (and the counting DP built on the same states)
# --------------------------------------------------------------------------------------


def enum_memo(setup: Setup) -> Iterator[Linearization]:
    """``opus-o-prune`` plus a memo of *dead* states.

    State of a prefix = (down-set, ``R0``). The future is a function of the state: the
    remaining linear extensions depend only on the down-set, and for every completion the
    interval order on relevant actions is ``R0`` for the ended actions plus pairs decided
    by the suffix (a started, not ended action precedes exactly the actions started after
    its end; unstarted actions are all after the down-set). So "no feasible completion"
    is a property of the state, and a state found dead is never expanded again.

    Time: every live state is expanded once per path reaching it (each such expansion
    leads to >= 1 output, so it is charged to outputs: ``O(n (w + T_F))`` per output);
    every dead state is expanded at most once: ``O(w (m + T_F))`` per dead state. So the
    total is ``O(#outputs * n (w + T_F) + #dead states * w (m + T_F))`` instead of the
    prune version's dead *subtrees*. Memory: ``O(#dead states * m)`` words.
    """
    model = ObsModel(setup)
    if model.hopeless:
        return
    st = _Prefix(setup, model)
    if not st.root_ok():
        return
    n = st.n
    preds, succs = st.preds, st.succs
    order: list[int] = []
    dead: set = set()
    done = 0

    def rec(avail: list[int]) -> Iterator[Linearization]:
        nonlocal done
        if len(order) == n:
            yield tuple(order)
            return
        for i, v in enumerate(avail):
            ok, tok = st.place(v)
            if ok:
                done |= 1 << v
                k = (done, st.key())
                if k not in dead:
                    order.append(v)
                    nav = avail[:i] + avail[i + 1 :]
                    for y in succs[v]:
                        if preds[y] & done == preds[y]:
                            nav.append(y)
                    nav.sort()
                    produced = False
                    for o in rec(nav):
                        produced = True
                        yield o
                    if not produced:
                        dead.add(k)
                    order.pop()
                done &= ~(1 << v)
            st.unplace(v, tok)

    yield from rec(sorted(x for x in range(n) if not preds[x]))


def count_dp(setup: Setup) -> tuple[int, int]:
    """(|Lin(P)|, |LinFeas(P)|) by a memoized DP over prefix states (down-set, ``R0``).

    ``feas(state)`` = sum over the minimal elements ``v`` of the remaining poset of
    ``feas(state + v)``, 0 if ``F(R0)`` fails, 1 at the full set: exact by the argument of
    :func:`enum_memo`. ``|Lin(P)|`` is the same DP on down-sets only. Time
    ``O(#states * w * (m + T_F))``, memory ``O(#states * m)``. With no observations the
    state is the down-set and this is the classic down-set DP.
    """
    model = ObsModel(setup)
    st = _Prefix(setup, model)
    n = st.n
    preds = st.preds
    full = (1 << n) - 1
    total = count_downsets(n, preds)
    if model.trivial:
        return total, total
    if model.hopeless or not st.root_ok():
        return total, 0
    memo: dict = {}

    def feas(done: int) -> int:
        if done == full:
            return 1
        k = (done, st.key())
        c = memo.get(k)
        if c is not None:
            return c
        c = 0
        rest = full & ~done
        while rest:
            low = rest & -rest
            rest ^= low
            v = low.bit_length() - 1
            if preds[v] & done == preds[v]:
                ok, tok = st.place(v)
                if ok:
                    c += feas(done | low)
                st.unplace(v, tok)
        memo[k] = c
        return c

    import sys

    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 4 * n + 100))
    try:
        return total, feas(0)
    finally:
        sys.setrecursionlimit(old)


# --------------------------------------------------------------------------------------
# 4. Split: disjoint decomposition of LinFeas(P) into Lin(Q_i) by branching on pairs
# --------------------------------------------------------------------------------------


def _split_leaves(setup: Setup, model: ObsModel) -> Iterator[list[list[int]]]:
    """Yield successor lists of posets ``Q_1, Q_2, ..`` with ``LinFeas(P) = disjoint union Lin(Q_i)``.

    A node of the branching tree is a poset ``Q`` (``P`` plus added edges). Per relevant
    block compute ``R0(Q)`` and ``R1(Q)`` (module docstring). If some block has
    ``F(R0) = False`` the node is dropped (all of ``Lin(Q)`` infeasible, by antitonicity).
    If every block has ``F(R1) = True`` then ``Lin(Q)`` is entirely feasible and ``Q`` is
    a leaf. Otherwise some block with ``F(R1) = False`` has an *undecided* ordered pair
    ``(x, y)`` (neither ``e(x) <_Q s(y)`` nor ``s(y) <_Q e(x)``; if all its pairs were
    decided then ``R0 = R1`` there, contradicting ``F(R0) != F(R1)``), and ``Lin(Q)``
    splits into the disjoint, nonempty ``Lin(Q + e(x)->s(y))`` (``x < y``) and
    ``Lin(Q + s(y)->e(x))`` (not ``x < y``): each linearization has exactly one of the two
    relations, and neither edge closes a cycle because the pair is undecided. Each branch
    decides one more pair, so the tree is finite (depth ``<= sum_b m_b^2``), every internal
    node has two children, and the leaves partition ``LinFeas(P)``.

    Pair choice: in the first failing block, pairs (read, write), (write, read),
    (write, write), (read, read) in that order; this decides reads-from candidates first.
    """
    P = setup.poset
    n = len(P)
    succ0 = [list(s) for s in P.succs]
    reach0 = _reach(n, succ0)
    blocks = model.blocks
    pairs_of = []
    for bp in blocks:
        W, m = bp.W, bp.n
        rw = [(r, w) for r in range(W, m) for w in range(W)]
        wr = [(w, r) for w in range(W) for r in range(W, m)]
        ww = [(a, b) for a in range(W) for b in range(W) if a != b]
        rr = [(a, b) for a in range(W, m) for b in range(W, m) if a != b]
        pairs_of.append(rw + wr + ww + rr)

    def bounds(reach: list[int], bp) -> tuple[list[int], list[int]]:
        r0, r1 = [], []
        sn, en = bp.snode, bp.enode
        for x in range(bp.n):
            rx = reach[en[x]]
            a = b = 0
            for y in range(bp.n):
                if y == x:
                    continue
                if (rx >> sn[y]) & 1:
                    a |= 1 << y
                    b |= 1 << y
                elif not (reach[sn[y]] >> en[x]) & 1:
                    b |= 1 << y
            r0.append(a)
            r1.append(b)
        return r0, r1

    def add_edge(reach: list[int], u: int, v: int) -> list[int]:
        up = reach[v] | (1 << v)
        bit = 1 << u
        return [r | up if (i == u or (r & bit)) else r for i, r in enumerate(reach)]

    # explicit stack of (reach, extra edges); left branch (x < y) first
    stack: list[tuple[list[int], tuple]] = [(reach0, ())]
    while stack:
        reach, extra = stack.pop()
        branch = None
        dead = False
        for bi, bp in enumerate(blocks):
            r0, r1 = bounds(reach, bp)
            if not bp.feasible(r0):
                dead = True
                break
            if branch is None and not bp.feasible(r1):
                for x, y in pairs_of[bi]:
                    if not (r0[x] >> y) & 1 and (r1[x] >> y) & 1:
                        branch = (bp.enode[x], bp.snode[y])
                        break
                assert branch is not None, "F(R0) != F(R1) needs an undecided pair"
        if dead:
            continue
        if branch is None:
            succ = [list(s) for s in succ0]
            for u, v in extra:
                succ[u].append(v)
            yield succ
            continue
        ex, sy = branch
        stack.append((add_edge(reach, sy, ex), extra + ((sy, ex),)))  # not x < y
        stack.append((add_edge(reach, ex, sy), extra + ((ex, sy),)))  # x < y


def enum_split(setup: Setup) -> Iterator[Linearization]:
    """Enumerate each leaf poset ``Q_i`` of :func:`_split_leaves` with Varol-Rotem.

    Correctness: the leaves partition ``LinFeas(P)`` (proof in ``_split_leaves``), so the
    concatenation lists every feasible ``L`` exactly once and nothing else; no output is
    tested individually. Every leaf is nonempty. Time: ``O(1)`` amortized per output inside
    a leaf, plus per tree node ``O(n + sum_b m_b^2 + T_F)``; the tree has ``2(#leaves
    + #dropped) - 1`` nodes, and ``#leaves <= #outputs``. Memory: ``O(depth * n)`` words
    for the DFS stack of reachability vectors (depth ``<= sum_b m_b^2``).
    """
    model = ObsModel(setup)
    n = len(setup.poset)
    if model.trivial:
        yield from varol_rotem(n, [list(s) for s in setup.poset.succs])
        return
    if model.hopeless:
        return
    for succ in _split_leaves(setup, model):
        yield from varol_rotem(n, succ)


def count_split(setup: Setup) -> tuple[int, int, int]:
    """(|Lin(P)|, |LinFeas(P)|, #leaves): sum of down-set DP counts over the split leaves."""
    model = ObsModel(setup)
    n = len(setup.poset)

    def pm(succ: list[list[int]]) -> list[int]:
        p = [0] * n
        for u in range(n):
            for v in succ[u]:
                p[v] |= 1 << u
        return p

    total = count_downsets(n, pm([list(s) for s in setup.poset.succs]))
    if model.trivial:
        return total, total, 1
    if model.hopeless:
        return total, 0, 0
    feas = leaves = 0
    for succ in _split_leaves(setup, model):
        leaves += 1
        feas += count_downsets(n, pm(succ))
    return total, feas, leaves


# --------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------


@register
class OpusObsFilter(LinEnumerator):
    name = "opus-o-filter"
    description = "Varol-Rotem over Lin(P) + exact polynomial-per-rf fixed-L feasibility test"
    capabilities = CAPS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_filter(setup)


@register
class OpusObsPrune(LinEnumerator):
    name = "opus-o-prune"
    description = "prefix DFS cut by the antitone reads-from test on certain precedences"
    capabilities = CAPS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_prune(setup)


@register
class OpusObsMemo(LinEnumerator):
    name = "opus-o-memo"
    description = "prefix DFS + lower-bound cut + memo of dead (down-set, precedence) states"
    capabilities = CAPS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_memo(setup)


@register
class OpusObsSplit(LinEnumerator):
    name = "opus-o-split"
    description = "partition LinFeas(P) into Lin(Q_i) by branching on precedence pairs; VR per part"
    capabilities = CAPS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_split(setup)


@register
class OpusObsDPCount(LinCounter):
    name = "opus-o-dpcount"
    description = "feasible count by memoized DP over (down-set, certain-precedence) states"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        total, feas = count_dp(setup)
        observed = setup.features().observed_reads
        return CountResult(total, feas if observed else None, "opus-state-dp")


@register
class OpusObsSplitCount(LinCounter):
    name = "opus-o-splitcount"
    description = "feasible count: sum of down-set DP counts over the split partition"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        total, feas, _ = count_split(setup)
        observed = setup.features().observed_reads
        return CountResult(total, feas if observed else None, "opus-split-dp")
