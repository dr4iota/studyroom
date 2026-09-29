"""Linearization enumerators and counters by Opus 5.5, trial 1.

Subpackages, one per case (see ../README.md):

* ``base``       base problem, no sync             names ``opus55-b-*``
* ``base_sync``  base problem with sync            names ``opus55-s-*``
* ``obs``        observed reads, no sync           names ``opus55-o-*``
* ``obs_sync``   observed reads with sync          (missing)

Importing this package registers all of them (``--plugin contrib.linear_opus55_1``);
a subpackage can also be loaded alone (``--plugin contrib.linear_opus55_1.obs``).
"""

from . import base, base_sync, obs  # noqa: F401  (registration)
