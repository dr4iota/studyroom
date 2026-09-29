# Sources

## opus55_1-br-effect-dp

Own derivation, using standard ideas I recall: the linearizability / interval-order view
of atomic registers (Herlihy and Wing, "Linearizability: a correctness condition for
concurrent objects", 1990: an operation takes effect at a point inside its interval) and
memoised state-space exploration over downsets of a partial order.

Reduction. Build a graph from the trace poset (or the fixed `L`), one node per effect
point `pi(a)` with `start(a) < pi(a) < end(a)`, and the chain of a candidate effect order
`sigma`. A full schedule with effect order `sigma` exists iff this graph is acyclic. Any
cycle is a sequence of effect points where each step is either forward in `sigma` or
`a -> b` with `end(a) <= start(b)` (in `P`, resp. in `L`). So `sigma` is realisable iff it
extends the relation `a -> b iff end(a) < start(b)`; the converse holds since
`pi(a) <= end(a) < start(b) <= pi(b)`. Effect points on interval endpoints can be nudged
inside because effect points are distinct.

Algorithm. DFS over states `(executed set, block contents, values of reads still
referenced by an unexecuted write/RCW)`, adding any action whose predecessors are all
executed, applying atomic semantics (RCW: return old content, write its content iff old
equals the evaluated expected value). Results are recorded on every transition, final
contents at the full state. The state determines the future, so memoisation is exact.
Content of a write/RCW is evaluated lazily from its data; every read it depends on
(transitively through referenced writes) ends before its start in program order, so it
has already taken effect. Terms are interned to ints; contents are cached per
(action, values of its read dependencies).

Modes: `all` (precedence from reachability in `P`) and `fixed` (from positions in `L`).
No witnesses.

Unsure about: nothing specific; the argument does not use the absence of sync points, but
the capability is declared `sync=False` as the task requires.
