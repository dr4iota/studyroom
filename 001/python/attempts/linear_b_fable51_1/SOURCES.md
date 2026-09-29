# Sources

## `fable51_1-b-interleave` (enumerator, `interleave.py`)

Own derivation on top of a standard algorithm. With `K = 0` the trace poset is a
disjoint union of thread chains, so `Lin(P)` is the set of chain interleavings, and each
interleaving is determined by its word of chain labels (a multiset permutation). The
words are generated in lexicographic order by the classic "next permutation" step
(find the rightmost ascent, bring in the smallest larger label from the suffix, arrange
the suffix ascending), which I recall from Knuth, *The Art of Computer Programming*,
Vol. 4A, §7.2.1.2 "Generating all permutations" (Algorithm L, 2011), applied to
multisets. The adaptation is mine: the rightward scan for the ascent also counts the
suffix's labels, so the node tuple's changed suffix is rebuilt directly from the
per-chain remainders with list slices rather than by re-reading the word.

## `fable51_1-b-multinomial` (counter, `interleave.py`)

Own derivation: `|Lin(P)|` is the multinomial coefficient of the chain lengths, computed
as a product of binomials with `math.comb`.

## Notes and uncertainties

- `gray_code` is left `False`: lexicographic multiset permutations are not adjacent
  transpositions apart.
- The chains are taken from `setup.poset.chains`, which, with no sync points, are exactly
  the thread chains (empty threads are dropped). No cross-chain edges exist in case b, so
  no fallback for them is included; the algorithm is only registered for
  `Capabilities(rcw=False, sync=False, observed_reads=False)`.
- The counter fills only `linearizations`, as the task asks, and leaves `feasible` as
  `None` (without observations `LinFeas(P) = Lin(P)`, but the task did not ask for it).
- With zero nodes the enumerator yields the single empty linearization `()` and the
  counter returns 1.
