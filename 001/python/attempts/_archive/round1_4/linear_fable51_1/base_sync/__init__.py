"""``fable51-s-*``: linearization enumerators for the base problem **plus sync** (``K >= 0``).

Load with ``--plugin attempts._archive.round1_4.linear_fable51_1.base_sync``. Registered algorithms:

* ``fable51-s-pr``    Pruesse-Ruskey Gray code: 1 or 2 adjacent transpositions per step, CAT
* ``fable51-s-vr``    Varol-Rotem / Knuth Algorithm V: iterative left shifts, O(n) worst case per output
* ``fable51-s-tree``  Ono-Nakano style family tree (parent = swap the leftmost descent), CAT, iterative
* ``fable51-s-dp``    ranked enumeration over the per-chain positions DP (start/stop/step); ``fable51-s-count`` counter
* ``fable51-s-cut``   cut-node decomposition (barriers split the poset): product of segment listings
"""

from . import cut, dp, pr, tree, vr  # noqa: F401  (registration)
