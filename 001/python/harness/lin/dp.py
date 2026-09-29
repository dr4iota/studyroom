"""Positions DP over down-sets (visions.md §2.1): exact count and exact uniform sampling.

A down-set of ``P`` is described by how far it has advanced along each chain of
``P.chains`` (the thread chains plus one singleton chain per sync node), so the state
space has at most ``prod(len(chain) + 1)`` states — ``(n/N + 1)^N`` for ``N`` threads,
times ``2^K`` for sync nodes. ``ways(state)`` is the number of ways to finish from a
down-set; ``|Lin(P)| = ways(empty)``. Sampling walks from the empty down-set choosing
each next node with probability ``ways(next) / ways(state)``.
"""

from __future__ import annotations

import random
import sys
from functools import lru_cache
from typing import Callable, Iterator

from ..capabilities import Capabilities
from ..model import Setup
from ..poset import Linearization
from ..registry import register
from .api import CountResult, LinCounter, LinSampler

State = tuple[int, ...]


def _table(setup: Setup) -> tuple[Callable[[State], int], Callable[[State], list[tuple[int, State]]]]:
    P = setup.poset
    chains = P.chains
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * len(P) + 1000))

    def moves(state: State) -> list[tuple[int, State]]:
        out = []
        for c, j in enumerate(state):
            if j == len(chains[c]):
                continue
            x = chains[c][j]
            if all(P.pos_in_chain[p] < state[P.chain_of[p]] for p in P.preds[x]):
                out.append((x, state[:c] + (j + 1,) + state[c + 1 :]))
        return out

    @lru_cache(maxsize=None)
    def ways(state: State) -> int:
        nxt = moves(state)
        return sum(ways(s) for _, s in nxt) if nxt else 1

    return ways, moves


def count_linearizations(setup: Setup) -> int:
    ways, _ = _table(setup)
    return ways(tuple(0 for _ in setup.poset.chains))


@register
class PositionsDPCounter(LinCounter):
    name = "dp-positions"
    description = "exact count by DP over per-chain positions"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=False)

    def count(self, setup: Setup) -> CountResult:
        return CountResult(count_linearizations(setup), None, "dp-positions")


@register
class PositionsDPSampler(LinSampler):
    name = "dp-uniform"
    description = "exact uniform sampling from the positions-DP table"
    capabilities = Capabilities(rcw=True, sync=True, observed_reads=False)
    distribution = "uniform"

    def sample(self, setup: Setup, rng: random.Random) -> Linearization:
        return next(self.samples(setup, rng, 1))

    def samples(self, setup: Setup, rng: random.Random, n: int) -> Iterator[Linearization]:
        ways, moves = _table(setup)
        start = tuple(0 for _ in setup.poset.chains)
        for _ in range(n):
            state, order = start, []
            while True:
                nxt = moves(state)
                if not nxt:
                    break
                r = rng.randrange(ways(state))
                for x, s in nxt:
                    r -= ways(s)
                    if r < 0:
                        break
                order.append(x)
                state = s
            yield tuple(order)
