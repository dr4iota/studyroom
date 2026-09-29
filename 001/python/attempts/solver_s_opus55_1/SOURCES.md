# Sources

## `opus55_1-s-downset` (solver.py)

Own derivation, using standard ideas.

- **Reduction to effect orders.** An effect order sigma is realizable (some L in Lin(P)
  and some pi) iff sigma extends the happens-before order `a hb b <=> done(a) <_P start(b)`.
  Proof sketch: add a node `e_a` with `start(a) < e_a < done(a)` for every action and chain
  the `e_a` in sigma order. Any cycle in that graph alternates forward sigma steps and hb
  jumps, which contradicts sigma extending hb. So the extended graph is acyclic, and
  linearizing it gives L and pi. For mode `fixed`, the same holds with hb taken in L.
  The idea is the usual one from interval orders and linearizability checking
  (Herlihy & Wing, "Linearizability", 1990), adapted here.
- **Search.** A memoized DFS over downsets of hb (the "state = executed set" dynamic
  programming used in linearizability checkers such as Wing & Gong 1993 and Lowe 2017),
  with the state cut down to what can still affect the outcome. A block's content is
  kept only while a read of that block is pending. A read's value is kept only while a
  pending write depends on it (directly or through write references). A block's final
  content is recorded once no write to it is pending. Terms are hash-consed to ints.
- Without observations every reachable state extends to a full schedule, so everything
  recorded is realizable, and all linear extensions are covered.

Unsure: no witnesses are returned, because I was not allowed to read
`harness/semantics.py`. Worst-case run time is exponential (the number of downsets
times the retained values).
