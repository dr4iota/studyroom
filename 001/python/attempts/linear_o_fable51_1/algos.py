"""Registered algorithms for task ``linear``, case ``o``."""

from __future__ import annotations

from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

from .core import (
    Model,
    count_feasible,
    count_interleavings,
    feasible_linearizations,
    has_observations,
    interleavings,
    thread_chains,
)

CAPS = Capabilities(rcw=False, sync=False, observed_reads=True)


@register
class StateSetEnumerator(LinEnumerator):
    name = "fable51_1-o-enum"
    description = "DFS over thread interleavings, pruned by the set of run states some effect-point choice can reach"
    capabilities = CAPS
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        if not has_observations(setup):
            yield from interleavings(thread_chains(setup))
        else:
            yield from feasible_linearizations(Model(setup))


@register
class StateSetCounter(LinCounter):
    name = "fable51_1-o-count"
    description = "|Lin(P)| as a multinomial; |LinFeas(P)| by the state-set walk memoised on (chain positions, state set)"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        chains = thread_chains(setup)
        total = count_interleavings(chains)
        if not has_observations(setup):
            return CountResult(linearizations=total, feasible=total, method="multinomial")
        feasible = count_feasible(Model(setup))
        return CountResult(linearizations=total, feasible=feasible, method="multinomial+memo-dfs")
