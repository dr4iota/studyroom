# Sources

## `fable51_1-s-varol-rotem` (enumerator, `varol_rotem.py`)

From memory: Y. L. Varol and D. Rotem, "An algorithm to generate all topological sorting
arrangements", The Computer Journal 24(1), 1981; also given as Algorithm V ("all
topological sorts") in D. E. Knuth, The Art of Computer Programming Vol. 4A, §7.2.1.2.

Adaptation: the array holds node indices of `setup.poset` directly (a deterministic
topological order, smallest ready index first, plays the role of the identity
labelling), positions are 0-based with an explicit "nothing to the left" test instead of
a sentinel element, and the predecessor test uses only the direct edges of the poset
(sufficient, since the array is always a linear extension and a transitive predecessor
of an adjacent element must be a direct one). Verified by hand on: an antichain of 3,
two chains of 2, a diamond, and a 3-chain with a shortcut edge.

`gray_code` is left False: consecutive outputs are one adjacent swap apart only when
no "put back" step happens in between.

## `fable51_1-s-ideal-dp` (counter, `ideal_count.py`)

Own derivation of standard ideas:
- counting linear extensions by dynamic programming over order ideals (downsets),
  layered by size, with the ideal represented by the progress along each chain of a
  chain partition (folklore; the chain partition is the harness's `poset.chains`);
- the disjoint-union rule `|Lin(A + B)| = C(|A|+|B|, |A|) |Lin(A)| |Lin(B)|`, applied to
  connected components so that threads unrelated to any sync point cost nothing.

## Unsure

- Whether `CountResult.feasible` should also be filled for a counter without the
  `observed_reads` capability; the task says to fill `linearizations`, so `feasible`
  is left `None`.
- Speed of the counter on large, loosely constrained components (many long threads all
  tied to one sync point): the ideal DP is exponential in the number of chains of a
  component. The enumerator's cost is O(n) per output, which the tuple copy needs anyway.
