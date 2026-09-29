"""``fable-o-filter``: Gray-code generation of ``Lin(P)`` with an incremental per-block filter.

Idea
----
Generate every linearization with the Pruesse–Ruskey listing (``contrib.linear_fable51_1.base_sync.pr``,
consecutive outputs differ by one or two adjacent transpositions) and keep the feasible
ones. Feasibility is the conjunction of per-block verdicts (per-block independence),
and a verdict is a function of the block's interval relation ``x ≺ y iff e(x) < s(y)``.
An adjacent transposition of nodes ``u, v`` changes the relative order of ``u`` and
``v`` only, so it changes ``≺`` only if ``u`` and ``v`` are a done endpoint and a start
endpoint of two tracked actions (writes or observed reads) of the same block. Hence
after each step only the blocks touched by such a swap are re-tested; all other
verdicts are carried over. Both fixed-``L`` tests of ``common`` are available
(``--opt test=slots`` (default) or ``test=auto``). Every ``L`` is generated once, so no
duplicates; the leaf test is exact, so no infeasible output.

Cost
----
Per candidate ``O(1)`` amortised for the Gray step plus ``O(n)`` to materialise and
diff the tuple, plus a block test when a swap touches a block (``O(m_b^2)`` plus the
write-order DFS for ``slots``; ``O(m_b · |configs| · F_b)`` for ``auto``). There is no
pruning, so the cost per *output* is ``|Lin(P)| / |LinFeas(P)|`` candidates; this is
the algorithm to use when most linearizations are feasible, and the worst one when few
are. Memory ``O(n)`` plus the ``O(n^2)``-bit closure of the Gray code. Deterministic,
lazy.
"""

from __future__ import annotations

from typing import Iterator

from abio.lin.api import LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register
from contrib.linear_fable51_1.base_sync.pr import linear_extensions as gray

from .common import OBS, Model, block_feasible_auto, block_feasible_slots


def feasible_linearizations(setup: Setup, test: str = "slots") -> Iterator[Linearization]:
    P = setup.poset
    n = len(P)
    model = Model(setup)
    if model.impossible:
        return
    blocks = model.blocks
    block_test = block_feasible_slots if test == "slots" else block_feasible_auto
    if not blocks:
        yield from gray(P)
        return
    node_block, node_is_start = model.node_block, model.node_is_start
    verdict = [True] * len(blocks)
    prev: tuple | None = None
    for o in gray(P):
        if prev is None:
            dirty = set(range(len(blocks)))
        else:
            dirty = set()
            starts: set[int] = set()
            dones: set[int] = set()
            for i in range(n):
                x = o[i]
                if x != prev[i] and node_block[x] >= 0:
                    (starts if node_is_start[x] else dones).add(node_block[x])
            dirty = starts & dones
        if dirty:
            pos = P.positions(o)
            for bi in dirty:
                verdict[bi] = block_test(blocks[bi], pos)
        prev = o
        if all(verdict):
            yield o


@register
class FableObsFilter(LinEnumerator):
    name = "fable-o-filter"
    description = "Pruesse-Ruskey Gray code of Lin(P), re-testing only the blocks a swap touches"
    capabilities = OBS
    options = {"test": "fixed-L block test: slots (default) or auto"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return feasible_linearizations(setup, str(self.opts.get("test", "slots")))
