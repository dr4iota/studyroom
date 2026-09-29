# Sources

## `fable51_1-so-downset-dp` (`solver.py`)

**Own derivation**, built from the specification. The pieces, and where they come from:

1. **Effect order suffices.** The values of a full schedule `(L, π)` depend only on the
   order of the effect points (spec §4), so `Poss` is a union over realisable effect
   orders `σ`.

2. **Realisable effect orders = linear extensions of an "effect poset" `Q`.** For a
   fixed `L`, an order `σ` of the actions admits distinct effect points
   `π(a) ∈ I_L(a)` iff `σ` is a linear extension of the interval order of `L`
   (`a < b` iff `pos(done(a)) < pos(start(b))`). The "if" direction is the greedy
   argument (assign each point as early as its interval and the previous point allow; a
   failure would exhibit a later action whose whole interval precedes an earlier one).
   Over all `L ∈ Lin(P)`, `σ` is realisable iff `P` extended with
   `start(a) < e(a) < done(a)` and the chain `e(σ_1) < e(σ_2) < …` is acyclic, and a
   cycle in that graph forces some `done(σ_j) <_P start(σ_i)` with `i < j`. Hence
   `σ` is realisable iff it extends `Q`: `a <_Q b` iff `done(a) <_P start(b)`. This is
   the standard "interval order / linear extension" reasoning (as in Fishburn's work on
   interval orders, 1970s), adapted here to a poset of endpoints rather than a single
   interval family.

3. **Dynamic programme over down-sets** (a routine subset-DP over the ideals of `Q`,
   in the spirit of counting linear extensions by down-sets): states are (block
   contents, values of reads still needed by writes that have not taken effect);
   a forward reachability pass enforces observations, a backward pass keeps states that
   complete to a feasible full schedule, and the possibility sets are read off the
   transitions between surviving states.

4. **Passive reads** (unobserved and not referenced by any write) are removed from the
   DP: a linear extension of `Q` minus those reads always extends to one of `Q`, so
   `Poss` of such a read is the set of contents of its block at any surviving state
   where all its `Q`-predecessors have fired and none of its `Q`-successors has.

5. **Witnesses** are rebuilt from parent/successor pointers, completed with the passive
   reads, re-executed under the same semantics, and turned into a linearization by a
   topological sort of `P` plus the effect chain (mode `all`), or the given `L`
   (mode `fixed`). Each witness is verified before it is returned.

## Uncertainties

- The exact constructor of `harness.semantics.Schedule` is taken from the task text
  (`Schedule(order, effects, results, final, consistent, meta)`); witness building is
  wrapped so that a mismatch would drop the witnesses rather than the answer.
- `order` in a witness is a tuple of node indices (as `harness.poset.Linearization`).
- Cost is governed by the number of down-sets of `Q` restricted to active actions,
  times the number of distinct execution states per down-set; no further pruning was
  attempted.
