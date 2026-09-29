# Sources

## `fable51_1-sr-downset` (`solver.py`)

Own derivation, assembled from standard ideas.

1. **Realisable effect orders = linear extensions of an "end before start" order.**
   Derived here. For a fixed linearization `L`, an effect order is realisable iff no later
   action's interval lies entirely before an earlier action's interval; this is the
   familiar fact that the orders of distinct points chosen from intervals are exactly the
   linear extensions of the interval order (Fishburn's interval orders, 1970s, as I recall
   it). Over all `L ∈ Lin(P)` I argued that the union of these sets is the set of linear
   extensions of `a ≺ b ⇔ end(a) <_P start(b)`: the pairwise condition is clearly
   necessary, and if it holds, adding the edges `start(σ_i) → end(σ_j)` (`i < j`) to `P`
   keeps it acyclic (a cycle would alternate `P`-paths `end(σ_j) ≤ start(σ_i)` with
   added edges and force `j < i < j`), so a topological order of the augmented graph is a
   suitable `L`.

2. **Memoised search over downsets.** The usual dynamic programme over ideals for
   enumerating linear extensions (e.g. as used for counting linear extensions), with
   the state enlarged by the block contents and the results of reads that some pending
   write or RCW still refers to. Interning terms as integers is an ordinary trick.

3. **Decomposition by block groups and passive reads.** Own observation: projection of
   a linear extension onto a subset is a linear extension of the restriction, and every
   linear extension of a restriction extends back, so blocks that share no read/write
   data dependency can be solved separately, and a read that nothing refers to can be
   evaluated at every state where it can be inserted (all its `≺`-predecessors done,
   none of its `≺`-successors done) instead of being enumerated.

4. **Witnesses.** Kahn's algorithm (1962) to complete a prefix of the effect order,
   plus the constructive step of item 1 (place the down-closure of each start in effect
   order, then the rest) to get a linearization in mode `all`.

## Things I was unsure about

- Whether the grader's re-execution of witnesses accepts any linearization realising
  the effect order (I build one by the closure construction above) or wants a specific
  form; I followed the `Schedule` description in the task file and the `Collector`
  helper in `solve/api.py` for field shapes (`order` is a tuple of node indices,
  `effects` a list of ids, `final` a list per block, `meta["certifies"]` with
  `harness.terms.to_value`).
- I ignore `setup.semantics` (`rcw_result: flag`, `distinct_effects`) and use the
  spec's default semantics: RCW returns the old content; effect points are distinct.
- Exponentially large terms (a chain of writes each pairing the previous one with
  itself) would make structural hashing slow; I did not add hash-consing beyond
  interning distinct terms.
