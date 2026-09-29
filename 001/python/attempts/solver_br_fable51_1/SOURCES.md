# Sources

## `fable51_1-br-groupdp` (`solver.py`)

My own derivation, assembled from standard ideas:

- **Effect orders are the linear extensions of an interval-order poset.** Realizability of
  an effect order is decided by acyclicity of the trace poset extended with one node per
  effect point; the standard "restriction of linear extensions" facts (a linear extension
  of an induced sub-poset extends to the whole poset; restrictions of linear extensions
  are linear extensions of the sub-poset) come from basic order theory (e.g. Trotter,
  *Combinatorics and Partially Ordered Sets*, 1992, and the folklore around interval
  orders / linearizability checking in the style of Herlihy & Wing, 1990). The idea that
  a concurrent history's admissible effect orders are the linear extensions of the
  "ends-before-starts" interval order is the usual view of linearizability.
- **Downset (antichain) dynamic programming** over "which actions have taken effect,
  plus the current memory state" is the classical state-space search for checking
  linearizability of histories (Wing & Gong 1993; Lowe 2017 for the "just-in-time"
  variants). I adapted it by (a) merging states on `(executed set, live contents, live
  read values)`, (b) forgetting block contents and read values that no remaining action
  can observe, and (c) removing unreferenced reads from the search entirely, recovering
  their possible results from the states in which they could be inserted.
- **Block-group decomposition** (union-find over blocks connected by read references) is
  my own observation: a group's values depend only on the restriction of the effect order
  to the group's actions.
- **Witness completion** (greedy topological completion of a forced prefix, then building
  a linearization by emitting each thread's program-order nodes lazily up to each
  effected action's start) is my own construction.

## Things I was unsure about

- I could not run anything, so the code is checked by reasoning only. The witness
  builder re-executes each schedule and drops a witness if its value does not match
  (which should never happen); a dropped witness would show up as a missing witness.
- The `Schedule` interface is used only as described in the task file
  (positional fields `order, effects, results, final, consistent, meta`).
- The mode `fixed` uses the same machinery with the poset induced by the given
  linearization (`pos(done(b)) < pos(start(a))`), and returns the given linearization in
  every witness.
