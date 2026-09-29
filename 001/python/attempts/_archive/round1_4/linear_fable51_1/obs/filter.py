"""``fable51-o-filter``: Gray-code generation of ``Lin(P)`` with an incremental per-component filter.

Idea
----
Generate every linearization with the Pruesse–Ruskey listing (``attempts._archive.round1_4.linear_fable51_1.base_sync.pr``,
consecutive outputs differ by one or two adjacent transpositions) and keep the
feasible ones. Feasibility is the conjunction of per-component verdicts (merging
lemma, ``common``), and a verdict is a function of the component's interval relation
``x ≺ y iff e(x) < s(y)``. An adjacent transposition of nodes ``u, v`` changes the
relative order of ``u`` and ``v`` only, so it changes a component's ``≺`` only if ``u``
and ``v`` are a done endpoint and a start endpoint of two tracked actions of that
component. Hence after each step only the components touched by such a swap are
re-tested; all other verdicts are carried over. Both fixed-``L`` tests of ``common``
are available (``--opt test=rf`` (default) or ``test=auto``). Every ``L`` is generated
once, so no duplicates; the leaf test is exact, so no infeasible output.

What carries over: everything, with "block" replaced by "component" (a swap of a
read's done on block ``b'`` with a write's start on block ``b`` now matters when
``b'`` feeds ``b``).

Cost
----
Per candidate ``O(1)`` amortised for the Gray step plus ``O(n)`` to materialise and
diff the tuple, plus a component test when a swap touches it (``O(m^2)`` plus the
reads-from DFS for ``rf``; ``O(m · |configs| · F)`` for ``auto``). There is no pruning,
so the cost per *output* is ``|Lin(P)| / |LinFeas(P)|`` candidates; this is the
algorithm to use when most linearizations are feasible, and the worst one when few
are. Memory ``O(n)`` plus the ``O(n^2)``-bit closure of the Gray code. Deterministic,
lazy.
"""

from __future__ import annotations

from typing import Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from attempts._archive.round1_4.linear_fable51_1.base_sync.pr import linear_extensions as gray

from .common import DEP, Model, comp_feasible_auto, comp_feasible_rf


def feasible_linearizations(setup: Setup, test: str = "rf") -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    comps = model.comps
    comp_test = comp_feasible_rf if test == "rf" else comp_feasible_auto
    if not comps:
        yield from gray(P)
        return
    node_comp, node_is_start = model.node_comp, model.node_is_start
    verdict = [True] * len(comps)
    prev: tuple | None = None
    for o in gray(P):
        if prev is None:
            dirty = set(range(len(comps)))
        else:
            starts: set[int] = set()
            dones: set[int] = set()
            for i in range(n):
                x = o[i]
                if x != prev[i] and node_comp[x] >= 0:
                    (starts if node_is_start[x] else dones).add(node_comp[x])
            dirty = starts & dones
        if dirty:
            pos = P.positions(o)
            for ci in dirty:
                verdict[ci] = comp_test(comps[ci], pos)
        prev = o
        if all(verdict):
            yield o


@register
class FableDepFilter(LinEnumerator):
    name = "fable51-o-filter"
    description = "Pruesse-Ruskey Gray code of Lin(P), re-testing only the components a swap touches"
    capabilities = DEP
    options = {"test": "fixed-L component test: rf (default, reads-from) or auto (automaton)"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup, str(self.opts.get("test", "rf")))
