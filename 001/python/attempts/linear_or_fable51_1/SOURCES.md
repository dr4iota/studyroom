# Sources

## `fable51_1-or-enum` (enumerator, `linfeas.py`)

Own derivation, built from two observations.

1. *Interval orders.* A linearization `L` gives each action a closed integer interval
   `[pos(start), pos(end)]`, and a full schedule `(L, π)` with distinct effect points is
   equivalent to a total order `T` of the actions that extends the interval order of `L`
   (`a` before `b` whenever `end(a)` precedes `start(b)`). One direction is immediate;
   for the other, a greedy assignment `π(a) = max(pos(start a), π(prev) + δ)` stays inside
   the intervals for small enough `δ`, because a chain of pushed points starts at some
   `pos(start c)` with `c` before `a` in `T`, and `T` extending the interval order gives
   `pos(start c) < pos(end a)`. This is the standard fact that every linear extension of
   an interval order is realised by points of the intervals (Fishburn, *Interval Orders
   and Interval Graphs*, 1985, as I recall it); the argument above is my own check of it.

2. *Incremental execution.* Such a `T` can be produced while `L` is built node by node:
   execute an action at any moment after its start is placed and before its end is
   placed. So the enumerator does a depth-first search over interleavings of the thread
   chains and carries the set of partial executions compatible with the prefix (executed
   open actions, block contents, and the values of unobserved reads that later
   expressions still need), closed under executing any executable action whose observed
   result matches. This is a subset-construction / powerset-simulation idea applied to
   the schedule search; I know no specific paper for it.

Simplifications I convinced myself are sound: unobserved reads referenced by no
expression are never tracked; the values of unobserved reads are dropped from the state
once every action whose content or expected value (transitively) depends on them has
executed; once all observed actions have ended, every completion is feasible and
tracking stops.

## `fable51_1-or-count` (counter, `linfeas.py`)

Same machinery, with memoisation on (chain positions, state set): the future of a
prefix depends only on these. `|Lin(P)|` is the multinomial coefficient of the chain
lengths (K = 0). With no observations, `feasible` is reported equal to `|Lin(P)|`.

## Unsure about

- Whether the reference `feasible` for a setup without observations is `|Lin(P)|` or
  `None`; I report `|Lin(P)|` since `LinFeas(P) = Lin(P)` then.
- The `rcw_result: flag` semantics (`"ok"`/`"fail"` observations) are not part of spec
  v2 §4 but exist in the model; I treat `"ok"` as "old content equals the expected
  value" and `"fail"` as its negation.
- Memory use of the state sets on adversarial large setups with many overlapping
  actions; the state set is bounded by (subsets of open actions) × (content variants).
