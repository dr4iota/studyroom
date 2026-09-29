# Sources

## `fable51_1-or-idealdp` (`solver.py`)

Own derivation, built from two pieces.

1. **Realizable effect orders = linear extensions of an interval order.** A full
   schedule `(L, π)` sorts the actions by `π`; I argued (docstring of `solver.py`) that a
   total order `σ` on actions comes from some `(L, π)` iff `σ` extends `Q`, where
   `a <_Q b` iff `done(a)` precedes `start(b)` in `P` (mode `all`) or in `L` (mode
   `fixed`). The necessity direction is immediate; sufficiency is the classical
   interval-order argument (the relation `P ∪ {start(a) → done(b) : a <_σ b}` is acyclic,
   and a greedy choice of effect points works in any of its topological orders). This is
   the standard "linearizability = interval order extension" fact from the concurrent
   data structure literature (Herlihy and Wing, *Linearizability*, 1990, in spirit), but
   the exact statement used here is my own.

2. **Memoised search over ideals with state projection.** A breadth-first search over
   states `(applied set, block contents, values of still-needed reads)`, dropping block
   contents and read values as soon as no future action can look at them and emitting
   them as edge labels instead; then a backward reachability pass from the terminal
   state marks the *alive* states (those with a feasible completion), and `Poss` is the
   set of labels on edges into alive states. This is ordinary explicit-state
   reachability with liveness pruning, as used in model checkers; the projection of dead
   state components is my own adaptation to this problem. Terms are interned to
   integers so that structural equality is integer equality.

Witnesses: a parent pointer (root → state) and a completion pointer (state → terminal)
give a full effect order for every reported value; it is re-simulated from scratch to
fill `results`/`final`. In mode `all` the linearization is built by emitting, for each
action in effect order, its start node with all P-predecessors, then everything left;
in mode `fixed` the given `L` is returned.

## Things I was unsure about

- The exact interface of `harness.semantics.Schedule` and of its re-execution by the
  grader (I could not read `semantics.py`). I followed the task description literally:
  `Schedule(order, effects, results, final, consistent, meta)` with `order` a tuple of
  node indices, `effects` a list of action ids in effect order, `results` an id → term
  dict for reads and RCWs, `final` a list of terms (one per block), and
  `meta["certifies"]` using `terms.to_value`.
- `rcw_result: flag` semantics (observed `"ok"`/`"fail"`) are not part of the task; the
  solver treats such an observation as a success/failure constraint, but this path is
  untested.
- The state space is the product of per-thread ideals of `Q` times the distinct
  contents, which is inherently exponential; no attempt was made to decompose by block
  when blocks are data-independent.
