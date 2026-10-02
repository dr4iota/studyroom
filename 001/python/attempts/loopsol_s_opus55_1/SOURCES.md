# Sources — loopsol_s_opus55_1

One algorithm: `opus55_1-s-statespace` (`solver.py`).

## Parts and where they come from

- **Effect orders as an operational search.** I derived this myself. A full schedule
  `(L, pi)` is the same as an interleaving of all thread steps, the virtual sync steps and
  one effect step per action between its start and its end. The atomic semantics are then
  just a simulation over block contents. The idea is close to the usual
  linearization-point view of atomic objects (Herlihy and Wing, "Linearizability: a
  correctness condition for concurrent objects", TOPLAS 1990), which I recall from
  memory; I adapted it to this setting.
- **Eager non-effect steps.** My own derivation. Starts, dones, before/after events and
  `at` firings only ever enable other steps, so moving them as early as possible keeps the
  same observations. That makes the closure unique, so only effects and loop/leave choices
  branch.
- **All iteration counts in one search.** My own derivation. Each thread keeps its own
  iteration counter, up to a cap `L`, and may leave its body after any iteration. A
  complete run is kept only when all threads leave after the same count `c`; these are
  exactly the runs of `P_c`. Every path to a state has the same length, so the state
  graph is layered. A backward pass over the layers gives each state a bit mask of the
  counts it can complete with. A read observation on an edge counts for the counts in the
  target state's mask. Per-iteration sync guards compare the counters exactly.
- **Reduction.** Adapted from persistent / stubborn sets in partial-order reduction
  (Godefroid, "Partial-Order Methods for the Verification of Concurrent Systems", LNCS
  1032, 1996; Valmari's stubborn sets), recalled from memory. I use only the simplest
  case, a persistent set of size one: take an effect alone when it conflicts with no
  access the other threads can still make and with no overlapping action of its own
  thread. Every action is effected in every complete run, so that effect can be commuted
  to the front of any complete run. This keeps one run from every equivalence class with
  the same observations and the same count.
- **Large `n`.** A heuristic of my own. The search is exact for every `n` up to the
  largest cap that fits a time budget (caps grow by about 1.5 each step, up to 400). For
  larger `n`, the exact answer sequence `Poss_1 .. Poss_L` is extended by its detected
  eventual period `(T, p)`. I take the smallest `p` whose repeat has been seen over at
  least `max(3p, p+4)` trailing values, or else the pair minimising `T + p`.

## Uncertainties

- **The extension beyond the cap is not proved.** Values here come from a finite set and
  the body only copies, so I expect the answers to be eventually periodic in `n`. I have
  no bound on the threshold or period that would guarantee the cap is large enough. When
  many threads drift freely, the affordable cap may be small (around 10–20), and the
  extension could then be wrong if the threshold or period is longer than that.
- **Time is budgeted, not guaranteed.** A single call can still take longer than the
  budget: the first table (cap 2, or `n` if smaller) always runs to completion, and the
  backward pass comes on top of the budgeted forward search.
- **Results are cached per setup** (keyed by its content) across calls. Later calls on
  the same setup reuse the table, or extend it if the earlier call stopped only because
  its `n` was small.
