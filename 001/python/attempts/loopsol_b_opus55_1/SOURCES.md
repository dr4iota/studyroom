# Sources

## `opus55_1-b-explore` (`solver.py`)

- **Reducing schedules to effect orders:** my own derivation from the spec. Starts and
  ends do not touch memory. Within one thread, an effect order works exactly when it
  extends the order "a ends before b starts". With no sync points the threads are
  independent, so any interleaving of the per-thread effect orders comes from some
  linearization (place each point greedily in its interval, then merge the threads).
- **Explicit-state exploration:** the standard model-checking idea: search the
  reachable global states with a visited set. Nothing ever blocks, so every reachable
  state completes. This makes a possibility set the set of values seen at reachable
  states, so no backward pass is needed. The liveness pruning of stored read values is
  my own.
- **All n in one search:** my own derivation. A state before any thread leaves its body
  is valid for every n at least its largest iteration index. Once a thread leaves, n is
  fixed. Levels go by the largest iteration index, which makes the answers exact for
  every n up to the deepest level finished.
- **Partial-order reduction:** adapted from what I recall of persistent/ample sets
  (Godefroid, "Partial-Order Methods for the Verification of Concurrent Systems", 1996;
  Peled, "All from one, one for all: on model checking using representatives", 1993;
  Valmari's stubborn sets). What I changed: a single thread is expanded when all its
  enabled effects commute with everything the other threads may still do. The state
  graph is acyclic, so no cycle condition is needed. The facts collected are values of
  individual read events and final states, and these do not change under the
  reordering.
- **Beyond the explored n:** my own heuristic. Facts seen before any thread leaves its
  body hold for every larger n, which is exact. For other facts, the membership over
  `1..N` is extended by the shortest period that has been seen at least twice. If no
  period fits, the last value is used.

## Unsure

- The extension past the deepest explored level is **not proven exact**. It is exact
  when the threshold and period of a fact's membership in n both fit inside the
  explored range (threshold plus two periods). That range depends on the time budget
  and the setup's size.
- The time budgets (about 4 to 8 s before starting a new level, and an abort at 13 s,
  resumable on the next call for the same setup) assume the 20 s limit per call.
