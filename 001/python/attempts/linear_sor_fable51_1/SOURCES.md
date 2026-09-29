# Sources

## `fable51_1-sor-enum` (enumerator, `sor_enum.py`)

Own derivation, assembled from standard pieces I recall:

- **Enumerating linear extensions** by depth-first backtracking over the "ready" (all
  predecessors placed) nodes is the classical topological-sort enumeration (Knuth,
  *TAOCP* vol. 4A §7.2.1.2; Varol and Rotem, "An algorithm to generate all topological
  sorting arrangements", *Computer Journal* 1981, is the usual reference for the
  swap-based variant, which I did not use).
- **Effect points are an interval order.** Given `L`, the effect orders realisable by
  distinct effect points in the closed intervals are exactly the linear extensions of the
  interval order "`a < b` iff `done(a)` precedes `start(b)`" (Fishburn, *Interval Orders
  and Interval Graphs*, 1985; the greedy point-assignment argument is mine). Different
  blocks interact only through data flowing from reads to later writers, so per-group
  effect orders combine freely (assign points per group, then perturb to make them
  distinct).
- **Carrying the set of reachable simulation configurations** along the prefix of `L`
  (a subset construction, in the spirit of NFA determinisation) so that a prefix is
  pruned as soon as no effect order can satisfy the observations: my own derivation.
- **Relevance analysis** (dropping actions and blocks that cannot influence any
  observation; erasing, per configuration, blocks no relevant reader will look at again
  and read values nothing will evaluate again; treating the affected actions as no-ops
  that count as effected, justified because a linear extension of an induced sub-order
  always extends to the whole order): my own derivation.

## `fable51_1-sor-count` (counter, `sor_enum.py`)

Own derivation: the same search memoised on `(set of placed nodes, configuration
sets)`; the future only depends on that pair. `|Lin(P)|` is the multinomial coefficient
when `P` is a disjoint union of chains (no sync node has an edge), otherwise the standard
dynamic programme over order ideals (memoised on the set of placed nodes).

## Unsure about

- Semantics `rcw_result: flag` (observed `ok`/`fail`) is outside spec v2; I treat `ok`
  as "old content equalled the expected value" and `fail` as the opposite. Semantics
  `distinct_effects: false` is ignored (effects are always treated as distinct).
- The counter always fills `feasible` (equal to `|Lin(P)|` when nothing is observed).
- The counter's memo is cleared beyond 2M entries to stay under the memory cap; on very
  large setups it may then be slow rather than run out of memory.
- Pruning happens at `done` nodes, so a prefix whose observed read can no longer succeed
  is only cut when that read's `done` becomes the candidate; correctness is unaffected.
