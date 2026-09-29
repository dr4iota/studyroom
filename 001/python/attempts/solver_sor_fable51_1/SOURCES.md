# Sources

## `fable51_1-sor-downset` (`solver.py`)

**Own derivation**, with standard building blocks from memory.

- The reduction is my own: over all linearizations `L` of `P`, the effect orders that
  some full schedule realises are exactly the linear extensions of the "effect poset"
  `Q` on actions, `a <Q b` iff `end(a)` precedes `start(b)` in `P` (for mode `fixed`,
  in `L`, where `Q_L` is the interval order of `L`). The proof sketch is in the module
  docstring: one direction is `π(a) ≤ end(a) < start(b) ≤ π(b)`; the other adds effect
  nodes and a chain along the extension to `P`, shows the result is acyclic, and takes a
  topological order. The fact that any total order compatible with an interval order is
  realisable by points inside the intervals is a standard fact about interval orders
  (Fishburn, *Interval Orders and Interval Graphs*, 1985, as best I recall).
- The engine is a memoised depth-first search over the downsets (order ideals) of `Q`,
  the usual state-space / dynamic-programming technique for enumerating linear
  extensions (e.g. the ideal-lattice DP used for counting linear extensions; Pruesse and
  Ruskey's work on generating them, 1990s). The state adds the block contents and the
  read results still referenced by pending writers; `Poss` is collected on transitions
  into completable states, so observations restrict the sets exactly.
- Small reductions of my own: a block's content is replaced by a "don't care" marker
  while it has no pending read/RCW but a pending plain write; read results are dropped
  from the state once every writer referencing them has effected; write and expect
  expressions are flattened so they refer only to reads (a referenced writer stands for
  its evaluated data, whether or not an RCW succeeded, per spec §4).
- Witnesses: the DFS path plus a memoised completion of the target state gives an effect
  order; it is re-executed with a direct implementation of spec §4, and a linearization
  is produced by a topological sort of `P` plus effect nodes chained in that order (mode
  `all`) or is the given `L` (mode `fixed`).

## Unsure about

- The `Schedule` constructor and field semantics are taken from the task description
  and the `Collector` helper in `solve/api.py` (positional
  `Schedule(order, effects, results, final, consistent, meta)`, `order` a tuple of node
  indices, `effects` all action ids in effect order).
- `semantics.rcw_result: "flag"` is not in spec v2; observed `"ok"`/`"fail"` are
  interpreted as "the compare succeeded/failed" and the reported result stays the old
  content. Default semantics are unaffected.
- The `topological_order` of `TracePoset` is used as a topological order for the
  reachability pass (it is Kahn's algorithm, so it is one).
