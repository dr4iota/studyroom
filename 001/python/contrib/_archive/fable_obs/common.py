"""Shared model and the two fixed-``L`` feasibility tests behind the ``fable-o-*`` algorithms.

Setting (premise.md §2.4-2.6, atomic register, distinct effect points)
------------------------------------------------------------------------
Fix a linearization ``L``; every action ``x`` has an interval ``[s(x), e(x)]`` of
positions. An effect order ``π`` is admissible iff it is a linear extension of the
**interval order** ``x ≺ y  iff  e(x) < s(y)``:

* if ``π`` is a linear extension, the greedy check of ``abio.semantics`` (``t :=
  max(t, s(x))``, require ``t < e(x)``) never fails, because ``t = max_{k<=i} s(x_k)`` and
  ``t >= e(x_i)`` would mean ``s(x_k) > e(x_i)`` for some earlier ``x_k``, i.e.
  ``x_i ≺ x_k`` with ``x_k`` before ``x_i``;
* conversely the greedy walk assigns non-decreasing instants, so an admissible ``π``
  never puts ``y`` before ``x`` when ``e(x) < s(y)``.

Three facts used by every algorithm here:

1. **Per-block independence.** A block's contents depend only on ``π`` restricted to
   that block's actions, and any family of per-block linear extensions of ``≺`` merges
   into one global linear extension (``≺`` is a partial order and the union of ``≺``
   with per-block chains is acyclic, because a cycle through other blocks' actions
   would shortcut, by transitivity of ``≺``, into a cycle inside one block). So
   ``LinFeas`` is the intersection of the per-block feasible sets, and only blocks
   with at least one observed read matter.
2. **Unobserved reads never matter.** Given a linear extension of ``≺`` on the other
   actions of the block, an unobserved read can always be inserted (same acyclicity
   argument), and its value is unconstrained. So a block's problem has as elements
   only its writes and its *observed* reads ("tracked" actions).
3. **Structural values.** A write's content is a term (a constant or its own unknown
   symbol); an observed value ``v`` can only come from a write whose content equals
   ``v`` structurally, or from ``init(b)`` when that equals ``v``. Contents are indexed
   0..V-1 per block; an observed value outside that set makes every ``L`` infeasible.

Two exact fixed-``L`` tests, both differentially tested against ``abio.semantics``:

``is_feasible_fast`` (slot criterion, :func:`block_feasible_slots`)
    Let ``σ = w_1 < ... < w_k`` be the order of the block's writes in ``π`` (``w_0`` =
    init) and say a read ``r`` is *in slot i* when ``w_i < r < w_{i+1}`` in ``π``; then
    ``r`` returns the content of ``w_i``. Claim: given ``σ`` (a linear extension of
    ``≺`` on the writes), an assignment of slots to the observed reads extends to an
    admissible ``π`` **iff** (a) ``content(w_i) = obs(r)`` for ``r`` in slot ``i``, (b)
    no placed write ``w_j`` with ``j <= i`` has ``r ≺ w_j`` and no later write ``w_j``
    (``j > i``) has ``w_j ≺ r``, and (c) ``r' ≺ r`` implies ``slot(r') <= slot(r)``.
    Proof: the slot structure is a total preorder (rank ``2i`` for ``w_i``, ``2i+1`` for
    slot-``i`` reads); the required ``π`` exists iff "preorder ∪ ≺" is acyclic; since ≺
    is transitive any cycle shortens to one whose ≺-edges each go backwards or stay
    within one rank, and (b)+(c) exclude backward edges while same-rank edges are
    between reads (a partial order, so acyclic on their own). Because reads impose no
    constraint on ``σ``, and putting a read in the *earliest* admissible slot only
    loosens (c) for its successors, the slot assignment can be greedy for a fixed
    ``σ``: walk ``σ`` and, after each write, place every unplaced read that fits the
    open slot, iterating to a fixpoint. A read that is still unplaced when a write
    ``w`` with ``r ≺ w`` is appended can never be placed. The write order ``σ`` is
    searched (a DFS over the down-sets of ``≺`` restricted to the writes, memoised on
    ``(placed writes, placed reads)``, which determines the future once the greedy
    fixpoint is reached), so the test is exponential in the number of writes of one
    block in the worst case (the underlying problem, linearizability of a register with
    repeated values, is NP-complete, Gibbons–Korach 1997) but polynomial when ``≺``
    orders the block's writes, and in practice tiny.

``is_feasible_auto`` (automaton criterion, :func:`block_feasible_auto`)
    Walk ``L`` and simulate the register nondeterministically: between two consecutive
    steps any in-flight tracked actions may take effect, in any order (the greedy check
    lets several effects share the integer instant ``t``; ``x`` may take effect at any
    ``t`` with ``s(x) <= t < e(x)``). A *configuration* is ``(E, c)``: the set ``E`` of
    in-flight actions that already took effect and the current content ``c``. After a
    start step the set of reachable configurations is closed under "one pending action
    takes effect" (a write sets ``c``; an observed read may take effect only when ``c``
    equals its observation); at ``done(x)`` the configurations with ``x`` not yet in
    ``E`` are dropped. ``L`` is feasible iff the set stays non-empty (at the end every
    tracked action has taken effect consistently, which is exactly a consistent ``π``;
    and every consistent ``π`` is traced by the simulation). Cost ``O(n + Σ_b m_b ·
    |configs_b| · F_b)`` with ``F_b`` the in-flight width of block ``b``: polynomial in
    ``n`` for bounded in-flight actions per block.

The automaton also serves as an incremental **prefix state** (``fable-o-auto``,
``fable-o-dp``): its configurations after a prefix of ``L`` depend only on that prefix.
The slot criterion serves as a **prefix pruning test** (``fable-o-prune``): with
unplaced endpoints at ``+∞`` the relation ``≺`` of a prefix is a subset of the relation
of every completion, so an infeasible prefix problem has no feasible completion.
"""

from __future__ import annotations

from typing import Sequence

from abio.capabilities import Capabilities
from abio.model import Setup
from abio.semantics import is_feasible as _oracle  # noqa: F401  (re-exported for tests)

OBS = Capabilities(rcw=False, sync=True, observed_reads=True)

INF = 1 << 40


class Block:
    """The tracked actions of one block: its writes and its observed reads.

    Local indices ``0..m-1``; ``val[i]`` is the content index a write leaves, or the
    observed content index of a read (``-1`` when the observation matches no possible
    content). ``init`` is the content index of the initial content.
    """

    def __init__(self, setup: Setup, b: int) -> None:
        P = setup.poset
        self.b = b
        acts = [a for a in setup.actions.values() if a.block == b and (a.kind == "write" or a.observed is not None)]
        contents = {setup.init[b]: 0}
        for a in acts:
            if a.kind == "write":
                contents.setdefault(setup.static_content(a.id), len(contents))
        self.nvals = len(contents)
        self.init = 0
        self.m = len(acts)
        self.ids = [a.id for a in acts]
        self.is_write = [a.kind == "write" for a in acts]
        self.wmask = sum(1 << i for i, a in enumerate(acts) if a.kind == "write")
        self.rmask = ((1 << self.m) - 1) & ~self.wmask
        self.start = [P.start_node[a.id] for a in acts]
        self.done = [P.done_node[a.id] for a in acts]
        self.val = [contents[setup.static_content(a.id)] if a.kind == "write" else contents.get(a.observed, -1) for a in acts]
        self.impossible = any(v < 0 for v in self.val)
        # writes per content index, as local bitmasks
        self.writes_with = [0] * self.nvals
        for i, a in enumerate(acts):
            if a.kind == "write":
                self.writes_with[self.val[i]] |= 1 << i
        self.n_obs = self.m - bin(self.wmask).count("1")


class Model:
    """The tracked blocks of a setup and the node -> (block, local index, is_start) map."""

    def __init__(self, setup: Setup) -> None:
        self.setup = setup
        P = setup.poset
        n = len(P)
        observed_blocks = sorted({a.block for a in setup.actions.values() if a.observed is not None})
        self.blocks = [Block(setup, b) for b in observed_blocks]
        self.impossible = any(bl.impossible for bl in self.blocks)
        self.node_block = [-1] * n
        self.node_local = [0] * n
        self.node_is_start = [False] * n
        for bi, bl in enumerate(self.blocks):
            for i in range(bl.m):
                self.node_block[bl.start[i]] = bi
                self.node_local[bl.start[i]] = i
                self.node_is_start[bl.start[i]] = True
                self.node_block[bl.done[i]] = bi
                self.node_local[bl.done[i]] = i

    def feasible_slots(self, order: Sequence[int]) -> bool:
        if self.impossible:
            return False
        pos = self.setup.poset.positions(order)
        return all(block_feasible_slots(bl, pos) for bl in self.blocks)

    def feasible_auto(self, order: Sequence[int]) -> bool:
        if self.impossible:
            return False
        pos = self.setup.poset.positions(order)
        return all(block_feasible_auto(bl, pos) for bl in self.blocks)


# --------------------------------------------------------------------------- slot criterion


def block_feasible_slots(bl: Block, pos: Sequence[int]) -> bool:
    """Slot criterion for one block; ``pos[node] = -1`` means "not placed yet" (``+∞``).

    Exact for a complete order; for a prefix it is a sound necessary condition.
    """
    if bl.impossible:
        return False
    m = bl.m
    if bl.rmask == 0:
        return True
    s = [pos[x] if pos[x] >= 0 else INF for x in bl.start]
    e = [pos[x] if pos[x] >= 0 else INF for x in bl.done]
    # pre[x] = mask of y with y ≺ x (e[y] < s[x]); suc[x] = mask of y with x ≺ y
    pre = [0] * m
    suc = [0] * m
    for x in range(m):
        sx = s[x]
        if sx == INF:
            mask = 0
            for y in range(m):
                if e[y] != INF and y != x:
                    mask |= 1 << y
        else:
            mask = 0
            for y in range(m):
                if e[y] < sx:
                    mask |= 1 << y
        pre[x] = mask
        bits = mask
        while bits:
            low = bits & -bits
            suc[low.bit_length() - 1] |= 1 << x
            bits ^= low
    wmask, rmask, val, writes_with = bl.wmask, bl.rmask, bl.val, bl.writes_with
    reads = [r for r in range(m) if not bl.is_write[r]]
    writes = [w for w in range(m) if bl.is_write[w]]
    dead: set[tuple[int, int]] = set()

    def greedy(placed_w: int, placed_r: int, content: int) -> int:
        unplaced_w = wmask & ~placed_w
        changed = True
        while changed:
            changed = False
            for r in reads:
                bit = 1 << r
                if placed_r & bit or val[r] != content:
                    continue
                if suc[r] & placed_w or pre[r] & unplaced_w or pre[r] & rmask & ~placed_r:
                    continue
                placed_r |= bit
                changed = True
        return placed_r

    def rec(placed_w: int, placed_r: int, content: int) -> bool:
        placed_r = greedy(placed_w, placed_r, content)
        if placed_w == wmask:
            return placed_r == rmask
        key = (placed_w, placed_r)
        if key in dead:
            return False
        remaining = wmask & ~placed_w
        unplaced_r = rmask & ~placed_r
        # every unplaced read still needs a supplier among the remaining writes
        bits = unplaced_r
        ok = True
        while bits:
            low = bits & -bits
            bits ^= low
            if not writes_with[val[low.bit_length() - 1]] & remaining:
                ok = False
                break
        if ok:
            for w in writes:
                bit = 1 << w
                if not remaining & bit or pre[w] & remaining or pre[w] & unplaced_r:
                    continue
                if rec(placed_w | bit, placed_r, val[w]):
                    return True
        dead.add(key)
        return False

    return rec(0, 0, bl.init)


# --------------------------------------------------------------------------- automaton criterion


def closure(configs, inflight: int, bl: Block) -> frozenset[int]:
    """Close a configuration set under "one pending tracked action takes effect".

    A configuration is encoded as ``E * nvals + content``.
    """
    V, val, wmask = bl.nvals, bl.val, bl.wmask
    out = set(configs)
    stack = list(configs)
    while stack:
        cf = stack.pop()
        E, c = divmod(cf, V)
        pend = inflight & ~E
        while pend:
            low = pend & -pend
            pend ^= low
            i = low.bit_length() - 1
            if wmask & low:
                nc = (E | low) * V + val[i]
            elif val[i] == c:
                nc = (E | low) * V + c
            else:
                continue
            if nc not in out:
                out.add(nc)
                stack.append(nc)
    return frozenset(out)


def step_block(state: tuple[int, frozenset[int]], i: int, is_start: bool, bl: Block) -> tuple[int, frozenset[int]] | None:
    """Advance one block's automaton state ``(inflight, configs)`` over an endpoint of local action ``i``.

    Returns None when no configuration survives (the prefix is infeasible).
    """
    inflight, configs = state
    bit = 1 << i
    if is_start:
        inflight |= bit
        return inflight, closure(configs, inflight, bl)
    V = bl.nvals
    keep = frozenset(cf - bit * V for cf in configs if (cf // V) & bit)
    if not keep:
        return None
    return inflight & ~bit, keep


def initial_state(bl: Block) -> tuple[int, frozenset[int]]:
    return 0, frozenset({bl.init})


def block_feasible_auto(bl: Block, pos: Sequence[int]) -> bool:
    """Automaton criterion for one block, over a complete order given by positions."""
    if bl.impossible:
        return False
    if bl.rmask == 0:
        return True
    events = sorted([(pos[bl.start[i]], i, True) for i in range(bl.m)] + [(pos[bl.done[i]], i, False) for i in range(bl.m)])
    state = initial_state(bl)
    for _, i, is_start in events:
        state = step_block(state, i, is_start, bl)
        if state is None:
            return False
    return True


# --------------------------------------------------------------------------- public tests


def is_feasible_fast(setup: Setup, order: Sequence[int]) -> bool:
    """Fixed-``L`` feasibility by the slot criterion (see the module docstring)."""
    return Model(setup).feasible_slots(order)


def is_feasible_auto(setup: Setup, order: Sequence[int]) -> bool:
    """Fixed-``L`` feasibility by the automaton criterion (see the module docstring)."""
    return Model(setup).feasible_auto(order)
