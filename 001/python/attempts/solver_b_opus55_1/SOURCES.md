# Sources

## opus55_1-b-reach

My own derivation. It uses standard ideas: a DP over the downsets (order ideals) of a
poset to walk its linear extensions, and the interval-order view of effect points.

- **Reduction.** With K = 0, the effect order sigma can be realized by some (L, pi)
  exactly when sigma extends the relation "a -> b iff a and b are in the same thread
  and done(a) comes before start(b) in program order". In mode "fixed" the relation is
  instead "pos_L(done(a)) < pos_L(start(b))", the interval order. My argument for this:
  - Necessity is immediate.
  - Sufficiency, for "all": every cycle in the constraint graph (program order, start <
    effect < end, sigma) contains a required edge that sigma reverses. Threads are
    independent, so the real-valued times can be merged into one L.
  - Sufficiency, for "fixed": choose each point greedily in sigma order.
- **Search.** Forward reachability, layer by layer, over states (executed set, block
  contents, values of executed reads that some unexecuted write still depends on). Terms
  are interned to ints.
  - A block's content is dropped when no read of it remains but a write does. This
    changes nothing that can be observed, including the final content.
  - A write's content depends only on reads that precede it in the relation, because
    they end before it starts. So its content is known when it executes.

Unsure about: nothing specific. I could not read `harness.semantics`, so I do not return
witnesses (`witnesses=False`).
