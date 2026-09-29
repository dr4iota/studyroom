# Sources

## `opus55_1-o-enum` (LinEnumerator)

This is my own derivation. It builds on two standard ideas I recall from memory:
- Enumerating the linear extensions of a union of chains (interleavings) by backtracking
  depth-first search.
- Checking linearizability of a history by simulating the object while tracking the set
  of reachable states. This is the Wing & Gong style search (J. Wing, C. Gong, "Testing
  and verifying concurrent objects", 1993), made into a set-of-states frontier as in
  P-compositionality / Lowe's "just-in-time linearization" checkers (G. Lowe, "Testing for
  linearizability", 2017).

What I changed or added:
- The history (L) is not fixed; it is built node by node. A prefix carries the exact set of
  configurations `(block contents, started-but-not-effected actions, needed values)`.
- A start adds the action to the pending set. At the end of `a`, the search effects any
  sequence of other pending actions, then `a`. This produces exactly the effect orders
  that extend the interval order of L. Those are exactly the orders that distinct effect
  points inside the closed intervals can realise (greedy placement argument).
- Pruning: completions depend only on `(chain positions, configuration set)`, so the
  search memoises that key for every subtree that produced nothing. Each dead key is
  explored at most once (the memo is cleared if it grows past a cap).
- Relevance analysis: the simulation ignores reads that are unobserved and unused by any
  relevant write, and writes to blocks that no relevant read looks at. Block contents
  and env values that can no longer matter are set to `None` so that equivalent states
  compare equal.
- If the setup has no observed reads, it falls back to plain interleaving enumeration.

## `opus55_1-o-count` (LinCounter)

This is my own derivation, using the same state machine. It is a memoised DP over the key
`(chain positions, configuration set)` that counts feasible completions.
`|Lin(P)|` is the multinomial coefficient of the chain lengths (K = 0).

## Unsure about

- `CountResult.feasible` is left `None` when the setup has no observed reads. I took the
  task text literally ("fill `feasible` ... when the setup has observed reads").
- I could not run the code, so it has not been tested.
