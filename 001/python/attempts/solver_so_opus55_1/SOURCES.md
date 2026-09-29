# Sources

## opus55_1-so-exact

Own derivation, using a standard fact about interval orders / scheduling with
intervals.

- A full schedule matters only through its effect order sigma. Adding an effect node
  e(a) with start(a) < e(a) < end(a) to P and chaining the e's in sigma order gives an
  acyclic graph iff sigma never places b before a when end(a) <_P start(b) (any cycle
  must contain a backward segment e(x) < end(x) <=_P start(y) < e(y) with y before x).
  So the realizable effect orders over Lin(P) are exactly the linear extensions of
  `a -> b iff end(a) <_P start(b)`. For a fixed L the relation is
  `pos_L(end(a)) < pos_L(start(b))`.
- The solver runs a memoized DFS over states (executed set, block contents, values of
  reads still needed by pending writes). Observed reads prune transitions. A state is
  "good" if it can be completed feasibly; a read value is recorded on a transition from
  a reached state into a good state, and final contents at the full state. This yields
  Poss exactly, and consistency = root is good.
- Write contents are evaluated at effect time: all reads a write depends on (directly or
  through earlier writes) end before its start in program order, so they have already
  taken effect.

Unsure: none major; no witnesses are returned (`witnesses=False`).
