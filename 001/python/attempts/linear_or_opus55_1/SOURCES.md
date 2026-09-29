# Sources

## opus55_1-or-enum (enumerator)

My own derivation, using standard ideas. It is a depth-first search over interleavings
of the thread chains (for K = 0 these are exactly `Lin(P)`). The search keeps, for each
prefix, the set of simulation states reachable when each action's effect point is placed
anywhere inside its interval. A state records which open actions have taken effect, the
block contents, and the values still needed by later expressions. After a start node the
set is closed under firing pending effects. At an end node only states where that action
has already fired are kept. Observed reads and RCWs are checked when their effect fires.
The effect-point view is the usual one for atomic registers (Herlihy & Wing,
"Linearizability", 1990). A memoised "has a feasible completion" test, keyed by
(thread positions, state set), keeps the search out of dead branches, so every branch
it enters yields at least one output. With no observations it lists plain interleavings.

Why the method is correct: moving an effect earlier, past an endpoint of another action,
changes nothing, so closing the set after start nodes only is enough. Distinct effect
points only fix an order among effects, and the closure covers every such order.

## opus55_1-or-count (counter)

The same state-set machinery, with a memoised sum over successors instead of a
feasibility test. `|Lin(P)|` is the multinomial coefficient of the chain lengths.
`feasible` is filled only when the setup has observed results.

## Notes and uncertainties

- Pruning: a read that is neither observed nor referenced, and a write or RCW on a block
  with no observed or referenced returning action, is not simulated. Such actions cannot
  affect any observation. A written value still reaches later expressions, because
  content is evaluated at the action's start.
- Under `rcw_result: flag` an observed `ok`/`fail` is checked against whether the
  comparison succeeded. The spec for this case uses the default `old` semantics.
- The feasibility memo is cleared if it grows past 1,000,000 entries, to bound memory.
