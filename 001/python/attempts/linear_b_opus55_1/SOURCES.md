# Sources

## opus55_1-b-interleave (enumerator)

From memory, then adapted. In case b (K = 0) the trace poset is a disjoint union of the
thread chains, so Lin(P) is the set of interleavings of those chains, which is in bijection
with the distinct permutations of the multiset of chain labels (label `c` repeated
`len(chain c)` times). These are listed with the classic lexicographic "next permutation"
step (Narayana Pandita, 14th c.; as in Knuth, TAOCP Vol. 4A, 7.2.1.2, Algorithm L), which
visits each distinct multiset permutation exactly once.

My adaptation: after each step only the suffix from the pivot position changes, so only
that suffix is mapped back to node indices. The k-th occurrence of label `c` in the
suffix is the node at position `len(c) - (occurrences of c in suffix) + k` of chain `c`.

Safety net (my own): if the poset is not exactly a disjoint union of chains (an edge that
is not a consecutive step of one chain), a plain DFS over minimal elements enumerates all
linear extensions instead. It should never trigger on case-b setups.

`gray_code` is left False (lexicographic order is not an adjacent-transposition order).

## opus55_1-b-multinomial (counter)

From memory: the number of interleavings of chains of lengths n_1..n_k is the
multinomial coefficient (n_1+...+n_k)! / (n_1! ... n_k!). Same safety net as above: a
down-set dynamic program over bitmasks (my own) for a poset that is not a disjoint union of
chains.

## Unsure

- I assumed that with K = 0 `poset.chains` holds exactly the thread chains and all
  poset edges are consecutive program-order steps; the code checks this and falls back if
  not.
- An empty poset yields one empty linearization and counts 1.
