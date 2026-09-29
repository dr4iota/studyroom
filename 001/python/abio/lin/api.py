"""Linearization API: pluggable enumerators, counters and samplers (LIN-ENUM/COUNT/SAMPLE).

There are two main API families, because "list every linearization" and "how many are
there" have very different algorithms and costs:

1. :class:`LinEnumerator` — **all permutations.** Produces every linearization.
2. :class:`LinCounter` — **counting only.** Produces the number ``|Lin(P)|`` without
   listing them (and optionally the number of *feasible* ones).

A third, smaller family, :class:`LinSampler`, draws random linearizations (randomized
linearization, premise.md §4 LIN-SAMPLE).

What is being enumerated / counted / sampled
--------------------------------------------
``Lin(P)`` is the set of linear extensions of the trace poset ``P`` (premise.md §2.3),
taken on the quotient by ``at`` events: the nodes are the endpoints, the
``before``/``after`` events and the virtual steps ``sync.k`` (see ``abio.poset``).
Every algorithm receives a validated :class:`abio.model.Setup`; the poset is
``setup.poset``.

A linearization is a ``Linearization = tuple[int, ...]``: node indices into
``setup.poset.names``, each exactly once, earliest first. Use
``setup.poset.to_names(order)`` for step names.

How the capabilities change the answer
--------------------------------------
* base problem (reads/writes, ``K = 0``, no observations): ``Lin(P)`` is the set of
  interleavings of the ``N`` thread chains (a multinomial coefficient).
* ``sync``: the ``sync.k`` nodes and their edges constrain ``P``; ``Lin(P)`` shrinks
  (``at`` barriers cut it into products). An unused sync point is an isolated node and
  *enlarges* it; that is a property of the input, not of the algorithm.
* ``observed_reads``: the algorithm works on ``LinFeas(P) ⊆ Lin(P)``, the linearizations
  that admit at least one full schedule consistent with every observed result
  (``abio.semantics.is_feasible``). Enumerators then yield only feasible ones, counters
  report ``feasible``, samplers sample from the feasible ones.
* ``rcw``: an RCW is an ordinary action for ``P``; it matters only when feasibility is
  evaluated (observed RCW results).

The CLI refuses to run an algorithm on a setup using an unsupported feature, so an
implementation may assume the setup is within its declared capabilities.
"""

from __future__ import annotations

import random
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Iterator

from ..model import Setup
from ..poset import Linearization
from ..registry import Algorithm


class LinEnumerator(Algorithm):
    """Enumerate linearizations (LIN-ENUM).

    Contract for :meth:`enumerate`:

    * yields every element of ``Lin(P)`` — or of ``LinFeas(P)`` when the setup has
      observed results — **exactly once**, each a valid linearization;
    * is lazy: the caller may stop early (``--limit``), so do not precompute the list;
    * is deterministic for a given setup (order may be algorithm-specific).

    Class attribute ``gray_code``: True if consecutive outputs always differ by one
    transposition of two adjacent positions (Pruesse–Ruskey style); validators check it.
    """

    category: ClassVar[str] = "lin-enum"
    gray_code: ClassVar[bool] = False

    @abstractmethod
    def enumerate(self, setup: Setup) -> Iterator[Linearization]: ...


@dataclass
class CountResult:
    """Result of a counter (the ``count`` document of formats.md §6).

    linearizations  ``|Lin(P)|``; None if the counter does not compute it
    feasible        ``|LinFeas(P)|`` given observations; None if not computed. Counters
                    with ``observed_reads`` must fill it when the setup has observations.
    method          short tag, e.g. ``dp-positions``, ``enumeration``, ``estimate``
    error           None for exact counts; for estimates ``{"relative": r, "confidence": c}``
    """

    linearizations: int | None
    feasible: int | None = None
    method: str = ""
    error: dict | None = None


class LinCounter(Algorithm):
    """Count linearizations without listing them (LIN-COUNT).

    Contract for :meth:`count`: return a :class:`CountResult`. Exact counters leave
    ``error`` as None; estimators set it. A counter must not return a count of a
    different set than the one documented above (e.g. it must not silently ignore sync
    edges).
    """

    category: ClassVar[str] = "lin-count"

    @abstractmethod
    def count(self, setup: Setup) -> CountResult: ...


class LinSampler(Algorithm):
    """Draw random linearizations (LIN-SAMPLE).

    Class attribute ``distribution`` states what the samples follow:

    ``any``               some valid linearization, no distribution promised (variant a)
    ``uniform``           uniform over ``Lin(P)`` (variant b)
    ``uniform-feasible``  uniform over ``LinFeas(P)`` (variant c; needs ``observed_reads``)

    Contract: all randomness comes from the ``rng`` argument, so a seed reproduces the
    output. :meth:`samples` exists so that samplers with expensive preprocessing (e.g. a
    DP table) can do it once for many samples; the default calls :meth:`sample` ``n``
    times.
    """

    category: ClassVar[str] = "lin-sample"
    distribution: ClassVar[str] = "any"

    @abstractmethod
    def sample(self, setup: Setup, rng: random.Random) -> Linearization: ...

    def samples(self, setup: Setup, rng: random.Random, n: int) -> Iterator[Linearization]:
        for _ in range(n):
            yield self.sample(setup, rng)
