"""``fable51-o-prune``: backtracking over minimal elements with reads-from prefix pruning.

Idea
----
Generate ``L`` left to right. A prefix fixes the positions of the placed endpoints;
treat every unplaced endpoint as ``+∞``. The interval relation of the prefix,
``x ≺ y iff e(x) < s(y)``, contains exactly the pairs (completed ``x``, ``y`` started
later or not yet started) and is a **subset of the relation of every completion**
(appending steps only turns ``+∞`` into a finite position larger than every placed
one). Feasibility is anti-monotone in ``≺``: the admissible ``π`` are the linear
extensions of ``≺`` and the values of a schedule depend on ``π`` alone, so more forced
precedences leave fewer consistent ``π``. Hence if the prefix problem is infeasible
under the reads-from criterion of ``common`` (exact for any interval relation: its
proof only uses that ``≺`` is an interval order, which the prefix intervals are) no
completion is feasible and the subtree is cut. The relation grows only when a
``done`` endpoint of a tracked action is placed, so the test runs only at those steps
and only on that action's component. At a leaf the prefix relation is the full one, so
the criterion is exact and every output is feasible; each linear extension is visited
at most once, so there are no duplicates.

What carries over: the prefix argument is unchanged from the constant-data round; the
criterion itself is the new goal-directed reads-from search (with term matching),
run per component rather than per block.

Cost
----
Per node placed ``O(w)`` bookkeeping plus, at the done step of a tracked action, one
component test: ``O(m^2)`` to build the relation plus the reads-from DFS (exponential
in the number of alternative sources per goal in the worst case, polynomial when
values are distinct, in practice a handful of nodes). Per output ``O(n)`` to
materialise the tuple. A rejected prefix costs one test and cuts its subtree. Memory
``O(n)`` for the search plus one transient digraph per test. Deterministic, lazy,
iterative (explicit stack).
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import DEP, Model, comp_feasible_rf


def feasible_linearizations(setup: Setup) -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    pos = [-1] * n
    if not all(comp_feasible_rf(c, pos) for c in model.comps):
        return
    if n == 0:
        yield ()
        return
    node_comp, kind, comps = model.node_comp, P.kind, model.comps
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
        ci = node_comp[x]
        if ci >= 0 and kind[x] == "done" and not comp_feasible_rf(comps[ci], pos):
            undo()
            continue
        if len(order) == n:
            yield tuple(order)
            undo()
            continue
        stack.append([sorted(avail), 0])


@register
class FableDepPrune(LinEnumerator):
    name = "fable51-o-prune"
    description = "backtracking; prefixes pruned by the reads-from criterion (term matching) at every tracked done step"
    capabilities = DEP

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup)
