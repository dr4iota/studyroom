# Sources

## `opus55_1-or-memo`

My own derivation. It uses a well-known fact about interval orders (atomicity and
linearizability, Herlihy and Wing, "Linearizability: A Correctness Condition for Concurrent
Objects", 1990): a point can be chosen inside each interval in a given order iff that order
never puts `b` before `a` when `a` ends strictly before `b` starts.

- **Reduction.** In mode `all`, an effect order `sigma` can be realised by some `(L, pi)` iff
  `sigma` extends `a < b <=> done(a) <_P start(b)`. The constraint graph (the edges of `P`,
  `start(a) -> pi(a) -> done(a)`, and the chain of `sigma`) has no cycle iff no `sigma` edge
  goes backwards against that relation. In mode `fixed`, the relation is
  `pos_L(done(a)) < pos_L(start(b))`, and a greedy choice of points proves the claim.
- **Search.** A memoised DFS over effect orders. A state is (executed set, block contents,
  values of executed reads that some unexecuted write or RCW still needs, possibly through
  write-to-write references). It returns the bitset of facts, meaning (read or RCW, old
  value) and (block, final value), that some feasible completion yields. It returns None
  when no completion satisfies every observation. A write's content is its data with the
  referenced reads' values put in; the needed reads always take effect first, because they
  end before the write starts in program order.
- RCW: it returns the old content; it writes when the evaluated `expect` equals the old
  content structurally. An observed RCW result is matched against the old content (or
  against success or failure for `ok`/`fail`, as a precaution).

## Unsure

- I assume the RCW result semantics is `old`, as the task states. I added the `ok`/`fail` flag
  handling but did not check it against anything.
- There are no witnesses (`witnesses=False`).
