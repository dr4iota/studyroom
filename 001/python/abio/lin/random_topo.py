"""Cheap sampler: repeatedly place a uniformly random minimal element.

Always valid, ``O(n + edges)`` per sample, but **not** uniform over ``Lin(P)`` (it
favours linearizations whose prefixes have few minimal elements). Variant (a) of
LIN-SAMPLE; the generator uses it for the hidden schedule.
"""

from __future__ import annotations

import random

from ..capabilities import Capabilities
from ..model import Setup
from ..poset import Linearization
from ..registry import register
from .api import LinSampler


def random_linearization(setup: Setup, rng: random.Random) -> Linearization:
    P = setup.poset
    indeg = [len(p) for p in P.preds]
    avail = [x for x in range(len(P)) if indeg[x] == 0]
    order = []
    while avail:
        x = avail.pop(rng.randrange(len(avail)))
        order.append(x)
        for y in P.succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                avail.append(y)
    return tuple(order)


@register
class RandomTopo(LinSampler):
    name = "random-topo"
    description = "random minimal element each step (valid, not uniform)"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=False)
    distribution = "any"

    def sample(self, setup: Setup, rng: random.Random) -> Linearization:
        return random_linearization(setup, rng)
