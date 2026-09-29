"""Enumerators and counters of ``LinFeas(P)`` with observed reads and read-dependent data.

Scope: Read/Write, ``K = 0``, observed (possibly compound) read results, write data any
expression of formats.md §2.2. All feasibility reasoning is in :mod:`contrib.linear_opus55_1.obs.core`:
``F(R)`` (a joint reads-from search over all relevant blocks with term matching) is exact
at ``R = <_L`` and antitone in ``R``; ``static_pins`` gives edges every feasible ``L``
satisfies (the pinned poset ``Q``, ``LinFeas(P) subset Lin(Q) subset Lin(P)``).

Algorithms (``n`` nodes, ``w`` width, ``m`` relevant actions, ``T_F`` one ``F`` evaluation,
``T_v = O(m^2)`` one witness re-check; tuple construction ``O(n)`` per output not counted):

``opus55-o-filter``    Varol-Rotem over ``Lin(P)`` (``pins=1``: over ``Lin(Q)``) + exact test.
``opus55-o-prune``     prefix DFS over ``Lin(Q)`` cut by ``F(R0)`` on certain precedences,
                     witness reuse.
``opus55-o-memo``      ``opus55-o-prune`` + memo of dead (down-set, ``R0``) states.
``opus55-o-split``     partition of ``LinFeas(P)`` into ``Lin(Q_i)`` by branching on
                     undecided precedence pairs chosen from a broken witness; VR per part.
``opus55-o-dpcount``   feasible count, memoized DP over (down-set, ``R0``) states.
``opus55-o-splitcount`` feasible count, sum of down-set DP counts over the split leaves.
"""

from __future__ import annotations

import sys
from typing import Iterator, Sequence

from abio.capabilities import Capabilities
from abio.lin.api import CountResult, LinCounter, LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .core import DepModel, reach_of, static_pins, topo

CAPS = Capabilities(rcw=False, sync=False, observed_reads=True)


# --------------------------------------------------------------------------------------
# Plain linear-extension machinery (self-contained copy of the opus_obs versions)
# --------------------------------------------------------------------------------------


def varol_rotem(n: int, succs: Sequence[Sequence[int]]) -> Iterator[Linearization]:
    """Varol-Rotem / Knuth Algorithm V on a DAG: every linear extension once, ~O(1)
    amortized transpositions/rotations per output."""
    if n == 0:
        yield ()
        return
    order = topo(n, succs)
    assert order is not None
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
    """Number of linear extensions by forward DP over down-sets: ``O(#down-sets * n)``."""
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


def _predmasks(n: int, succs: Sequence[Sequence[int]]) -> list[int]:
    p = [0] * n
    for u in range(n):
        for v in succs[u]:
            p[v] |= 1 << u
    return p


def _pinned(setup: Setup, model: DepModel, pins: bool) -> list[list[int]] | None:
    """Successor lists of ``Q`` (``P`` plus static pins), or None if nothing is feasible."""
    succs = [list(s) for s in setup.poset.succs]
    if not pins:
        return succs
    edges = static_pins(model)
    if edges is None:
        return None
    for u, v in edges:
        succs[u].append(v)
    return succs


# --------------------------------------------------------------------------------------
# Shared prefix-search state
# --------------------------------------------------------------------------------------


class _Prefix:
    """Prefix lower bound ``R0`` with witness reuse.

    ``R0[bi][x]``: until ``e(x)`` is placed, the actions ``y`` with ``e(x) <_Q s(y)``;
    after, every block action not started at that moment (they all start later). Every
    completion's ``<`` contains ``R0`` (restricted to relevant actions), so ``not F(R0)``
    kills the prefix (antitonicity); when the last relevant end is placed, ``R0`` equals
    ``<_L`` on relevant actions, so it is exact. ``wit`` is a stack of witnesses: the top
    satisfies ``F`` for the current ``R0``; after an update it is re-checked in ``T_v``
    and the search ``solve`` runs only when it broke.
    """

    def __init__(self, model: DepModel, succs: list[list[int]]) -> None:
        n = len(succs)
        self.n = n
        self.model = model
        self.preds = _predmasks(n, succs)
        self.succs = succs
        reach = reach_of(n, succs)
        self.role: list[tuple[int, int, bool] | None] = [None] * n
        self.R0 = [bp.prec_from_reach(reach) for bp in model.blocks]
        for bi, bp in enumerate(model.blocks):
            for x in range(bp.n):
                self.role[bp.snode[x]] = (bi, x, False)
                self.role[bp.enode[x]] = (bi, x, True)
        self.started = [0] * len(model.blocks)
        self.wit: list[dict] = []
        self.solves = 0

    def root_ok(self) -> bool:
        w = self.model.solve(self.R0)
        if w is None:
            return False
        self.wit.append(w)
        return True

    def place(self, v: int) -> tuple[bool, int, bool]:
        """Apply node ``v``; returns (still possibly feasible, undo token, pushed)."""
        r = self.role[v]
        if r is None:
            return True, -1, False
        bi, x, is_end = r
        if not is_end:
            self.started[bi] |= 1 << x
            return True, -1, False
        bp = self.model.blocks[bi]
        row = self.R0[bi]
        old = row[x]
        new = bp.full & ~self.started[bi]
        row[x] = new
        if new == old or self.model.verify(self.wit[-1], self.R0):
            return True, old, False
        self.solves += 1
        w = self.model.solve(self.R0)
        if w is None:
            return False, old, False
        self.wit.append(w)
        return True, old, True

    def unplace(self, v: int, token: int, pushed: bool) -> None:
        r = self.role[v]
        if r is None:
            return
        bi, x, is_end = r
        if is_end:
            self.R0[bi][x] = token
            if pushed:
                self.wit.pop()
        else:
            self.started[bi] &= ~(1 << x)

    def key(self) -> tuple:
        return tuple(m for row in self.R0 for m in row)


# --------------------------------------------------------------------------------------
# 1. Filter
# --------------------------------------------------------------------------------------


def enum_filter(setup: Setup, pins: bool = False) -> Iterator[Linearization]:
    """Every ``L`` of ``Lin(P)`` (or ``Lin(Q)`` with ``pins``) by Varol-Rotem, kept iff
    ``F(<_L)`` (core Theorem: exact).

    Time: ``O(1)`` amortized per candidate + ``O(n + sum_b m_b^2) + T_F`` per candidate,
    accepted or rejected. Memory ``O(n + m)`` plus the match cache.
    """
    model = DepModel(setup)
    n = len(setup.poset)
    if model.trivial:
        yield from varol_rotem(n, [list(s) for s in setup.poset.succs])
        return
    if model.hopeless:
        return
    succs = _pinned(setup, model, pins)
    if succs is None:
        return
    pos = [0] * n
    for o in varol_rotem(n, succs):
        for i, x in enumerate(o):
            pos[x] = i
        if model.feasible_positions(pos):
            yield o


# --------------------------------------------------------------------------------------
# 2./3. Prefix DFS (prune, memo)
# --------------------------------------------------------------------------------------


def enum_prefix(setup: Setup, memo: bool = False, pins: bool = True) -> Iterator[Linearization]:
    """DFS over prefixes of ``Lin(Q)`` (minimal elements in ascending index), cut when
    ``F(R0)`` fails (see :class:`_Prefix`).

    Correctness: no feasible ``L`` is cut (``R0 subset <_L``, antitone ``F``, ``Q`` pins are
    necessary); every leaf is feasible (``R0`` exact after the last relevant end, and every
    relevant end is re-checked). Each ``L`` is one root-leaf path: no duplicates.

    ``memo``: a state is (down-set, ``R0``). The remaining completions depend only on the
    down-set; for each of them ``<_L`` on relevant actions is ``R0`` plus pairs decided by
    the suffix alone (an ended action precedes exactly the actions not started at its
    end, which ``R0`` records; a not-yet-ended action precedes the actions started after
    its end, all in the suffix). So "no feasible completion" is a function of the state
    and dead states are never re-expanded.

    Time: ``O(w)`` per search node, plus ``T_v`` (and ``T_F`` if the witness broke) per
    relevant end node; per output ``O(n (w + T_v))`` + amortized solves, plus the work in
    cut subtrees (``prune``) or ``O(w (m + T_F))`` per dead state (``memo``).
    Memory: ``O(n + m)`` + witness stack ``O(n m)``; ``memo`` adds ``O(m)`` words per dead state.
    """
    model = DepModel(setup)
    n = len(setup.poset)
    if model.trivial:
        yield from varol_rotem(n, [list(s) for s in setup.poset.succs])
        return
    if model.hopeless:
        return
    succs = _pinned(setup, model, pins)
    if succs is None:
        return
    st = _Prefix(model, succs)
    if not st.root_ok():
        return
    preds = st.preds
    order: list[int] = []
    dead: set = set()
    done = 0

    def rec(avail: list[int]) -> Iterator[Linearization]:
        nonlocal done
        if len(order) == n:
            yield tuple(order)
            return
        for i, v in enumerate(avail):
            ok, tok, pushed = st.place(v)
            if ok:
                done |= 1 << v
                k = (done, st.key()) if memo else None
                if k is None or k not in dead:
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
                    if memo and not produced:
                        dead.add(k)
                    order.pop()
                done &= ~(1 << v)
            st.unplace(v, tok, pushed)

    yield from rec(sorted(x for x in range(n) if not preds[x]))


# --------------------------------------------------------------------------------------
# 4. Split
# --------------------------------------------------------------------------------------


def _split_leaves(setup: Setup, model: DepModel, succ0: list[list[int]]) -> Iterator[list[list[int]]]:
    """Successor lists of posets ``Q_i`` with ``LinFeas(P) = disjoint union Lin(Q_i)``.

    Node = poset ``Q`` (``succ0`` plus added edges). ``R0(Q) = {e(x) <_Q s(y)}`` is contained
    in every ``<_L`` (``L in Lin(Q)``), ``R1(Q) = {not s(y) <_Q e(x)}`` contains every one.
    ``F(R0)`` false: drop (antitone). ``F(R1)`` true: leaf, all of ``Lin(Q)`` feasible.
    Otherwise take the witness ``rf`` of ``F(R0)``: it violates (i)-(iii) under ``R1`` but
    not under ``R0``, so a violated condition uses a pair ``(x, y)`` in ``R1 \\ R0``, i.e.
    undecided in ``Q``; ``Lin(Q)`` splits into the disjoint, nonempty
    ``Lin(Q + e(x)->s(y))`` and ``Lin(Q + s(y)->e(x))``. Each branch decides a pair, so the
    tree is finite (depth ``<= sum_b m_b^2``) and the leaves partition ``LinFeas(P)``.
    Branching on pairs that break the current witness steers toward deciding reads-from.
    """
    n = len(succ0)
    blocks = model.blocks

    def bounds(reach: list[int]):
        r0s, r1s = [], []
        for bp in blocks:
            sn, en = bp.snode, bp.enode
            r0, r1 = [], []
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
            r0s.append(r0)
            r1s.append(r1)
        return r0s, r1s

    def add_edge(reach: list[int], u: int, v: int) -> list[int]:
        up = reach[v] | (1 << v)
        bit = 1 << u
        return [r | up if (i == u or (r & bit)) else r for i, r in enumerate(reach)]

    stack: list[tuple[list[int], tuple]] = [(reach_of(n, succ0), ())]
    while stack:
        reach, extra = stack.pop()
        r0, r1 = bounds(reach)
        wit = model.solve(r0)
        if wit is None:
            continue
        if model.verify(wit, r1) or model.solve(r1) is not None:
            succ = [list(s) for s in succ0]
            for u, v in extra:
                succ[u].append(v)
            yield succ
            continue
        bpair = model.branch_pair(wit, r1, r0)
        assert bpair is not None, "a witness valid under R0 but not R1 has an undecided pair"
        bi, x, y = bpair
        ex, sy = blocks[bi].enode[x], blocks[bi].snode[y]
        stack.append((add_edge(reach, sy, ex), extra + ((sy, ex),)))  # not x < y
        stack.append((add_edge(reach, ex, sy), extra + ((ex, sy),)))  # x < y


def enum_split(setup: Setup, pins: bool = True) -> Iterator[Linearization]:
    """Varol-Rotem on each leaf poset of :func:`_split_leaves`.

    Correctness: the leaves partition ``LinFeas(P)`` (proof in ``_split_leaves``); no output
    is tested. Time: ``O(1)`` amortized per output inside a leaf, plus per tree node
    ``O(n + sum_b m_b^2 + T_F)`` (two ``F`` evaluations at most); the tree has
    ``2(#leaves + #dropped) - 1`` nodes and ``#leaves <= #outputs``. Memory
    ``O(depth * n)`` words for the DFS stack.
    """
    model = DepModel(setup)
    n = len(setup.poset)
    if model.trivial:
        yield from varol_rotem(n, [list(s) for s in setup.poset.succs])
        return
    if model.hopeless:
        return
    succs = _pinned(setup, model, pins)
    if succs is None:
        return
    for succ in _split_leaves(setup, model, succs):
        yield from varol_rotem(n, succ)


# --------------------------------------------------------------------------------------
# Counters
# --------------------------------------------------------------------------------------


def count_dp(setup: Setup, pins: bool = True) -> tuple[int, int]:
    """(|Lin(P)|, |LinFeas(P)|) by a memoized DP over prefix states (down-set, ``R0``) of
    ``Lin(Q)``: ``feas(state)`` = sum over minimal remaining ``v`` of ``feas(state + v)``, 0
    when ``F(R0)`` fails, 1 at the full set (exact by the argument of :func:`enum_prefix`).
    Time ``O(#states * w * (T_v + T_F))``, memory ``O(#states * m)``.
    """
    P = setup.poset
    n = len(P)
    total = count_downsets(n, _predmasks(n, P.succs))
    model = DepModel(setup)
    if model.trivial:
        return total, total
    if model.hopeless:
        return total, 0
    succs = _pinned(setup, model, pins)
    if succs is None:
        return total, 0
    st = _Prefix(model, succs)
    if not st.root_ok():
        return total, 0
    preds = st.preds
    full = (1 << n) - 1
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
                ok, tok, pushed = st.place(v)
                if ok:
                    c += feas(done | low)
                st.unplace(v, tok, pushed)
        memo[k] = c
        return c

    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 4 * n + 100))
    try:
        return total, feas(0)
    finally:
        sys.setrecursionlimit(old)


def count_split(setup: Setup, pins: bool = True) -> tuple[int, int, int]:
    """(|Lin(P)|, |LinFeas(P)|, #leaves): down-set DP counts summed over the split leaves."""
    P = setup.poset
    n = len(P)
    total = count_downsets(n, _predmasks(n, P.succs))
    model = DepModel(setup)
    if model.trivial:
        return total, total, 1
    if model.hopeless:
        return total, 0, 0
    succs = _pinned(setup, model, pins)
    if succs is None:
        return total, 0, 0
    feas = leaves = 0
    for succ in _split_leaves(setup, model, succs):
        leaves += 1
        feas += count_downsets(n, _predmasks(n, succ))
    return total, feas, leaves


# --------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------


def _flag(opts: dict, key: str, default: bool) -> bool:
    v = opts.get(key)
    return default if v is None else str(v).lower() not in ("0", "false", "no", "off")


PIN_OPT = {"pins": "1 (default for all but filter) = add static reads-from pin edges first; 0 = off"}


@register
class OpusDepFilter(LinEnumerator):
    name = "opus55-o-filter"
    description = "Varol-Rotem over Lin(P) + exact joint reads-from/term-matching fixed-L test"
    capabilities = CAPS
    options = PIN_OPT

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_filter(setup, _flag(self.opts, "pins", False))


@register
class OpusDepPrune(LinEnumerator):
    name = "opus55-o-prune"
    description = "prefix DFS over pinned poset, cut by antitone F on certain precedences, witness reuse"
    capabilities = CAPS
    options = PIN_OPT

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_prefix(setup, memo=False, pins=_flag(self.opts, "pins", True))


@register
class OpusDepMemo(LinEnumerator):
    name = "opus55-o-memo"
    description = "opus55-o-prune + memo of dead (down-set, certain-precedence) states"
    capabilities = CAPS
    options = PIN_OPT

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_prefix(setup, memo=True, pins=_flag(self.opts, "pins", True))


@register
class OpusDepSplit(LinEnumerator):
    name = "opus55-o-split"
    description = "partition LinFeas(P) into Lin(Q_i) by branching on witness-breaking pairs; VR per part"
    capabilities = CAPS
    options = PIN_OPT

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return enum_split(setup, _flag(self.opts, "pins", True))


@register
class OpusDepDPCount(LinCounter):
    name = "opus55-o-dpcount"
    description = "feasible count by memoized DP over (down-set, certain-precedence) states"
    capabilities = CAPS
    options = PIN_OPT

    def count(self, setup: Setup) -> CountResult:
        total, feas = count_dp(setup, _flag(self.opts, "pins", True))
        return CountResult(total, feas if setup.features().observed_reads else None, "opus-dep-state-dp")


@register
class OpusDepSplitCount(LinCounter):
    name = "opus55-o-splitcount"
    description = "feasible count: down-set DP counts summed over the split partition"
    capabilities = CAPS
    options = PIN_OPT

    def count(self, setup: Setup) -> CountResult:
        total, feas, _ = count_split(setup, _flag(self.opts, "pins", True))
        return CountResult(total, feas if setup.features().observed_reads else None, "opus-dep-split-dp")
