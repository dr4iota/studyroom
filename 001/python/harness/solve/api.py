"""Solver API: pluggable possibility-set solvers (SOLVE-READ, SOLVE-FINAL, CHECK).

A solver computes, **exactly** ("no more, no less", spec §5):

* ``Poss(r)`` for every read and every RCW ``r`` (for an RCW: the old content it found);
* ``Poss(b)`` for every block ``b`` (its final content);
* whether any feasible full schedule exists at all (CHECK).

Two modes (``SolverCapabilities.modes``):

``all``    ``Poss`` over every linearization ``L ∈ Lin(P)`` and every effect order
           (levels 1+2). ``solve(setup)`` is called with ``linearization=None``.
``fixed``  ``Poss_L`` for one given linearization (level 2 only).
           ``solve(setup, linearization=L)``; ``L`` is a valid linearization of ``setup``.

Values are terms (``harness.terms``). Unknown write contents are free symbols (``Unk``),
unknown initial contents are ``Init``; they are compared structurally (spec §4).
An observed result is matched structurally too.

Output contract (:class:`Outcomes`):

* ``consistent`` is False iff no feasible full schedule exists; then ``results`` and
  ``final`` must be empty.
* otherwise ``results`` has one entry per read/RCW id and ``final`` one per block, each
  a non-empty set; an observed result's set is exactly ``{observed}``;
* ``witnesses``, when the solver has ``witnesses=True``, holds one feasible
  :class:`harness.semantics.Schedule` per ``(id, value)`` and per ``(block, value)`` pair,
  with ``meta["certifies"] = {"id": .., "value": ..}`` or ``{"block": .., "value": ..}``.
  Validators re-execute them to check soundness cheaply.

Capabilities (``SolverCapabilities``, extends ``harness.capabilities.Capabilities``):
``rcw``, ``sync`` and ``observed_reads`` as documented there, plus
``modes`` and ``witnesses``. The CLI never calls a solver outside its capabilities.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from .. import terms as T
from ..capabilities import Capabilities
from ..model import Setup
from ..poset import Linearization
from ..registry import Algorithm
from ..semantics import Schedule


@dataclass(frozen=True)
class SolverCapabilities(Capabilities):
    modes: frozenset[str] = frozenset({"all"})  # subset of {"all", "fixed"}
    witnesses: bool = False

    def summary(self) -> str:
        return f"{super().summary()} modes={','.join(sorted(self.modes))} witnesses={'yes' if self.witnesses else 'no'}"


@dataclass
class Outcomes:
    """Solver output (the ``outcomes`` document of formats.md §5)."""

    mode: str  # all | fixed
    consistent: bool
    results: dict[str, set[T.Term]] = field(default_factory=dict)  # read/rcw id -> Poss
    final: dict[int, set[T.Term]] = field(default_factory=dict)  # block -> Poss
    witnesses: list[Schedule] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


class Solver(Algorithm):
    """Base class of solvers. Implement :meth:`solve`."""

    category: ClassVar[str] = "solver"
    capabilities: ClassVar[SolverCapabilities] = SolverCapabilities()

    @abstractmethod
    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        """Return exact possibility sets; ``linearization`` given iff mode ``fixed``."""


class Collector:
    """Helper: accumulate consistent schedules (and optional witnesses) into an Outcomes."""

    def __init__(self, setup: Setup, mode: str, keep_witnesses: bool) -> None:
        self.setup = setup
        self.out = Outcomes(mode, False)
        self.keep = keep_witnesses

    def add(self, s: Schedule) -> None:
        """Record one *consistent* schedule."""
        o = self.out
        o.consistent = True
        for aid, v in s.results.items():
            vals = o.results.setdefault(aid, set())
            if v not in vals:
                vals.add(v)
                if self.keep:
                    self._witness(s, {"id": aid, "value": T.to_value(v)})
        for b, v in enumerate(s.final):
            vals = o.final.setdefault(b, set())
            if v not in vals:
                vals.add(v)
                if self.keep:
                    self._witness(s, {"block": b, "value": T.to_value(v)})

    def _witness(self, s: Schedule, certifies: dict) -> None:
        self.out.witnesses.append(Schedule(s.order, s.effects, s.results, s.final, True, {"certifies": certifies}))
