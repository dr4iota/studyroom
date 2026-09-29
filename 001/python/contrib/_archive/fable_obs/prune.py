"""``fable-o-prune``: backtracking over minimal elements with slot-criterion prefix pruning.

Idea
----
Generate ``L`` left to right (Varol–Rotem style: repeatedly append a node whose
predecessors are placed). A prefix fixes the positions of the placed endpoints; treat
every unplaced endpoint as ``+∞``. The interval relation of the prefix,
``x ≺ y iff e(x) < s(y)``, then contains exactly the pairs (completed ``x``, ``y``
started later or not yet started), and it is a **subset of the relation of every
completion** of the prefix, because appending steps can only turn ``+∞`` into a finite
position that is larger than every placed one. Feasibility is anti-monotone in ``≺``
(more forced precedences, fewer admissible ``π``), so if the prefix problem is
infeasible under the slot criterion of ``common`` (which is exact for any interval
relation, complete or not) no completion is feasible: the subtree is cut. The relation
grows only when a ``done`` endpoint of a tracked action (a write or an observed read of
a block with observations) is placed, so the test runs only at those steps and only on
that block (per-block independence). At a leaf the prefix relation is the full one, so
the criterion is exact and every output is feasible; the search visits each linear
extension of the poset at most once, so there are no duplicates.

Cost
----
Per node placed: ``O(w)`` bookkeeping (``w`` = number of available nodes) plus, at the
done step of a tracked action, one block test: ``O(m_b^2)`` to build the relation plus
the write-order DFS (exponential in the block's writes in the worst case, memoised,
usually a handful of states). Per output ``O(n)`` to materialise the tuple. A rejected
prefix costs one block test and cuts its whole subtree. Memory ``O(n)`` for the
search plus one transient memo per test. Deterministic, lazy, iterative (explicit
stack). No adjacency property.
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import OBS, Model, block_feasible_slots


def feasible_linearizations(setup: Setup) -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    pos = [-1] * n
    if not all(block_feasible_slots(bl, pos) for bl in model.blocks):
        return
    if n == 0:
        yield ()
        return
    node_block, kind, blocks = model.node_block, P.kind, model.blocks
    indeg = [len(p) for p in P.preds]
    avail = {x for x in range(n) if indeg[x] == 0}
    order: list[int] = []
    freed: list[list[int]] = []
    stack: list[list] = [[sorted(avail), 0]]

    def undo() -> None:
        x = order.pop()
        pos[x] = -1
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
        pos[x] = len(order)
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
        if bi >= 0 and kind[x] == "done" and not block_feasible_slots(blocks[bi], pos):
            undo()
            continue
        if len(order) == n:
            yield tuple(order)
            undo()
            continue
        stack.append([sorted(avail), 0])


@register
class FableObsPrune(LinEnumerator):
    name = "fable-o-prune"
    description = "backtracking; prefixes pruned by the slot criterion at every tracked done step"
    capabilities = OBS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup)
