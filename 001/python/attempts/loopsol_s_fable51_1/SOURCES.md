# Sources

## `fable51_1-s-effects` (`effects.py`)

**Reduction to effect orders (own derivation).** I derived that the effect orders
realizable by some full schedule `(L, π)` are exactly the linear extensions of the
relation `a < b iff done(a) precedes start(b) in the trace poset`. One direction is
immediate; for the other, adding the edges `start(a_i) -> done(a_j)` (`i < j`) for a
linear extension keeps the poset acyclic, and effect points can then be chosen greedily
left to right. The step resembles the classical interval-order view of real-time
precedence in linearizability (Herlihy and Wing, 1990), which I had in mind, but the
argument above is my own and specific to this spec (linearization chosen freely,
distinct effect points).

**State exploration (adapted from a standard technique).** Linear extensions are walked
as paths through down-sets, with block contents and live read values added to the
state so that read-dependent write data is handled exactly. This is the usual
down-set / lattice-of-ideals enumeration of linear extensions, with deduplication on the
full state. The register-slot sharing across iterations of one template read is my own
observation (all users of a body read lie in its own iteration).

**Large `n` (own heuristic).** Exact answers are computed for `n = 1, 2, ...` within a
time budget; if the requested `n` is not reached, the sequence is extended by its
smallest observed eventual period, accepted only when the periodic tail covers at least
`2p + 2` values. The periodicity itself is suggested by lockstep setups that rotate
values between blocks each iteration; I have no proof of a bound on the pre-period or
the period, so this part is the one I am least sure about. For `n` reached by the
sweep the answer is exact.

## Uncertainties

- The time budgets (6 s soft, 11 s hard, 1.2 M states) are guesses for the grader's
  machine.
- Setups with four or more mutually unsynchronized threads make the state space grow
  quickly, so the sweep may stop at small `n` and the extrapolation may then rest on
  few values.
