# Sources

## `opus55_1-sr-downset` (solver.py)

An adaptation of well-known ideas, put together by me:

- **Effect orders = linear extensions of the real-time order.** This is the standard
  characterization behind linearizability (Herlihy and Wing, "Linearizability: A
  Correctness Condition for Concurrent Objects", 1990): an effect order is realizable iff
  it respects "a ends before b starts". I adapted it to the trace poset: in mode `all`,
  "ends before" means `done(a) <_P start(b)` in the poset (including sync edges); the
  proof (adding effect nodes between start and done and chaining them; a cycle needs a
  backward real-time edge) is my own sketch, written in the module docstring. In mode
  `fixed` it is the interval order of the given linearization.
- **Search.** DFS over downsets (ideals) of that order, with memoisation on
  `(downset, block contents, read values still referenced by pending writes)`, in the
  spirit of the Wing and Gong / Lowe style linearizability checkers with state caching
  (Lowe, "Testing for linearizability", 2017). Every reachable state extends to a full
  schedule, so the collected sets are exact.

Unsure: none about correctness; performance on large setups depends on the number of
downsets times distinct content combinations. No witnesses are returned.
