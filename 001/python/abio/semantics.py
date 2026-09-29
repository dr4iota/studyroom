"""Register semantics interpreter (premise.md §2.4) and full-schedule enumeration.

A **full schedule** is a linearization ``order`` plus an effect order ``effects`` (all
action ids). The effect order is admissible for ``order`` iff distinct instants
``π(x) ∈ [pos(x), pos(x.done)]`` exist in that order; the greedy test walks the effects
with a running instant ``t := max(t + ε, pos(x))`` and requires ``t < pos(x.done)``
(positions are distinct integers, so ``≤`` and ``<`` coincide up to ε).

Only the atomic register with distinct effect points is implemented. RCW returns the
old content (``rcw_result: old``) or ``ok``/``fail`` (``flag``); both are supported.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Iterator, Sequence

from . import terms as T
from .model import Action, Setup
from .poset import Linearization


@dataclass
class Schedule:
    """A full schedule and what it produces (formats.md §4)."""

    order: Linearization
    effects: tuple[str, ...]
    results: dict[str, T.Term]  # read/rcw id -> value returned (rcw: the old content)
    final: list[T.Term]  # per block
    consistent: bool  # every observed result matched
    meta: dict = field(default_factory=dict)


class _State:
    """Mutable execution state with an undo trail (used by the DFS)."""

    def __init__(self, setup: Setup) -> None:
        self.setup = setup
        self.acts = setup.actions
        self.flag = setup.semantics.rcw_result == "flag"
        self.content: list[T.Term] = list(setup.init)
        self.results: dict[str, T.Term] = {}
        self.mismatches = 0
        self.trail: list[tuple[str, int, T.Term, bool]] = []

    def value(self, aid: str) -> T.Term:
        """``Ref`` lookup: a read's result, or a write/rcw's content (its evaluated data)."""
        a = self.acts[aid]
        if a.kind == "read":
            return self.results[aid]
        return self.content_of(a)

    def content_of(self, a: Action) -> T.Term:
        return T.Unk(a.id) if a.data is None else T.substitute(a.data, self.value)

    def apply(self, a: Action) -> bool:
        """Take effect; return True iff the action's observed result (if any) matches."""
        b, old = a.block, self.content[a.block]
        ok = True
        if a.kind == "read":
            self.results[a.id] = old
            ok = a.observed is None or a.observed == old
        elif a.kind == "write":
            self.content[b] = self.content_of(a)
        else:  # rcw
            self.results[a.id] = old
            success = old == T.substitute(a.expect, self.value)
            if success:
                self.content[b] = self.content_of(a)
            if a.observed is not None:
                ok = a.observed == ("ok" if success else "fail") if self.flag else a.observed == old
        self.mismatches += not ok
        self.trail.append((a.id, b, old, ok))
        return ok

    def undo(self) -> None:
        aid, b, old, ok = self.trail.pop()
        self.content[b] = old
        self.results.pop(aid, None)
        self.mismatches -= not ok

    def snapshot(self, order: Linearization, effects: Sequence[str]) -> Schedule:
        return Schedule(tuple(order), tuple(effects), dict(self.results), list(self.content), self.mismatches == 0)


def intervals(setup: Setup, order: Sequence[int]) -> dict[str, tuple[int, int]]:
    """Action id -> (pos(start), pos(done)) under ``order``."""
    P = setup.poset
    pos = P.positions(order)
    return {a: (pos[P.start_node[a]], pos[P.done_node[a]]) for a in setup.actions}


def check_effects(setup: Setup, order: Sequence[int], effects: Sequence[str]) -> list[str]:
    """Errors (empty iff ``effects`` is an admissible effect order for ``order``)."""
    iv = intervals(setup, order)
    if sorted(effects) != sorted(iv):
        return ["effects is not a permutation of all action ids"]
    t = -1
    for x in effects:
        s, e = iv[x]
        t = max(t, s)
        if t >= e:
            return [f"{x} cannot take effect after the previous effects (interval {s}..{e})"]
    return []


def execute(setup: Setup, order: Sequence[int], effects: Sequence[str]) -> Schedule:
    """Run the register semantics along an admissible effect order."""
    errs = check_effects(setup, order, effects)
    if errs:
        raise ValueError("; ".join(errs))
    st = _State(setup)
    for x in effects:
        st.apply(setup.actions[x])
    return st.snapshot(tuple(order), effects)


def iter_schedules(setup: Setup, order: Sequence[int], *, prune: bool = True) -> Iterator[Schedule]:
    """Every admissible effect order for ``order`` (brute force, exponential).

    With ``prune`` (default) only consistent schedules are produced, and branches are
    cut as soon as an observed result mismatches.
    """
    iv = intervals(setup, order)
    acts = list(setup.actions.values())
    s = [iv[a.id][0] for a in acts]
    e = [iv[a.id][1] for a in acts]
    n = len(acts)
    placed = [False] * n
    effects: list[str] = []
    st = _State(setup)

    def rec(t: int) -> Iterator[Schedule]:
        if len(effects) == n:
            yield st.snapshot(tuple(order), effects)
            return
        for i in range(n):
            if placed[i]:
                continue
            nt = max(t, s[i])
            if nt >= e[i]:
                continue
            if any(not placed[j] and j != i and e[j] <= nt for j in range(n)):
                continue  # placing i at nt would leave j unable to take effect
            ok = st.apply(acts[i])
            if ok or not prune:
                placed[i] = True
                effects.append(acts[i].id)
                yield from rec(nt)
                effects.pop()
                placed[i] = False
            st.undo()

    yield from rec(-1)


def is_feasible(setup: Setup, order: Sequence[int]) -> bool:
    """Does ``order`` admit at least one full schedule matching every observation?"""
    return next(iter_schedules(setup, order, prune=True), None) is not None


def random_effects(setup: Setup, order: Sequence[int], rng: random.Random) -> list[str]:
    """A random admissible effect order: a uniform random point in each interval, sorted."""
    iv = intervals(setup, order)
    pts = sorted((rng.uniform(s, e), x) for x, (s, e) in iv.items())
    return [x for _, x in pts]


def observed_value_doc(v: Any) -> Any:
    return v if isinstance(v, str) else T.to_value(v)
