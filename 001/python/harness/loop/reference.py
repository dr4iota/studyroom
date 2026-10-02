"""Reference loop algorithms: unroll to ``P_n`` and use the validated oracles.

Exact for every ``n``, but the cost grows with ``n``, so they are oracles for small ``n``
only. ``dp-positions`` gives ``|Lin(P_n)|``; the down-set solver gives the possibility
sets. These are harness code, not attempts.
"""

from __future__ import annotations

from ..capabilities import Capabilities
from ..lin.dp import count_linearizations
from ..loops import LoopSetup, project
from ..registry import register
from ..solve.downset import solve_downset
from .api import LoopCounter, LoopOutcomes, LoopSolver


def oracle_count(setup: LoopSetup, n: int) -> int:
    return count_linearizations(setup.unroll(n))


def oracle_solve(setup: LoopSetup, n: int) -> LoopOutcomes:
    o = solve_downset(setup.unroll(n))
    res = project(o.results)
    for r in setup.reads():
        res.setdefault(r, set())
    return LoopOutcomes(res, {b: set(v) for b, v in o.final.items()})


@register
class UnrollCounter(LoopCounter):
    name = "loop-unroll-count"
    description = "reference: unroll to P_n, positions DP"
    capabilities = Capabilities(sync=True)

    def count(self, setup: LoopSetup, n: int) -> int:
        return oracle_count(setup, n)


@register
class UnrollSolver(LoopSolver):
    name = "loop-unroll-solve"
    description = "reference: unroll to P_n, down-set solver"
    capabilities = Capabilities(sync=True)

    def solve(self, setup: LoopSetup, n: int) -> LoopOutcomes:
        return oracle_solve(setup, n)
