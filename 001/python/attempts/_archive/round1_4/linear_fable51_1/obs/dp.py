"""``fable51-o-dp`` / ``fable51-o-count``: exact DP over (down-set, component automaton states); no dead ends.

Idea
----
A prefix of ``L`` is a down-set ``D`` of the poset, described by per-chain positions
(``setup.poset.chains``; without sync these are the thread chains). Feasibility of the
completions of a prefix depends on the prefix only through ``D`` and, per data-flow
component, the automaton state ``(inflight, configs)`` of ``common``: the set of
reachable register configurations including the classes of live feeder reads and of
pending writes. The transition on a node is **deterministic** in the ``L``-step (the
nondeterminism of the effect points is inside the configuration *set*), so every ``L``
is exactly one path through the state graph and

    ways(D, S) = Σ_{x minimal in P \\ D, S' = step(S, x) non-empty} ways(D ∪ {x}, S')
    ways(P, S) = 1

counts the feasible linearizations exactly (``ways(∅, S_0) = |LinFeas(P)|``): the
automaton is exact at a complete ``L`` (``common`` docstring) and a path whose state
dies has no feasible completion. ``fable51-o-count`` returns that number, plus
``|Lin(P)|`` from the positions DP. ``fable51-o-dp`` enumerates by DFS over the same
graph in lexicographic order of the chain sequence, descending only into children with
``ways > 0``: **every branch leads to an output**, no dead-end work at all. The tables
also give rank/unrank, so ``start``/``stop``/``step`` select ranks as ``range`` does.

What carries over from constant data: everything except the state, which is now
per component rather than per block and carries value classes (lemma 1-3 in
``common``); with constant data it is the same DP as ``fable-o-dp``.

Cost
----
Precomputation: one DP over the reachable states ``(D, S)``; a state costs ``O(w)``
move generation plus ``O(Σ_comp |configs| · F)`` for the automaton step. The number of
states is at most (#down-sets) × (#distinct automaton states), exponential in the
width ``N`` and in the in-flight width per component, polynomial in ``n`` for fixed
width. Per output ``O(n · w)`` worst case for the DFS (no rejected candidates), plus
``O(n)`` for the tuple; ``O(n · w)`` per unranked output. Memory: the memo tables
(``ways`` and the children lists), i.e. the number of reachable states times ``O(w)``.
Deterministic, lazy. With no observations the automaton is trivial and this is the
plain positions DP.
"""

from __future__ import annotations

import sys
from typing import Callable, Iterator

from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.lin.dp import count_linearizations
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

from .common import DEP, Model, initial_state, step

State = tuple  # (chain positions, per-component automaton states)
Children = list  # [(node, child state)]


def table(setup: Setup) -> tuple[Callable[[State], int], Callable[[State], Children], State]:
    """``(ways, children, root)`` for the feasible-linearization DP."""
    P = setup.poset
    model = Model(setup)
    chains, chain_of, pos_in_chain, preds = P.chains, P.chain_of, P.pos_in_chain, P.preds
    comps, node_comp, node_local, node_is_start = model.comps, model.node_comp, model.node_local, model.node_is_start
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * len(P) + 1000))
    mv_memo: dict[tuple, list] = {}
    ch_memo: dict[State, Children] = {}
    w_memo: dict[State, int] = {}

    def moves(D: tuple) -> list:
        out = mv_memo.get(D)
        if out is None:
            out = []
            for c, j in enumerate(D):
                if j == len(chains[c]):
                    continue
                x = chains[c][j]
                if all(pos_in_chain[p] < D[chain_of[p]] for p in preds[x]):
                    out.append((x, D[:c] + (j + 1,) + D[c + 1:]))
            mv_memo[D] = out
        return out

    def children(state: State) -> Children:
        out = ch_memo.get(state)
        if out is None:
            D, S = state
            out = []
            for x, D2 in moves(D):
                ci = node_comp[x]
                if ci < 0:
                    out.append((x, (D2, S)))
                    continue
                new = step(comps[ci], S[ci], node_local[x], node_is_start[x])
                if new is not None:
                    out.append((x, (D2, S[:ci] + (new,) + S[ci + 1:])))
            ch_memo[state] = out
        return out

    def ways(state: State) -> int:
        w = w_memo.get(state)
        if w is None:
            kids = children(state)
            if kids:
                w = sum(ways(s) for _, s in kids)
            else:
                w = 1 if all(j == len(chains[c]) for c, j in enumerate(state[0])) else 0
            w_memo[state] = w
        return w

    root = (tuple(0 for _ in chains), tuple(initial_state(c) for c in comps))
    if model.impossible:
        w_memo[root] = 0
    return ways, children, root


def unrank(n: int, r: int, ways, children, root: State) -> tuple[list[int], list[list], list[State]]:
    """The DFS stack of the feasible linearization of rank ``r``: ``(order, frames, states)``."""
    order: list[int] = []
    frames: list[list] = []
    states: list[State] = []
    state = root
    for _ in range(n):
        kids = [(x, s) for x, s in children(state) if ways(s) > 0]
        idx = 0
        while r >= ways(kids[idx][1]):
            r -= ways(kids[idx][1])
            idx += 1
        frames.append([kids, idx])
        x, state = kids[idx]
        order.append(x)
        states.append(state)
    return order, frames, states


def feasible_linearizations(setup: Setup, start: int = 0, stop: int | None = None, step_: int = 1) -> Iterator[Linearization]:
    n = len(setup.poset)
    ways, children, root = table(setup)
    total = ways(root)
    stop = total if stop is None else min(int(stop), total)
    if step_ < 1:
        raise ValueError("step must be >= 1")
    if start >= stop:
        return
    if n == 0:
        yield ()
        return
    if step_ > 1:
        for r in range(start, stop, step_):
            yield tuple(unrank(n, r, ways, children, root)[0])
        return
    order, stack, states = unrank(n, start, ways, children, root)
    yield tuple(order)
    remaining = stop - start - 1
    while stack and remaining > 0:
        kids, idx = stack[-1]
        idx += 1
        if idx < len(kids):
            stack[-1][1] = idx
            x, st = kids[idx]
            order[-1], states[-1] = x, st
            while len(order) < n:
                kids2 = [(x, s) for x, s in children(st) if ways(s) > 0]
                stack.append([kids2, 0])
                x, st = kids2[0]
                order.append(x)
                states.append(st)
            yield tuple(order)
            remaining -= 1
        else:
            stack.pop()
            order.pop()
            states.pop()


@register
class FableDepDP(LinEnumerator):
    name = "fable51-o-dp"
    description = "DP over (down-set, component automata); zero dead ends; rank/unrank (start/stop/step)"
    capabilities = DEP
    options = {"start": "first rank to output (default 0)", "stop": "stop before this rank", "step": "rank stride (default 1)"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        o = self.opts
        return feasible_linearizations(setup, int(o.get("start", 0)), o.get("stop"), int(o.get("step", 1)))


@register
class FableDepCount(LinCounter):
    name = "fable51-o-count"
    description = "exact |Lin(P)| (positions DP) and |LinFeas(P)| (DP over down-set x component automata)"
    capabilities = DEP

    def count(self, setup: Setup) -> CountResult:
        total = count_linearizations(setup)
        if not setup.features().observed_reads:
            return CountResult(total, None, "fable51-o-count")
        ways, _, root = table(setup)
        return CountResult(total, ways(root), "fable51-o-count")
