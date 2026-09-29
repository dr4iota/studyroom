# Sources

## opus55_1-s-backtrack (enumerator)

Adaptation of the textbook backtracking enumeration of linear extensions / topological
sorts (Knuth and Szwarcfiter, "A structured program to generate all topological sorting
arrangements", 1974; also Knuth, TAOCP Vol. 1, topological sorting). Changed: written as
an explicit-stack iterative generator (no recursive generator chain), with the set of
minimal elements kept incrementally via in-degrees, and each level's candidates taken in
sorted node order so the output is deterministic (lexicographic by node index). Every
prefix of a linear extension extends to one, so there are no dead ends. Not a Gray code.

## opus55_1-s-decomp (counter)

Own derivation, combining standard facts:
- disjoint union of incomparable parts: `e(P) = n!/prod(|P_i|!) * prod e(P_i)`
  (components of the comparability graph);
- a node comparable to every other node splits the poset into a product of the parts
  below and above it (all such nodes are totally ordered, so the poset is cut into
  consecutive segments);
- otherwise, counting paths in the lattice of downsets (bitmask dynamic programming by
  level).
Reachability is computed as ancestor/descendant bitmasks from `setup.poset` edges.

## Unsure

- The counter's downset DP can be exponential on wide, connected posets; the
  decompositions are there to keep typical setups (thread chains cut by sync barriers)
  small.
