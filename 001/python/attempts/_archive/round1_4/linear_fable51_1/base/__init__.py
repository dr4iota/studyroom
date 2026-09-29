"""``fable-*``: base-case linearization enumerators (interleavings of thread chains).

Load with ``--plugin attempts._archive.round1_4.linear_fable51_1.base``. Registered algorithms:

* ``fable51-b-lex``      iterative lexicographic next-permutation (enumerator)
* ``fable51-b-coollex``  loopless cool-lex prefix shifts, Williams 2009 (enumerator)
* ``fable51-b-unrank``   ranked enumeration by multinomial unranking; start/stop/step (enumerator)
* ``fable51-b-gray``     SJT over threads, consecutive outputs differ by <= 2 adjacent swaps (enumerator)
* ``fable51-b-count``    multinomial coefficient (counter)
"""

from . import coollex, gray, lex, unrank  # noqa: F401  (registration)
