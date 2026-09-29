"""``fable51-o-*``: enumerators and a counter for **feasible** linearizations ``LinFeas(P)``
with observed reads and **read-dependent write data**.

Scope: reads and writes (no RCW), no sync (``K = 0``), write data any expression of
formats.md §2.2 (constants, ``"*"``, references to earlier reads and writes of the same
thread, ``~``-trees of these), constant or unknown initial contents, and partially
observed read results whose values may be compound terms.

Load with ``--plugin contrib.linear_fable51_1.obs``. Registered algorithms:

* ``fable51-o-prune``   backtracking, prefixes pruned by the reads-from criterion (goal-directed term matching)
* ``fable51-o-auto``    backtracking, component automaton (value classes) as incremental prefix state + lookahead
* ``fable51-o-dp``      DP over (down-set, component automata): zero dead ends, rank/unrank; ``fable51-o-count`` counter
* ``fable51-o-filter``  Pruesse-Ruskey Gray code of ``Lin(P)`` with an incremental per-component filter

Fixed-``L`` tests (``common``): ``is_feasible_fast`` (reads-from criterion) and
``is_feasible_auto`` (automaton criterion); the theory, and which constant-data lemmas
survive, is in ``common``'s docstring.
"""

from . import auto, dp, filter, prune  # noqa: F401  (registration)
from .common import is_feasible_auto, is_feasible_fast  # noqa: F401
