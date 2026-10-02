"""Loop APIs: answers for a loop setup (``harness.loops``) at a given iteration count.

The iteration count ``n`` is an input and may be arbitrarily large (e.g. ``10**9``).
Implementations must not assume ``n`` is small.

- :class:`LoopCounter`: ``count(setup, n)`` returns ``|Lin(P_n)|`` exactly, as an ``int``.
- :class:`LoopSolver`: ``solve(setup, n)`` returns :class:`LoopOutcomes`, the exact
  possibility sets of ``P_n``. A body read's set is the union over its ``n``
  instances; every read of the loop setup, and every block, gets an entry.

Capabilities: ``sync`` (sync points, plain and per-iteration) is the only extension;
``rcw`` and ``observed_reads`` are always False for loops.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from .. import terms as T
from ..loops import LoopSetup
from ..registry import Algorithm


@dataclass
class LoopOutcomes:
    results: dict[str, set[T.Term]] = field(default_factory=dict)  # loop-setup read id -> Poss_n
    final: dict[int, set[T.Term]] = field(default_factory=dict)  # block -> Poss_n


class LoopCounter(Algorithm):
    category: ClassVar[str] = "loop-count"

    @abstractmethod
    def count(self, setup: LoopSetup, n: int) -> int: ...


class LoopSolver(Algorithm):
    category: ClassVar[str] = "loop-solver"

    @abstractmethod
    def solve(self, setup: LoopSetup, n: int) -> LoopOutcomes: ...
