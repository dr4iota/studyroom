"""Capabilities (what an algorithm can handle) vs. features (what a setup uses).

The **base problem** every algorithm must handle is:

* actions are ``Read`` and ``Write`` only (no ``RCW``);
* write data is any expression of formats.md §2.2: constants, unknown (``"*"``),
  earlier reads and earlier writes of the same thread, and ``~``-trees of these;
* no synchronization (``K = 0``: no sync points, hence no events);
* no observed read results (every ``done`` step of a read has no ``data``);
* atomic register semantics with distinct effect points.

Unknown write contents (``data: "*"``) and unknown initial contents are free symbols
(``Unk``/``Init`` terms), not extra nondeterminism. Read-dependent data never changes
``Lin(P)``, since a referenced read always completes earlier in program order. It
does change the values a solver must report, and the feasible linearizations once
reads are observed.

The problem is organised in four cases, observations × sync:

==============  ==========  =================
                no sync     sync
==============  ==========  =================
base            ``b``       ``s``
observed        ``o``       ``so``
==============  ==========  =================

Each algorithm declares, as a class attribute ``capabilities``, which extensions it
supports on top of the base problem. The CLI compares them with
:meth:`abio.model.Setup.features` and refuses to run an algorithm on a setup that uses an
unsupported extension (``--ignore-observed`` strips observations instead of refusing).

Sync and observed results *restrict* the problem: sync edges remove linearizations, and
observations remove infeasible full schedules, so both shrink ``Lin(P)`` (or its feasible
part) and the possibility sets. An algorithm that ignored them would over-approximate;
that is why they are capabilities and not hints.
"""

from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class Features:
    """Extensions beyond the base problem that a setup actually uses."""

    rcw: bool = False  # some action is an RCW
    sync: bool = False  # K > 0 (sync points exist, even if no event references one)
    observed_reads: bool = False  # some read/RCW done step carries an observed result

    def names(self) -> list[str]:
        return [f.name for f in fields(self) if getattr(self, f.name)]


@dataclass(frozen=True)
class Capabilities:
    """Extensions an algorithm supports.

    rcw
        Handles ``RCW`` actions. For linearizers an RCW is just an action with two
        endpoints, so it is almost always supported; for solvers it means implementing
        compare-and-write semantics (the result is the old content).
    sync
        Handles ``K > 0``: virtual steps ``sync.k`` and the edges induced by
        ``before``/``after``/``at`` events (premise.md §2.2).
    observed_reads
        Handles observed read/RCW results. A linearizer with this capability restricts
        itself to *feasible* linearizations (those admitting at least one full schedule
        matching every observation); a solver restricts ``Poss`` to feasible schedules.
    """

    rcw: bool = False
    sync: bool = False
    observed_reads: bool = False

    def missing(self, feats: Features) -> list[str]:
        """Names of features used by the setup but not supported here."""
        return [n for n in feats.names() if not getattr(self, n)]

    def summary(self) -> str:
        return " ".join(f"{f.name}={'yes' if getattr(self, f.name) else 'no'}" for f in fields(Capabilities))

    def case(self) -> str:
        """The widest of the four cases supported: ``b``, ``s``, ``o`` or ``so``."""
        return {(False, False): "b", (True, False): "s", (False, True): "o", (True, True): "so"}[
            (self.sync, self.observed_reads)]
