# Premise: Trace Analysis for Asynchronous Multi-Threaded Block I/O

Status: v0.2 (derived from `statement.draft.md`; vocabulary revised 2026-09-28)

This document fixes the *problem class* we are studying: the objects, the semantics,
the hyperparameters, and the precise questions each sub-problem must answer. It is
meant to be the shared contract for every sub-project (generator, linearizer, solver,
validator). `surveys.md` places the class in the literature; `visions.md` lists what
we could build and study.

---

## 0. Vocabulary (read this first)

Three words are reserved and must not be mixed up:

| Word | Meaning | Symbol |
|---|---|---|
| **action** | a paired I/O: `Read`, `Write`, or `RCW` on one block, with a start and an end | `a ∈ A` |
| **endpoint** | the start or the end of an action | `start(a)`, `end(a)` |
| **event** | a synchronization primitive: `before(h)`, `after(h)`, `at(h)` on a sync point `h` | `ev ∈ V` |
| **step** | anything that receives a timestamp: an endpoint or an event | `x ∈ S = Endpoints ∪ V` |
| **sync point** | a named virtual instant that events refer to ("semaphore" in the draft) | `h ∈ H`, `|H| = K` |

We avoid the letter `O` (indistinguishable from `0`) and the word "operation".
"Thread" is kept; "process" and "session" in the literature mean the same thing.

---

## 1. Informal picture

- There are `N` threads, `M` storage blocks and `K` sync points (`K = 0` means no
  synchronization at all).
- Each thread issues *asynchronous* I/O **actions** on blocks. Each action has a
  **start endpoint** and an **end endpoint**. Because I/O is asynchronous, one thread may
  have several actions in flight, so its actions may overlap in time.
- Action kinds: `Read`, `Write`, and optionally `RCW` (atomic Read-Compare-Write, i.e.
  compare-and-write / CAS on a block).
- Optionally, threads are coupled through **events** on sync points. Each sync point
  `h` is a virtual instant; a thread can declare that one of its steps happens
  `before(h)`, `after(h)`, or `at(h)` (a rendezvous / barrier). This single mechanism
  expresses the draft's happens-before, happens-after and happens-at-the-same-time
  relations.
- Each thread's **steps** (its endpoints and events) are totally ordered: its
  *program order*. Across threads the order is unknown except where sync points
  constrain it.
- A **linearization** is a single global sequence of all steps consistent with all
  program orders and all sync constraints. We represent it by increasing integer
  timestamps (only the order matters).
- Given a linearization, each action becomes an *interval* `[ts(start(a)), ts(end(a))]`.
  The block behaves as a per-block *atomic register*: each action "takes effect" at one
  instant inside its interval, and a read returns the content of the most recent
  effective write to that block (or the initial content).
- Contents may be **partially known**: some write contents are known, some read contents
  are observed, the rest are unknown. Write contents may be constants or expressions
  over earlier reads by the same thread.

The questions we ask: (a) generate such setups; (b) enumerate or sample
linearizations; (c) for each read (and for the final block states), compute *exactly*
the set of contents that are possible, "no more, no less"; (d) validate all of the above.

---

## 2. Formal model

### 2.1 Structure

| Symbol | Meaning |
|---|---|
| `T = {1..N}` | threads |
| `B = {1..M}` | blocks |
| `H = {h_1..h_K}` | sync points |
| `A` | actions; each `a` has `thr(a) ∈ T`, `blk(a) ∈ B`, `kind(a) ∈ {R, W, RCW}` |
| `start(a), end(a)` | the two endpoints of action `a` |
| `V` | events; each `ev` has `thr(ev) ∈ T`, `sp(ev) ∈ H`, `rel(ev) ∈ {before, after, at}` |
| `S` | steps: all endpoints and all events, `|S| = 2|A| + |V|` |
| `<_prog` | program order: a total order on the steps of each thread |
| `<_sync` | edges induced by events (see 2.2) |
| `P = (S, <_P)` | the *trace poset* |

Well-formedness: `start(a) <_prog end(a)`; `P` is acyclic; a sync point referenced by
no event is allowed (it is simply unused).

### 2.2 Sync semantics

Each sync point `h` is modelled as a **virtual step** `ĥ` added to the poset. Events
become edges to or from that virtual step:

| Event | Constraint |
|---|---|
| `before(h)` on step `x` | `x <_P ĥ` |
| `after(h)` on step `x` | `ĥ <_P x` |
| `at(h)` on step `x` | `x ≡ ĥ` (merged with `ĥ`; all `at(h)` steps share one timestamp) |

Consequences (all derived, none extra): every `before(h)` precedes every `after(h)`;
every `before(h)` precedes every `at(h)`, which precedes every `after(h)`; several
`at(h)` events on different threads form a barrier. A thread may reference the same
`h` more than once (e.g. `before(h)` then `after(h)`); the reverse order in one thread
creates a cycle and the setup is invalid. Reuse of a sync point for a second
rendezvous is *not* allowed: use another sync point (this keeps `K` meaningful as a
count of distinct synchronization instants).

The virtual steps `ĥ` are placed in the linearization like any other step but carry no
I/O meaning. Because `at(h)` merges steps, `P` is formally a partial order on
equivalence classes; a linearization is a linear extension of that quotient.

**Width observation.** `P` is a union of `N` thread chains plus the `K` virtual steps
and cross edges, so `width(P) ≤ N + K` (and `≤ N` when every sync point has at least
one `at` or is otherwise ordered against some thread). This single fact drives much of
the complexity landscape: many problems that are hard in `|S|` become polynomial for
fixed `N` (see `surveys.md` §3).

### 2.3 Linearization (level 1)

A *linearization* `L` is a linear extension of `P`: a map `ts : S → ℕ` that is
injective on equivalence classes, constant within them, and satisfies
`x <_P y ⇒ ts(x) < ts(y)`. `Lin(P)` is the set of all linearizations.

Under `L`, each action has interval `I_L(a) = [ts(start(a)), ts(end(a))]`. Two actions
are *concurrent* under `L` if their intervals intersect; otherwise one *precedes* the
other. The precedence relation on actions induced by `L` is an **interval order**.

### 2.4 Effect points and block semantics (level 2)

Fix `L`. An *effect assignment* `π` picks for each action `a` a point
`π(a) ∈ I_L(a)`, all distinct (equivalently: a linear order of actions consistent with
the interval order of `L`). The block is an **atomic (linearizable) register per block**:

- `Write(b, v)` at its effect point sets `content(b) := v`.
- `Read(b)` at its effect point returns the current `content(b)` (`init(b)` if no write
  has taken effect).
- `RCW(b, expected, new)` at its effect point: if `content(b) = expected` then
  `content(b) := new`; the result is the old content (from which success/failure is
  derived). This mirrors NVMe/SCSI compare-and-write.

We call `(L, π)` a **full schedule**. There are two independent sources of
nondeterminism: the interleaving of steps (`L`) and the effect point inside each
interval (`π`). The draft's "solver" lives at level 2 for a fixed `L`, and at both
levels when `L` is not fixed. We keep both variants (see §4).

Alternative semantics available as hyperparameters (not default): regular register,
safe register (Lamport 1986), torn writes (sub-block granularity), non-atomic RCW.
See `surveys.md` §5.

### 2.5 Content model

Values live in a domain `Val`. Write contents are *terms*:

1. **Constant**: `c ∈ Val` (we use natural numbers).
2. **Constant plus previous read**: `f(c, x)` where `x` is the value returned by an
   earlier *completed* read of the same thread (its end endpoint precedes the write's
   start endpoint in program order).
3. **Combination of previous reads**: `g(c, x_1, …, x_k)`.

We treat terms **symbolically and non-commutatively** (written `a~b` in `formats.md`;
`a~b ≠ b~a`): a
term is an AST, equality is structural, and a term records which reads fed it. This
makes the history *recoverable* from observed values (the same trick that lets Elle
infer version orders from list-append). Interpreting terms in an actual algebra
(e.g. integers with addition) is a separate hyperparameter.

Knowledge dimensions (hyperparameters):

| Parameter | Meaning |
|---|---|
| `p_w ∈ [0,1]` | fraction of write contents that are *known* to the analyzer (the rest are unknown symbols) |
| `p_r ∈ [0,1]` | fraction of read results that are *observed* (given as constraints) |
| `init` | initial contents known / unknown |

With `p_w = 1, p_r = 0` the problem is pure forward *prediction*. With `p_r > 0` it
becomes *inference / consistency checking*: observed reads constrain which full
schedules are feasible, and hence what other reads and unknown writes can be.

### 2.6 Feasibility and possibility (the central definitions)

A full schedule `(L, π)` together with an assignment `θ` of values to unknown write
symbols determines, by running the register semantics, a value `val_{L,π,θ}(r)` for
every read `r` and a final content `fin_{L,π,θ}(b)` for every block. `(L, π, θ)` is
**feasible** iff every observed read result and every observed RCW result matches.

- `Poss(r) = { val_{L,π,θ}(r) : (L, π, θ) feasible }` — possible contents of read `r`.
- `Poss(b) = { fin_{L,π,θ}(b) : (L, π, θ) feasible }` — possible final contents of `b`.
- `Poss_L(r)`, `Poss_L(b)` — the same with `L` fixed (level-2 only).
- The *joint* possibility set `Poss(r_1, …, r_k)` is generally **not** the product of the
  individual sets; individual sets are projections.

"No more, no less" means the solver must output exactly `Poss(·)`: every returned value
must be witnessed by some feasible full schedule, and every feasible value must be
returned.

---

## 3. Hyperparameters of a setup

| Group | Hyperparameter |
|---|---|
| Size | `N` threads, `M` blocks, `K` sync points, actions per thread (or total per kind), events per thread |
| Kinds | enable `RCW`? which event relations (`before`/`after`/`at`) are allowed? |
| Shape | max in-flight actions per thread (1 = synchronous I/O), read/write ratio, block access skew, sync density, threads per sync point |
| Content | term class (1/2/3 of §2.5), value domain, `init` known? |
| Knowledge | `p_w`, `p_r` |
| Semantics | atomic / regular / safe register; torn writes |
| Seed | RNG seed (all generation must be reproducible) |

Hardness dials suggested by the literature (see `surveys.md`): writers per block
(1 / 2 / 3+), number of preemptions in the hidden schedule, fraction of repeated
constants.

---

## 4. The sub-problems, stated precisely

### GEN — Generation
Input: hyperparameters + seed. Output: a *setup*: `N`, `M`, `K`, per-thread step
sequences (endpoints and events), contents (write terms; observed read results where
`p_r` applies). The output must be well-formed (§2.1–2.2) and, when `p_r > 0`,
**realizable**: the observed values must come from at least one feasible full schedule
(the generator produces them by actually running one hidden schedule).

### LIN-SAMPLE — Randomized linearization
Input: setup. Output: one `L ∈ Lin(P)`. Variants: (a) any valid `L` (cheap);
(b) *uniform* over `Lin(P)`; (c) uniform over *feasible* `L` given observations.

### LIN-ENUM — Enumerate linearizations
Input: setup. Output: all of `Lin(P)`, ideally with constant amortized time per
element (Gray-code style: consecutive linearizations differ by an adjacent swap).

### LIN-COUNT — Count linearizations
Input: setup. Output: `|Lin(P)|`. Needed for uniform sampling and validator checks.

### SOLVE-READ, SOLVE-FINAL — Possibility sets
Input: setup (and optionally a fixed `L`). Output: `Poss(r)` for one or all reads;
`Poss(b)` for all blocks. Exactly, no more, no less.

### SOLVE-INC — Incremental / online solver
Steps (or observed values) arrive one at a time; maintain possibility sets with
bounded work per step. Possibility sets only shrink as observations are added and only
grow as new unconstrained steps are appended; the solver must respect both.

### CHECK — Consistency of an observed history
Input: setup with `p_r = 1` (all read results observed). Output: is there a feasible
full schedule? This is linearizability checking of read/write(/CAS) registers,
NP-complete in general (Gibbons & Korach 1997). It is the special case of SOLVE where
every possibility set is tested for non-emptiness, and the natural lower bound on
solver difficulty.

### VAL-LIN, VAL-ENUM, VAL-SOLVE — Validators
- VAL-LIN: is a given `L` a linear extension of `P`? (polynomial, trivial)
- VAL-ENUM: does an enumerator output exactly `Lin(P)`, each once? (compare against a
  reference enumerator or against `LIN-COUNT`, plus per-item VAL-LIN)
- VAL-SOLVE: is a solver's output exactly `Poss(·)`? Soundness is witnessed by a
  feasible full schedule per returned value; completeness is checked against a
  brute-force reference on small instances.

---

## 5. Dependencies between sub-problems

```
GEN ──► (setup) ──► LIN-ENUM / LIN-SAMPLE / LIN-COUNT ──► SOLVE-* ──► VAL-*
                    ▲                                        │
                    └──────── brute-force reference ◄────────┘
```

- Everything consumes one shared on-disk format, specified in `formats.md`.
- The brute-force pipeline (enumerate `L`, enumerate `π`, enumerate `θ` over a finite
  domain) is the oracle for all validators. It is exponential but sufficient for small
  `N, M, K, |A|`.
- Fast algorithms are accepted only after differential testing against the oracle.

---

## 6. Modeling decisions

Settled (v0.2):
1. **Same-time semantics**: `at(h)` steps are merged with the virtual step `ĥ`
   (quotient poset). One timestamp per sync point.
2. **Sync points are single-use instants**: `K` counts distinct synchronization
   instants; a second rendezvous needs a second sync point.
3. **RCW returns the old content** (subsumes success/failure).

Still open:
4. **Distinct effect points.** Do we allow two actions to take effect at the same
   instant? Recommendation: no (strict total order of effects).
5. **Unknown-write value domain.** Finite (enumerable) or a free symbol. Recommendation:
   free symbol with symbolic equality; interpret only when a validator needs concrete runs.
6. **Term algebra.** Purely syntactic (recommended) vs. interpreted (e.g. integer addition).
   Interpreted algebras create collisions (`1+2 = 2+1`) that hide history.
7. **Reads feeding writes.** Only *completed* reads may feed a later write (recommended).
8. **Can an event sit between the endpoints of an in-flight action?** Recommended: yes;
   an event is just a step in program order and does not interact with I/O.

---

## 7. Glossary

- **Action**: paired I/O (`Read`/`Write`/`RCW`) with two endpoints. Set `A`.
- **Endpoint**: `start(a)` or `end(a)`.
- **Event**: `before(h)`, `after(h)`, `at(h)` on a sync point `h`. Set `V`.
- **Sync point**: named virtual instant `h ∈ H`, `|H| = K`; realized as virtual step `ĥ`.
- **Step**: endpoint or event (or virtual step); the unit that gets a timestamp. Set `S`.
- **Trace poset `P`**: program order plus sync edges, on steps.
- **Linearization `L`**: linear extension of `P`; equivalently, timestamps.
- **Interval order**: precedence between actions induced by `L`.
- **Effect point**: the instant an action takes effect, inside its interval.
- **Full schedule**: `(L, π)`; **feasible** when consistent with all observations.
- **Possibility set `Poss(·)`**: values witnessed by at least one feasible full schedule.
- **Width**: size of the largest antichain of `P`; here `≤ N + K`.
