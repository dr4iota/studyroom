# Sources

## opus55_1-so-enum (enumerator)

- **Linear-extension generation:** a standard backtracking DFS. Place any minimal
  remaining node, in increasing index order, and undo on backtrack. I wrote it from
  memory; it is the textbook method (compare Varol and Rotem, 1981, and Knuth's TAOCP
  Vol. 4A, 7.2.1.2, on topological sorts). It is written with an explicit stack, so deep
  posets do not hit the recursion limit.
- **Feasibility pruning:** my own derivation. For a fixed prefix of L, I keep a set of
  effect states (pending actions, block contents, the values of reads that writes need).
  Start nodes add a pending action. A done node forces that action's effect, after any
  sequence of effects of other pending actions. Effects are postponed to the gap before
  the next done node. This keeps their relative order and so loses no schedule, because
  start nodes have no data effect. Pairwise interval constraints are enough to realise an
  effect order: a greedy argument over distinct integer endpoints and real effect points
  shows it. A branch is cut when the set becomes empty.
- **Relevance reduction:** my own. Only the observed reads are tracked, together with the
  writes to their blocks and, by fixpoint, the reads those writes' data depends on. A read
  value is stored only for unobserved reads that a tracked write uses. An observed read's
  value is taken to be its observed term.
- **Dead-prefix memo:** my own. If a subtree with key (placed set, state set) yields
  nothing, the key is remembered and pruned when it is seen again. The future depends only
  on this key. The memo is capped at 10^6 entries.

## opus55_1-so-count (counter)

- `|Lin(P)|`: a layered forward DP over downsets (bitmask of placed nodes), from memory.
  This is the standard ideal-lattice count.
- `|LinFeas(P)|`: the same DP keyed by (downset, effect-state set), using the step
  function above. It is filled only when the setup has observed reads; otherwise it is
  `None`.

## Uncertainties

- I assumed that `feasible` should be `None` when there are no observations, as the API
  docstring allows.
- The downset DP can be slow or use a lot of memory on posets with very many downsets.
  It is exact.
