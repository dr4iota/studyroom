"""Linearization enumerators and counters by Fable 5.1, trial 1.

Subpackages, one per case (see ../README.md):

* ``base``       base problem, no sync             names ``fable51-b-*``
* ``base_sync``  base problem with sync            names ``fable51-s-*``
* ``obs``        observed reads, no sync           names ``fable51-o-*``
* ``obs_sync``   observed reads with sync          (missing)

Importing this package registers all of them (``--plugin contrib.linear_fable51_1``);
a subpackage can also be loaded alone (``--plugin contrib.linear_fable51_1.obs``).
"""

from . import base, base_sync, obs  # noqa: F401  (registration)
