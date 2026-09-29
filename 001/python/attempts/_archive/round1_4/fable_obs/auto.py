"""``fable-o-auto``: backtracking with the register automaton as incremental prefix state.

Idea
----
Same left-to-right generation as ``fable-o-prune``, but the feasibility state is the
per-block **automaton** of ``common`` (the set of configurations ``(E, c)`` reachable
after the prefix: which in-flight tracked actions have taken effect and the current
content). The state is a pure function of the prefix, so it is pushed on a stack when
a tracked endpoint is placed and popped on backtrack; nothing is recomputed. A prefix
is cut when

* a block's configuration set becomes empty (an observed read completed without ever
  being able to return its value): exact necessary condition on the prefix, and exact
  at a leaf (``common`` docstring), so every output is feasible; or
* the *supplier lookahead* fails: an observed read ``r`` (value ``v``) of the block
  that has not completed needs some way to still return ``v``: a configuration where
  ``r`` already took effect, or one where a write with content ``v`` is still pending,
  or a not-yet-started write with content ``v``, or (for a not-yet-started ``r``) a
  configuration whose current content is ``v``. If none exists, no completion can
  satisfy ``r``: in any completion ``r`` reads the last write before it, which is
  either already effected (then the content would have to be ``v`` now, and no
  pending write of value ``v`` could change that) or effected later (then it is
  pending now or unstarted). Sound pruning; it catches "observed ``init`` but a
  write already completed" and "the only ``v``-writer is gone" long before the read
  completes.

Each linear extension of the poset is visited at most once, so no duplicates.

Cost
----
Per node placed ``O(w)`` plus, at a tracked endpoint, one automaton step:
``O(|configs| · F_b)`` for a start (closure) or ``O(|configs|)`` for a done, plus the
lookahead ``O(|configs| · m_b)``; ``|configs| <= 2^{F_b} · V_b`` with ``F_b`` the number
of in-flight tracked actions of the block, so polynomial for bounded in-flight width.
Per output ``O(n)`` for the tuple; a rejected prefix costs one step and cuts its
subtree. Memory ``O(n · Σ_b |configs_b|)`` for the state stack. Deterministic, lazy,
iterative.
"""

from __future__ import annotations

from typing import Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

from .common import OBS, Block, Model, initial_state, step_block


def lookahead(bl: Block, state: tuple[int, frozenset[int]], unstarted: int, unstarted_vals: list[int]) -> bool:
    """Can every not-yet-completed observed read of the block still be satisfied?"""
    inflight, configs = state
    V, val, wmask, rmask = bl.nvals, bl.val, bl.wmask, bl.rmask
    need = rmask & (inflight | unstarted)
    if not need:
        return True
    effected_any = 0
    contents = 0  # bitmask over content indices
    pending_vals = 0  # bitmask over content indices of pending writes in some config
    for cf in configs:
        E, c = divmod(cf, V)
        effected_any |= E
        contents |= 1 << c
        pend = inflight & wmask & ~E
        while pend:
            low = pend & -pend
            pend ^= low
            pending_vals |= 1 << val[low.bit_length() - 1]
    bits = need
    while bits:
        low = bits & -bits
        bits ^= low
        r = low.bit_length() - 1
        v = val[r]
        if effected_any & low or unstarted_vals[v] > 0 or pending_vals >> v & 1:
            continue
        if unstarted & low and contents >> v & 1:
            continue
        return False
    return True


def feasible_linearizations(setup: Setup) -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    blocks = model.blocks
    node_block, node_local, node_is_start = model.node_block, model.node_local, model.node_is_start
    states = [initial_state(bl) for bl in blocks]
    unstarted = [(1 << bl.m) - 1 for bl in blocks]
    unstarted_vals = [[bin(bl.writes_with[v]).count("1") for v in range(bl.nvals)] for bl in blocks]
    if not all(lookahead(bl, states[i], unstarted[i], unstarted_vals[i]) for i, bl in enumerate(blocks)):
        return
    if n == 0:
        yield ()
        return
    indeg = [len(p) for p in P.preds]
    avail = {x for x in range(n) if indeg[x] == 0}
    order: list[int] = []
    freed: list[list[int]] = []
    saved: list[tuple] = []  # (bi, old state) per placed node; bi = -1 when untracked
    stack: list[list] = [[sorted(avail), 0]]

    def undo() -> None:
        x = order.pop()
        bi, old = saved.pop()
        if bi >= 0:
            states[bi] = old
            if node_is_start[x]:
                unstarted[bi] |= 1 << node_local[x]
                bl = blocks[bi]
                if bl.wmask >> node_local[x] & 1:
                    unstarted_vals[bi][bl.val[node_local[x]]] += 1
        for y in freed.pop():
            avail.discard(y)
        for y in P.succs[x]:
            indeg[y] += 1
        avail.add(x)

    while stack:
        fr = stack[-1]
        cands, idx = fr
        if idx == len(cands):
            stack.pop()
            if order:
                undo()
            continue
        fr[1] = idx + 1
        x = cands[idx]
        order.append(x)
        avail.discard(x)
        fl = []
        for y in P.succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                fl.append(y)
                avail.add(y)
        freed.append(fl)
        bi = node_block[x]
        ok = True
        if bi >= 0:
            bl = blocks[bi]
            i = node_local[x]
            old = states[bi]
            saved.append((bi, old))
            if node_is_start[x]:
                unstarted[bi] &= ~(1 << i)
                if bl.wmask >> i & 1:
                    unstarted_vals[bi][bl.val[i]] -= 1
            new = step_block(old, i, node_is_start[x], bl)
            if new is None:
                ok = False
            else:
                states[bi] = new
                ok = lookahead(bl, new, unstarted[bi], unstarted_vals[bi])
        else:
            saved.append((-1, None))
        if not ok:
            undo()
            continue
        if len(order) == n:
            yield tuple(order)
            undo()
            continue
        stack.append([sorted(avail), 0])


@register
class FableObsAuto(LinEnumerator):
    name = "fable-o-auto"
    description = "backtracking; register automaton as incremental prefix state, with supplier lookahead"
    capabilities = OBS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup)
