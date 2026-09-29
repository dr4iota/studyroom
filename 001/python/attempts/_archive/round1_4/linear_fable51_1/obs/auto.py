"""``fable51-o-auto``: backtracking with the component automaton as incremental prefix state.

Idea
----
Generate ``L`` left to right (append a node whose predecessors are placed). The
feasibility state is, per data-flow component, the automaton of ``common``: the set
of configurations ``(E, c, rk, wk)`` reachable after the prefix. It is a pure function
of the prefix, so it is pushed on a stack when a tracked endpoint is placed and popped
on backtrack. A prefix is cut when

* a component's configuration set becomes empty (an observed read completed without
  ever being able to return its value, or a feeder read's class never let a later
  write carry the observed value): an exact necessary condition on the prefix, and
  exact at a leaf (``common`` docstring), so every output is feasible; or
* the *supplier lookahead* fails: an observed read ``r`` (value ``v``) that has not
  completed needs some way to still return ``v``: a configuration where ``r`` already
  took effect, or an in-flight write that is pending in some configuration and has
  an option ``v`` (a write whose expression can match ``v``), or a not-yet-started
  write with an option ``v``, or (for a not-yet-started ``r``) a configuration whose
  content class is ``v``. If none exists no completion satisfies ``r``: in any
  completion ``r`` reads the last write before it, which is either already effected
  (then the content would be ``v`` now, and closure would have effected ``r`` too) or
  effected later (then it is pending now or unstarted, and its content can be ``v``
  only if it has that option). Sound; with read-dependent data it is weaker than
  before (an option is a static possibility), but still cuts "the only writer that
  can match is gone" early.

Assumptions carried over from the constant-data round: the merging lemma (so the
components are independent) and prefix-monotonicity of the automaton; the per-block
factoring is replaced by per-component states (``common`` docstring, lemma 1-3).
Each linear extension of the poset is visited at most once, so no duplicates.

Cost
----
Per node placed ``O(w)`` (``w`` = available nodes) plus, at a tracked endpoint, one
automaton step: ``O(|configs| · F)`` for a start (closure; ``F`` = in-flight tracked
actions of the component) or ``O(|configs|)`` for a done, plus the lookahead
``O(|configs| + m)``. ``|configs| <= 2^F · Π_b (|Vals_b|+1) · Π_r (|G_r|+2) · ...`` in the
worst case, polynomial for bounded in-flight width and bounded live feeder reads. Per
output ``O(n)`` for the tuple; a rejected prefix costs one step and cuts its subtree.
Memory ``O(n · Σ_comp |configs|)`` for the state stack. Deterministic, lazy, iterative.
"""

from __future__ import annotations

from typing import Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

from .common import DEP, NONE, Comp, Model, State, initial_state, step


def lookahead(comp: Comp, state: State, unstarted: int) -> bool:
    """Can every not-yet-completed observed read of the component still be satisfied?"""
    inflight, configs = state
    obs, C, blk = comp.obs, comp.C, comp.blk
    need = [i for i in range(comp.m) if obs[i] != NONE and (inflight | unstarted) >> i & 1]
    if not need:
        return True
    effected_any = 0
    pending_any = 0
    contents = [0] * comp.nb  # bitmask of content classes seen per local block
    for cf in configs:
        E = cf[0]
        effected_any |= E
        pending_any |= inflight & ~E
        for b in range(comp.nb):
            c = cf[C + b]
            if c >= 0:
                contents[b] |= 1 << c
    for i in need:
        v = obs[i]
        if effected_any >> i & 1 or comp.suppliers[i] & (pending_any | unstarted):
            continue
        if unstarted >> i & 1 and contents[blk[i]] >> v & 1:
            continue
        return False
    return True


def feasible_linearizations(setup: Setup) -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    comps = model.comps
    node_comp, node_local, node_is_start = model.node_comp, model.node_local, model.node_is_start
    states = [initial_state(c) for c in comps]
    unstarted = [(1 << c.m) - 1 for c in comps]
    if not all(lookahead(c, states[i], unstarted[i]) for i, c in enumerate(comps)):
        return
    if n == 0:
        yield ()
        return
    indeg = [len(p) for p in P.preds]
    avail = {x for x in range(n) if indeg[x] == 0}
    order: list[int] = []
    freed: list[list[int]] = []
    saved: list[tuple] = []  # (ci, old state) per placed node; ci = -1 when untracked
    stack: list[list] = [[sorted(avail), 0]]

    def undo() -> None:
        x = order.pop()
        ci, old = saved.pop()
        if ci >= 0:
            states[ci] = old
            if node_is_start[x]:
                unstarted[ci] |= 1 << node_local[x]
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
        ci = node_comp[x]
        ok = True
        if ci >= 0:
            comp = comps[ci]
            i = node_local[x]
            old = states[ci]
            saved.append((ci, old))
            if node_is_start[x]:
                unstarted[ci] &= ~(1 << i)
            new = step(comp, old, i, node_is_start[x])
            if new is None:
                ok = False
            else:
                states[ci] = new
                ok = lookahead(comp, new, unstarted[ci])
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
class FableDepAuto(LinEnumerator):
    name = "fable51-o-auto"
    description = "backtracking; component automaton (classes of contents and feeder reads) as prefix state, with supplier lookahead"
    capabilities = DEP

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup)
