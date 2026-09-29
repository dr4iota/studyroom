"""``fable51-s-dp`` / ``fable51-s-count``: ranked enumeration and counting over the chain-positions DP.

Idea
----
The poset has bounded width: ``N`` thread chains plus ``K`` singleton sync chains
(``setup.poset.chains``). A down-set is a vector of per-chain positions, so there are at
most ``prod(len(chain) + 1)`` states, and ``ways(state)`` (the number of ways to finish
from that down-set) is a DP over the down-set lattice, restricted here to the states
reachable from the empty down-set. Cut nodes (``common.cut_segments``: full ``at``
barriers and anything else every step is ordered against) split the poset into
intervals whose counts multiply, which shrinks the state space further.

``fable51-s-count`` returns ``prod_i ways_i(empty)``. ``fable51-s-dp`` enumerates the
linearizations in **lexicographic order of the chain-label sequence** (which chain
advances next, chains in ``P.chains`` order) by an explicit-stack DFS over the
down-set lattice; every DFS branch leads to at least one output (a down-set always
extends), so there are no dead ends. The DP table gives *rank/unrank*, so the options
``start``, ``stop`` and ``step`` select ranks ``start, start+step, ... < stop`` (as in
``range``); with ``step > 1`` every output is unranked directly.

Cost
----
Per output ``O(n * w)`` worst case for the DFS (``w = N + K`` chains examined at each
of ``n`` levels, amortised over the shared prefix), ``O(n * w)`` per unranked output.
Memory: the DP tables, at most ``prod(len(chain)+1)`` states (exponential in the width,
polynomial in ``n`` for fixed width). Deterministic, lazy. No adjacency property.
"""

from __future__ import annotations

import sys
from typing import Callable, Iterator

from abio.lin.api import CountResult, LinCounter, LinEnumerator
from abio.model import Setup
from abio.poset import Linearization
from abio.registry import register

from .common import SYNC, SubPoset, cut_segments

State = tuple[int, ...]
Moves = list[tuple[int, State]]


def table(P) -> tuple[Callable[[State], int], Callable[[State], Moves], State]:
    """``(ways, moves, empty)`` for a :class:`TracePoset` or :class:`SubPoset`."""
    chains = P.chains
    chain_of, pos_in_chain, preds = P.chain_of, P.pos_in_chain, P.preds
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * len(P) + 1000))
    mv_memo: dict[State, Moves] = {}
    w_memo: dict[State, int] = {}

    def moves(state: State) -> Moves:
        out = mv_memo.get(state)
        if out is None:
            out = []
            for c, j in enumerate(state):
                if j == len(chains[c]):
                    continue
                x = chains[c][j]
                if all(pos_in_chain[p] < state[chain_of[p]] for p in preds[x]):
                    out.append((x, state[:c] + (j + 1,) + state[c + 1:]))
            mv_memo[state] = out
        return out

    def ways(state: State) -> int:
        w = w_memo.get(state)
        if w is None:
            nxt = moves(state)
            w = sum(ways(s) for _, s in nxt) if nxt else 1
            w_memo[state] = w
        return w

    return ways, moves, tuple(0 for _ in chains)


def count_segments(setup: Setup) -> int:
    P = setup.poset
    total = 1
    for seg in cut_segments(P):
        if len(seg) > 1:
            ways, _, empty = table(SubPoset(P, seg))
            total *= ways(empty)
    return total


def unrank(P, r: int, ways, moves, empty: State) -> tuple[list[int], list[list], list[State]]:
    """The DFS stack of the linearization of rank ``r``: ``(order, frames, states)``."""
    order: list[int] = []
    frames: list[list] = []  # [moves, index]
    states: list[State] = []
    state = empty
    for _ in range(len(P)):
        mv = moves(state)
        idx = 0
        while r >= ways(mv[idx][1]):
            r -= ways(mv[idx][1])
            idx += 1
        frames.append([mv, idx])
        x, state = mv[idx]
        order.append(x)
        states.append(state)
    return order, frames, states


def linear_extensions(P, start: int = 0, stop: int | None = None, step: int = 1) -> Iterator[Linearization]:
    n = len(P)
    ways, moves, empty = table(P)
    total = ways(empty)
    stop = total if stop is None else min(stop, total)
    if step < 1:
        raise ValueError("step must be >= 1")
    if start >= stop:
        return
    if n == 0:
        yield ()
        return
    if step > 1:
        for r in range(start, stop, step):
            yield tuple(unrank(P, r, ways, moves, empty)[0])
        return
    order, stack, states = unrank(P, start, ways, moves, empty)
    yield tuple(order)
    remaining = stop - start - 1
    while stack and remaining > 0:
        mv, idx = stack[-1]
        idx += 1
        if idx < len(mv):
            stack[-1][1] = idx
            x, st = mv[idx]
            order[-1], states[-1] = x, st
            while len(order) < n:
                mv2 = moves(st)
                stack.append([mv2, 0])
                x, st = mv2[0]
                order.append(x)
                states.append(st)
            yield tuple(order)
            remaining -= 1
        else:
            stack.pop()
            order.pop()
            states.pop()


@register
class FableSyncDP(LinEnumerator):
    name = "fable51-s-dp"
    description = "lexicographic by chain labels over the positions DP; rank/unrank (start/stop/step)"
    capabilities = SYNC
    options = {"start": "first rank to output (default 0)", "stop": "stop before this rank", "step": "rank stride (default 1)"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        o = self.opts
        return linear_extensions(setup.poset, int(o.get("start", 0)), o.get("stop"), int(o.get("step", 1)))


@register
class FableSyncCount(LinCounter):
    name = "fable51-s-count"
    description = "exact count: positions DP per cut-node segment, product over segments"
    capabilities = SYNC

    def count(self, setup: Setup) -> CountResult:
        return CountResult(count_segments(setup), None, "fable51-s-count")
