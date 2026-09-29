"""Brute-force oracle (visions.md §3.1): enumerate ``L``, then every effect order ``π``.

Runs the register semantics on every full schedule and collects values. Supports every
feature; exponential, intended for small setups and as the reference in differential
tests. Unknown contents are free symbols, so no enumeration of ``θ`` is needed.
"""

from __future__ import annotations

from ..model import Setup
from ..poset import Linearization
from ..registry import register
from ..lin.backtrack import linear_extensions
from ..semantics import iter_schedules
from .api import Collector, Outcomes, Solver, SolverCapabilities


@register
class BruteForce(Solver):
    name = "brute"
    description = "oracle: every linearization x every effect order"
    capabilities = SolverCapabilities(
        rcw=True, sync=True, observed_reads=True,
        modes=frozenset({"all", "fixed"}), witnesses=True,
    )
    options = {"witnesses": "record witness schedules (default true)"}

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        col = Collector(setup, "all" if linearization is None else "fixed", bool(self.opts.get("witnesses", True)))
        orders = linear_extensions(setup) if linearization is None else [linearization]
        for order in orders:
            for sched in iter_schedules(setup, order, prune=True):
                col.add(sched)
        return col.out
