# Sources

## `fable51_1-o-ideals` (`solver.py`)

Own derivation, assembled from standard ideas.

- **Reduction to linear extensions.** With `K = 0` the trace poset is a disjoint union
  of chains (one per thread), so a total order of the actions is the effect order of
  some full schedule iff it extends `R = {(a, b) : same thread, done(a) before start(b)
  in program order}`; for a fixed linearization `L`, iff it extends
  `R_L = {(a, b) : done(a) <_L start(b)}`. I derived this myself: the "only if" is
  immediate; for the "if", the graph of program order plus `start(a) -> done(b)` for
  every `a < b` in the order is acyclic (a cycle would close a strictly increasing
  chain in the total order), any linear extension of it is a suitable `L`, and
  `pi(a_i) = max(pos(start(a_1..a_i))) + i*eps` are distinct effect points inside the
  intervals because all endpoint positions are distinct integers. The fact that
  interval-compatible total orders are exactly the linear extensions of the interval
  order is folklore (interval orders, Fishburn 1970).
- **Search.** Depth-first search over the order ideals of `R` with memoization on
  `(ideal, block contents, values of the reads a pending write still depends on)`, i.e.
  ordinary state-space exploration / dynamic programming over subsets, as used for
  linearizability checking (Wing and Gong, "Testing and verifying concurrent objects",
  1993, and later work); the "good state = has a feasible completion" post-order
  labelling is standard reachability. Terms are interned to ints so state keys hash
  fast.
- **Witnesses.** Parent and completion pointers per state; the concatenated effect
  order is re-executed, and in mode `all` a linearization is built by emitting each
  action's start (with its not yet emitted program-order predecessors) in effect order
  and the remaining ends last. Own construction; its correctness follows from the same
  acyclicity argument as the reduction.

## Uncertainties

- I could not read `harness.semantics`, so the `Schedule` constructor is used exactly
  as the task file and `solve/api.py`'s `Collector` show it: positional
  `(order, effects, results, final, consistent, meta)`, `order` a tuple of node
  indices, `final` a list of terms. If the grader re-executes witnesses with a
  different notion of validity (e.g. requiring effect points strictly inside intervals)
  the construction still holds, since the derived `pi` avoids the endpoints.
- Every witness is re-executed and checked against what it certifies before being
  returned; a witness that failed that self-check would be dropped rather than
  returned, which should never happen.
- The state space is the number of reachable `(ideal, contents, live reads)` states,
  which can grow quickly for many independent threads; on the small correctness cases
  this is negligible, and I did not have a way to time the larger setups.
