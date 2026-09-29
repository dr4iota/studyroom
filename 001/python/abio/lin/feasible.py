"""Observation-aware reference algorithms (capability ``observed_reads``).

They wrap the base algorithms with the brute-force feasibility test
``abio.semantics.is_feasible`` (exponential in the number of actions per linearization),
so they are oracles for small setups, not scalable algorithms.
"""

from __future__ import annotations

import random
from typing import Iterator

from ..capabilities import Capabilities
from ..model import Setup
from ..poset import Linearization
from ..registry import register
from ..semantics import is_feasible
from .api import CountResult, LinCounter, LinEnumerator, LinSampler
from .backtrack import linear_extensions
from .dp import PositionsDPSampler

FULL = Capabilities(rcw=True, sync=True, observed_reads=True)


@register
class FeasibleBacktrack(LinEnumerator):
    name = "backtrack-feasible"
    description = "backtrack, keeping only linearizations feasible for the observations"
    capabilities = FULL

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        observed = setup.features().observed_reads
        for order in linear_extensions(setup):
            if not observed or is_feasible(setup, order):
                yield order


@register
class EnumerationCounter(LinCounter):
    name = "enum-count"
    description = "count by enumerating (also counts feasible linearizations)"
    capabilities = FULL

    def count(self, setup: Setup) -> CountResult:
        observed = setup.features().observed_reads
        total = feasible = 0
        for order in linear_extensions(setup):
            total += 1
            if observed and is_feasible(setup, order):
                feasible += 1
        return CountResult(total, feasible if observed else None, "enumeration")


@register
class RejectionSampler(LinSampler):
    name = "rejection"
    description = "uniform over feasible linearizations: dp-uniform + rejection"
    capabilities = FULL
    distribution = "uniform-feasible"
    options = {"max_tries": "give up after this many rejected samples per draw (default 100000)"}

    def sample(self, setup: Setup, rng: random.Random) -> Linearization:
        return next(self.samples(setup, rng, 1))

    def samples(self, setup: Setup, rng: random.Random, n: int) -> Iterator[Linearization]:
        max_tries = int(self.opts.get("max_tries", 100000))
        source = PositionsDPSampler().samples(setup, rng, n * max_tries)
        for _ in range(n):
            for _, order in zip(range(max_tries), source):
                if is_feasible(setup, order):
                    yield order
                    break
            else:
                raise RuntimeError(f"no feasible linearization found in {max_tries} tries")
