# Sources

## `fable51_1-b-downset` (`solver.py`)

Own derivation, built from three pieces.

1. **Reduction of full schedules to effect orders (own derivation).** With `K = 0` the
   trace poset is a disjoint union of per-thread chains. For a fixed linearization `L`,
   an order `E` of the actions is the order of some valid effect-point assignment iff
   `pos(start(E_i)) < pos(done(E_j))` for all `i < j` (necessity is immediate; for
   sufficiency take `pi(E_k) = max_{i<=k} pos(start(E_i)) + k*eps`). That is: `E` is a
   linear extension of the interval order `a < b iff done(a) precedes start(b) in L`.
   Over all linearizations, `E` is realisable iff the union of program order and the
   edges `start(E_i) -> done(E_j)` (`i < j`) is acyclic; any cycle alternates such an
   edge with a program-order path `done(y) -> start(z)`, which forces `y <_E z` when `E`
   extends "same thread and done before start", so the condition is exactly that `E`
   extends that relation. This is the standard "interval order of an execution" view of
   linearizability-style reasoning (I have Herlihy & Wing 1990 and the interval-order
   characterisation of Fishburn in mind), specialised to this problem.

2. **Closed form for blocks without read-dependent writes (own derivation).** In any
   partial order, write `w` can be the last `b`-write before read `r` iff `r` is not
   below `w` and no `b`-write lies strictly between them (construct the linear extension
   as: the down-set of `{x : not (w <= x) and not (r <= x)}`, then `{x : w <= x <= r}`,
   then the rest). Initial content is possible iff no `b`-write is below `r`. `w` can be
   the final writer iff no `b`-write is above it.

3. **Memoised search over reachable states for read-dependent blocks (standard
   dynamic programming over down-sets / linear extensions; own adaptation).** Blocks are
   grouped by data flow (a write's block is joined with the blocks of the reads its
   content depends on, references to earlier writes being inlined). For a group with a
   read-dependent write the search enumerates reachable states
   `(down-set, block contents, values of reads still needed by pending writes)`,
   restricted to that group's writes and referenced reads. Unreferenced reads are
   dropped from the order (this does not change the achievable orders of the remaining
   actions) and their results are read off at every state after which they could be
   inserted. Contents of blocks nothing can touch any more, and read values no pending
   write needs, are forgotten so that states merge.

Mode `fixed` uses the same machinery with the interval order of the given `L`.

## Things I was unsure about

- I could not run anything; all of the above was checked by reasoning only.
- The `fixed` mode relies on my reading of spec §4-5: effect points are reals in the
  closed intervals `[pos(start), pos(done)]`, distinct across actions, and `Poss_L`
  ranges over every such assignment.
- No witnesses are returned (`witnesses=False`), to avoid depending on details of
  `harness.semantics.Schedule` I could not read.
- The search can be expensive on large groups of heavily overlapping read-dependent
  writes; static groups are always handled by the closed form, which is quadratic.
