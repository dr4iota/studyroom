# Sources

## `fable51_1-so-enum` (enumerator, `lin_so.py`)

Own derivation, built from standard pieces:

- Enumeration of `Lin(P)`: textbook backtracking over the minimal elements of the
  remaining poset (indegree counters and a ready set), as in Knuth, *TAOCP* vol. 4A,
  §7.2.1.2 (generating all topological sorts). Written with an explicit stack so that
  the generator is lazy and each output costs O(n) work in the worst case.
- Feasibility of a fixed linearization: my own reduction. With closed intervals and
  distinct real effect points, `a` can take effect before `b` iff
  `pos(start(a)) < pos(end(b))`, so the realisable effect orders are exactly the linear
  extensions of the interval order `end(a) < start(b)` (the greedy construction
  `π(a_i) = max_{j<=i} start(a_j) + i·ε` witnesses sufficiency). Feasibility is then a
  search over those linear extensions with atomic block semantics, memoised on
  (placed set, block contents, results of reads still needed by unplaced writes). Two
  safe greedy moves prune it: a minimal observed read whose block already holds the
  observed term is placed at once, and so is a minimal read whose result nobody still
  needs (moving a read earlier never changes any result).
- Incremental checking along the prefix: my own observation that the interval-order
  relations among started actions never change afterwards, and that later-started
  actions are forced after every already-ended action. Hence a check at each observed
  read's `done` node is necessary, and the last one is sufficient. The check depends
  only on the "runs" of relevant endpoints (maximal groups of consecutive starts or
  consecutive dones), which is used as the memo key for check results and for dead
  DFS states `(placed set, runs)`.
- The general problem is a form of verifying a read/write history against atomic
  register semantics, which is NP-hard in general (Gibbons and Korach, "Testing shared
  memories", SIAM J. Comput. 1997, as I recall it), so a memoised search rather than a
  polynomial test is expected.

## `fable51_1-so-count` (counter, `lin_so.py`)

Own derivation from the same state space:

- `|Lin(P)|`: the multinomial coefficient `n! / ∏ len(chain)!` when `K = 0` (the poset
  is a disjoint union of thread chains); otherwise the standard dynamic programme over
  order ideals (down-sets), level by level.
- `|LinFeas(P)|`: the same level-by-level DP over states `(ideal, runs)`, dropping a
  transition when the check at an observed read's `done` fails. The state is exactly
  what determines the future of the enumerator's DFS, so the counts are exact.

## Unsure about

- Whether the harness ever hands over a poset with zero nodes; I return the single
  empty linearization (count 1) in that case.
- Memory: the dead-state and check memo tables are cleared when they exceed one
  million entries; this only loses pruning, never correctness.
- Performance on setups where almost every action is relevant to some observed read
  and the feasibility search itself is hard; the memoised search is exponential in the
  worst case, as the problem requires.
