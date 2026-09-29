# Sources

## opus55_1-o-memo (`memo_solver.py`)

My own derivation, using a standard idea about interval orders.

- **Reduction.** A total order of the actions is the effect order of some full schedule
  exactly when it extends `a <_Q b iff done(a) <_P start(b)` (mode `all`), or
  `pos_L(done(a)) < pos_L(start(b))` (mode `fixed`). In mode `fixed` this is the usual
  interval-order fact: points can be picked inside intervals in a given order iff no
  interval that comes later in the order lies entirely before an earlier one. In mode
  `all`, sufficiency comes from a greedy construction. Take the actions in the order
  given. For each one, emit the P-down-set of its start that has not been emitted yet,
  then place its effect point. That down-set holds only starts and the ends of actions
  already placed. An end of a later action there would break the condition.
- **Search.** A memoised DFS over the linear extensions of `Q`. The state is (the bitmask
  of actions done, the block contents, the values of reads that pending writes still
  need). Reads that contradict their observation are pruned. A state is live if some
  completion reaches the end. A read's value is counted only on an edge into a live
  state. The final contents are the contents of the terminal states that are reached.
  Terms are interned to ints.
- **Write contents.** A write's content is its expression with each reference replaced:
  a referenced read gives its recorded value, and a referenced write gives its own content,
  computed recursively. A write's referenced reads all end before the write starts, so
  they are always done when the write takes effect.

Unsure about: performance on the larger timing setups. The state space can still grow
exponentially. No witnesses are returned.
