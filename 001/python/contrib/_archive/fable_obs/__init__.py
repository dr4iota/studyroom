"""``fable-o-*``: enumerators and a counter for **feasible** linearizations ``LinFeas(P)``.

Scope: reads and writes (no RCW), sync points (any mix of before/after/at), constant or
unknown write data and initial contents, and partially observed read results. Write
data that depends on earlier reads is not supported (``data_from_reads=False``).

Load with ``--plugin contrib._archive.fable_obs``. Registered algorithms:

* ``fable-o-prune``   backtracking, prefixes pruned by the slot criterion (write order + read slots)
* ``fable-o-auto``    backtracking, register automaton as incremental prefix state + supplier lookahead
* ``fable-o-dp``      DP over (down-set, automaton state): zero dead ends, rank/unrank; ``fable-o-count`` counter
* ``fable-o-filter``  Pruesse-Ruskey Gray code of ``Lin(P)`` with an incremental per-block filter

Fixed-``L`` tests (``common``): ``is_feasible_fast`` (slot criterion) and
``is_feasible_auto`` (automaton criterion); the theory is in ``common``'s docstring.
"""

from . import auto, dp, filter, prune  # noqa: F401  (registration)
from .common import is_feasible_auto, is_feasible_fast  # noqa: F401
