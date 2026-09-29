# Sources

## `fable51_1-s-lastwrite` (`solver.py`)

Own derivation, assembled from standard order-theory facts I recall.

1. **Effect orders = linear extensions of an action poset.** A full schedule `(L, pi)`
   is a linear extension of the trace poset `P` with one extra "effect" node per action,
   placed strictly between its start and its done (effect points can be perturbed off the
   integer positions and off each other without changing anything). The restriction of the
   linear extensions of a poset to a subset of its elements is exactly the set of linear
   extensions of the induced sub-order (a standard fact: adding a linear order on the
   subset that extends the induced order cannot close a cycle). Hence, over all
   linearizations, the reachable effect orders are the linear extensions of `Q` with
   `a < b` iff `done(a)` reaches `start(b)` in `P`. For one fixed `L`, the same argument
   on the chain `L` (or the greedy interval argument for interval orders, Fishburn 1970)
   gives `a < b` iff `pos(done(a)) < pos(start(b))`.

2. **Values as source maps.** Under atomic semantics a read returns the content of the
   last write to its block placed before it, else the initial content. A write's content
   is its expression with write references inlined and read references replaced by
   values. So a read's value is determined by its source and, recursively, by the
   sources of the reads its source's expression depends on. The final content of a block
   is the value of a virtual read placed after every action.

3. **Enumeration with feasibility pruning.** Source maps are enumerated depth-first;
   each partial map is a set of constraints "`w` is the last write to `b` before `r`"
   (or "no write to `b` before `r`") and is kept only if some linear extension of `Q`
   realises it (a superset of an infeasible set is infeasible, so pruning is sound).

4. **Feasibility.** Restrict to the relevant actions (constrained reads and writes plus
   the writes to those blocks that are not trivially outside every interval); add the
   constraints' orderings as edges; propagate forced resolutions of the other writes
   (before `w` if before `r`, after `r` if after `w`) to a fixpoint with an incremental
   transitive closure, failing on a cycle; drop unconstrained writes that are minimal or
   maximal in the reduced order (they can always go first or last); if no disjunction is
   left, the acyclic augmented order is realisable; otherwise a depth-first search over
   ideals of the reduced order, memoising failed ideals, decides it. Each reduction step
   preserves the existence of a realising linear extension (restriction lemma above, and
   prepend/append arguments for the dropped writes).

## Things I was unsure about

- I could not run anything; the code was checked by reading only.
- Whether the harness expects `final` keyed by `int` block indices (I followed
  `Outcomes` in `solve/api.py`).
- Witnesses are not returned (`witnesses=False`), since I could not read
  `harness.semantics` to confirm the `Schedule` contract.
