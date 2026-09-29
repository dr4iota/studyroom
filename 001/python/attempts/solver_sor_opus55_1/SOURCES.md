# Sources

## opus55_1-sor-effdp (`effdp.py`)

My own derivation, using standard ideas I remember:

- The reduction from full schedules to effect orders is the usual linearizability
  argument (Herlihy and Wing, "Linearizability: A Correctness Condition for Concurrent
  Objects", 1990). An effect order sigma can be realised iff it extends the interval
  precedence order `a -> b iff end(a) < start(b)`. For mode "all" the order used is `<_P`.
  In the graph P + {start(a) < e_a < end(a)} + the sigma chain, a cycle has to contain a
  backward jump e_j -> end(a_j) <_P start(a_k) -> e_k with k before j in sigma, which
  breaks that precedence. For mode "fixed" the order uses positions in L, and a greedy
  point placement proves it. Data dependencies and observations do not change which
  orders are realisable. They only filter orders by simulation.
- The enumeration of linear extensions is a layered DP / memoised state-space search
  (the same idea as Gibbons and Korach's work on testing shared memories, 1997). Its state
  is (set of executed actions, block contents, read values that undone writers still
  need). Observations prune transitions. A backward pass keeps only the transitions that
  reach a complete schedule. `Poss(r)` comes from those transitions and `Poss(b)` from the
  terminal states.

Unsure points:
- Under the non-default `rcw_result: flag`, observed `ok`/`fail` values are applied as a
  constraint, but the reported RCW result is still the old content.
- No witnesses are returned.
