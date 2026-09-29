# Sources

## `fable51_1-o-enum` (enumerator)

- **Interleavings without observations** (`core.interleavings`): the sequence of thread
  indices of a linearization is a multiset permutation; it is advanced with the classic
  lexicographic next-permutation step (find the last ascent, swap with the last larger
  element, reverse the suffix). From memory: Narayana Pandita's algorithm, as given in
  Knuth, *The Art of Computer Programming* Vol. 4A, §7.2.1.2, Algorithm L (which handles
  repeated elements). Only the strictness of the two comparisons is my choice.
- **Feasibility of a linearization**: my own derivation from the specification.
  - Reduction of full schedules to effect orders: an effect order is realisable by
    distinct effect points inside the intervals iff it extends the interval order
    (`a` before `b` whenever `end(a) < start(b)`). The greedy argument
    `pi(a_i) = max(start(a_i), pi(a_{i-1}) + eps)` is the standard one for interval
    orders (Fishburn, *Interval Orders and Interval Graphs*, 1985, as I recall it);
    I re-derived it rather than quoting it.
  - The walk of `L` in which effects only happen just before `done` nodes, and the
    state set `(pending actions, block contents, values of reads that later writes
    depend on)` reachable at each prefix, are my own construction.
  - Dropping actions that cannot influence any observed read (relevance fixpoint), the
    necessary "some writer can still deliver the observed term" prune, and the memo of
    `(chain positions, state set)` pairs with no feasible completion are my own.
- **Enumeration order**: depth-first over interleavings, lexicographic in the thread
  index sequence, so both code paths yield in the same order.

## `fable51_1-o-count` (counter)

- `|Lin(P)|` for `K = 0` is the multinomial coefficient `n! / prod |chain_t|!`.
- `|LinFeas(P)|` is the same state-set walk, memoised on `(chain positions, state set)`:
  the number of feasible completions of a prefix depends only on these two. My own
  derivation. When the setup has no observed reads `LinFeas(P) = Lin(P)` (spec §5), so
  `feasible` is filled with the multinomial as well.

## Points I was unsure about

- Whether the grader wants `feasible` filled or `None` on setups without observations.
  I fill it with `|Lin(P)|`, which is the value spec §5 defines.
- Growth of the state sets on large setups with many concurrently pending relevant
  actions; correctness does not depend on it, only speed.
- I could not run anything, so the iterative DFS bookkeeping (`ptr`, `found`, `dead`)
  was checked by hand only.
