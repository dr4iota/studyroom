# Visions: What We Could Build and Study

Status: v0.2, 2026-09-29. Companion to `premise.md` (formal definitions) and `surveys.md`
(literature). This is a menu, not a plan: each item is a candidate sub-project with its
inputs, outputs, dependencies, and the questions it would answer. §7 proposes how to
cut the menu into separately-owned pieces with shared code. §10 lists problems for
testing AI models on questions the literature does not answer.

The section "Terms" below defines everything this document uses, so it can be read
without the code. `premise.md` gives the same definitions formally.

---

## Terms (read first)

### The setting

- **Threads, blocks, sync points.** There are `N` threads, `M` storage blocks and `K`
  sync points.
- **Action.** A `Read` of one block, or a `Write` of one block with some data (and,
  as an extension, an `RCW`: an atomic compare-and-write, see
  [compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)).
  - Every action has a **start** and an **end** endpoint.
  - I/O is asynchronous: a thread may start several actions before any of them
    ends, so one thread's actions can overlap in time.
- **Event.** A step that refers to a sync point `h`:
  - `before(h)`: this step happens before `h`;
  - `after(h)`: this step happens after `h`;
  - `at(h)`: this step happens at the same instant as `h`. Several threads doing
    `at(h)` form a barrier.
- **Step.** Anything that gets a timestamp: an endpoint or an event. Each thread's
  steps are totally ordered, which is its **program order**.
- **Trace poset `P`.** The steps, ordered by program order plus the sync edges. Each
  sync point is a virtual step `ĥ`: `before(h)` steps precede it, `after(h)` steps
  follow it, and `at(h)` steps are merged into it. `P` is a
  [partially ordered set](https://en.wikipedia.org/wiki/Partially_ordered_set).
- **Width** of `P`. The size of its largest set of pairwise unordered steps. Here it
  is at most `N + K`, because `P` is covered by `N` thread chains plus `K` virtual
  steps ([Dilworth's theorem](https://en.wikipedia.org/wiki/Dilworth%27s_theorem)).
  Many problems that are hard in general become polynomial when the width is fixed,
  by dynamic programming over *down-sets*: sets of steps closed under "earlier than"
  (a [lower set](https://en.wikipedia.org/wiki/Upper_set)).

### Orders and effects

- **Linearization `L`.** A total order of all steps that respects `P`: a
  [linear extension](https://en.wikipedia.org/wiki/Linear_extension) of `P`, or a
  [topological sort](https://en.wikipedia.org/wiki/Topological_sorting). Read it as
  timestamps.
  - **`Lin(P)`** is the set of all linearizations.
  - Counting `|Lin(P)|` is [#P](https://en.wikipedia.org/wiki/%E2%99%AFP)-complete for
    general posets (Brightwell–Winkler 1991), but polynomial for fixed width.
- **Interval.** Under `L`, an action `a` occupies the interval `I_L(a)` from its start
  to its end. Two actions are *concurrent* if their intervals overlap; otherwise one
  *precedes* the other. This precedence relation is an
  [interval order](https://en.wikipedia.org/wiki/Interval_order).
- **Effect point `π(a)`.** The instant inside `I_L(a)` at which the action takes
  effect; different actions get different instants. Each block behaves as an
  **atomic register**: a read returns the content written by the latest write whose
  effect point precedes the read's (or the initial content). This is the standard
  notion of [linearizability](https://en.wikipedia.org/wiki/Linearizability) for a
  single register.
- **Full schedule `(L, π)`.** A linearization plus effect points. There are two
  sources of nondeterminism: the interleaving `L` and the effect points `π` within it.
- **Reads-from.** In a full schedule, `rf(r)` is the write whose content read `r`
  returned, or "initial".

### Data

- **Term.** A block's content.
  - A term is a constant (`7`), the unknown initial content of block `b` (`init.b`),
    the unknown content of write `w` (the symbol `w`), or a pair `a~b`.
  - `~` is an ordered pair with no algebra: `a~b ≠ b~a`, and two terms are equal only
    if they are identical trees (a
    [term algebra](https://en.wikipedia.org/wiki/Term_algebra)).
- **Write data.** An expression over constants and the values returned by *earlier,
  completed* reads of the same thread. `w = r1~7` writes "what `r1` returned,
  paired with 7".
  - Because `r1` must have ended before `w` starts, read-dependent data never changes
    `Lin(P)`.
  - It does change which values are possible.

### Observations and possibility sets

- **Observation.** A read whose result is known.
- **Feasible.** A full schedule is feasible if, when executed, every observed read
  returns its observed value. `L` is feasible if some `π` makes `(L, π)` feasible.
  **`LinFeas(P)`** is the set of feasible linearizations.
- **`Poss(r)`.** The set of values read `r` returns across all feasible full
  schedules.
  - **`Poss_L(r)`** is the same with `L` fixed.
  - **`Poss(b)`** is the set of possible final contents of block `b`.
  - A solver must output these sets **exactly**, "no more, no less": every value it
    lists needs a feasible schedule as a witness, and every value that some feasible
    schedule produces must be listed.
- **Joint possibility `Poss(r₁, …, r_k)`.** The set of *tuples* `(v₁, …, v_k)` that
  the reads return *together*, in one feasible schedule. It is usually smaller than
  the product `Poss(r₁) × … × Poss(r_k)`.

  **Example.** Thread A writes 1, then (after that write ends) writes 2, to a block
  that starts at 0. Thread B reads it twice in sequence, `r₁` then `r₂`.
  - Individually `Poss(r₁) = Poss(r₂) = {0, 1, 2}`.
  - But `(r₁, r₂) = (2, 1)` is impossible, because the block's value only moves
    forward. The joint set has 6 of the 9 pairs.
- **CHECK.** Deciding whether any feasible schedule exists at all. This is
  linearizability checking of a register history, which is NP-complete in general
  (Gibbons–Korach 1997; [NP-completeness](https://en.wikipedia.org/wiki/NP-completeness)).

### The four cases

Every problem here comes in four cases: observations (none / some) × sync (no / yes).

| | no sync (`K = 0`) | sync |
|---|---|---|
| **base**: no observations; data constant or read-dependent | `b` | `s` |
| **observed**: some read results known | `o` | `so` |

RCW, weaker registers and torn writes are later extensions.

### Complexity and enumeration words

- **FPT.** Fixed-parameter tractable: polynomial once a parameter, such as the number
  of threads, is fixed
  ([parameterized complexity](https://en.wikipedia.org/wiki/Parameterized_complexity)).
- **CAT.** Constant amortized time per output of an enumeration.
- **[Gray code](https://en.wikipedia.org/wiki/Gray_code).** An enumeration in which
  consecutive outputs differ by a small, fixed kind of change (here, one or two
  adjacent swaps).

---

## 0. Guiding observations

1. **Width is our lever.** The trace poset has width ≤ N. Almost every "hard in general"
   problem here (counting, sampling, checking) is polynomial for fixed N by dynamic
   programming over the N-tuple of per-thread positions. Build that DP once and reuse it.
2. **Unique values buy tractability.** With `p_w = 1` and distinct terms, checking is
   `O(n log n)` (LinP). Hardness enters only through unknown or repeated contents.
   Generators should expose that dial explicitly.
3. **Two nondeterminism levels.** Keep step interleaving (`L`) and effect points (`π`)
   separate in code; several problems become easy at one level and hard at the other.
4. **Brute force first.** Every fast algorithm gets a slow, obviously-correct twin. The
   validator sub-project is the backbone, not an afterthought.

---

## 1. Generator (GEN)

### 1.1 Baseline random generator
- Seeded, parameterized by every hyperparameter in `premise.md` §3.
- Emits a canonical JSON/text setup; emits the *hidden* full schedule and hidden values
  used to produce observations (kept in a sidecar for validators).
- Shape controls: max in-flight actions per thread, read/write/RCW mix, block skew
  (Zipf), `K` and events per thread, relation mix (`before`/`after`/`at`), threads per sync point.

### 1.2 Targeted / adversarial generators
- **Hardness dials from the literature**: writers per block (1 / 2 / 3+), number of
  preemptions, fraction of repeated values, fraction of unknown writes. Lets us
  reproduce the known trichotomies experimentally.
- **Anomaly-seeking generation** (litmus-style): construct setups that contain a
  specific pattern (e.g. a write that can only be observed by exactly one linearization),
  to stress solvers.
- **Coverage-driven generation**: pick hyperparameters to maximize diversity of
  possibility-set sizes or of `|Lin(P)|`.

### 1.3 Realism layer
- Import real block traces (e.g. `blktrace` output) into our format, with unknown
  contents, to see how the solver behaves on real shapes.

Dependencies: shared format (§6). Validators: well-formedness, realizability.

---

## 2. Linearizer (LIN-*)

### 2.1 Reference implementations
- LIN-ENUM by Varol–Rotem backtracking (on the quotient poset, virtual steps included) (simple) and Pruesse–Ruskey Gray code (fast,
  constant amortized time).
- LIN-COUNT and exact uniform LIN-SAMPLE by DP over down-sets indexed by per-thread
  positions (`(n/N+1)^N` states). Also gives rank/unrank, hence *deterministic
  pseudo-random access* to the k-th linearization — handy for reproducible tests.

### 2.2 Scalable sampling
- Bubley–Dyer adjacent-transposition chain; Huber's bounding chain for perfect samples
  when N is large and the DP is too big.
- Experiments: mixing in practice vs. N, sync density; compare to exact DP on small cases.

### 2.3 Constrained linearization
- Sample or enumerate only linearizations that are *feasible* given observations
  (`p_r > 0`). Approaches: rejection (baseline), DP with pruning by a per-state feasibility
  check, SAT/SMT with random parity constraints (XOR-sampling) for near-uniformity.
- Open question we can attack: is uniform feasible-linearization sampling hard even
  for fixed N?

### 2.4 Enumeration modulo equivalence
- Enumerate one linearization per *reads-from class* (DPOR-style) instead of all of
  `Lin(P)`. This is what a solver really needs and can be exponentially smaller.

Dependencies: shared poset library (§6). Validators: VAL-LIN, VAL-ENUM, count
cross-checks (enumerator length = DP count = Monte-Carlo estimate within error).

---

## 3. Solver (SOLVE-*)

### 3.1 Brute-force oracle
- Enumerate `L`, then `π` (all effect orders consistent with intervals), then `θ` over a
  small finite domain; run the register semantics; collect values. Exponential but
  the ground truth for everything else.

### 3.2 Level-2 solver for a fixed `L`, constants only (polynomial)
For a fixed linearization and constant writes, `Poss_L(r)` under atomic semantics has a
direct characterization: write `w` on the same block is possible for read `r` iff
(a) `w` can precede `r` (`ts(start(w)) < ts(end(r))`) and (b) no other write `w'` to that
block is *forced strictly between* them (`ts(end(w)) < ts(start(w'))` and
`ts(end(w')) < ts(start(r))`); the initial value is possible iff no write is forced entirely
before `r`. This is `O(#writes on the block)` per read. First deliverable of the solver
track; prove it and differential-test it against §3.1.

*Status:* this was implemented as the `window` solver and matched §3.1 on every test.
It was removed once read-dependent data became part of the base problem, because the
characterization holds for constant data only.

### 3.3 Level-1+2 solver, constants only
- `Poss(r)` over all linearizations. Condition (b) above becomes a disjunction per
  competing write (`w'` placed before `w` **or** after `r`), i.e. a linear extension
  problem with disjunctive constraints. Study its complexity: conjecture polynomial for
  fixed N via the positions DP; find whether it is NP-hard for unbounded N.

### 3.4 Symbolic solver (terms, unknown writes)
- Represent block contents as terms; propagate possibility sets as sets of terms.
- Joint possibilities: because terms mention earlier reads, `Poss(r)` for a later read
  depends on what earlier reads returned in the *same* schedule. Represent the joint
  space as a set of reads-from assignments, or as an SMT problem (uninterpreted
  functions for terms; integer timestamps for `L` and `π`; per-read query "is value v
  possible?").
- Enumerating `Poss(r)` exactly via SMT: iterate "find a model with `val(r) ∉ found`"
  until unsat. Cost grows with `|Poss(r)|`, which is fine when sets are small.

### 3.5 Observation-driven inference (CHECK and beyond)
- With `p_r > 0`: prune schedules by observed reads; derive *forced* facts (a read that
  saw term `t` forces the write of `t` to precede it and every other write of the block to
  be outside the window). Non-commutative terms recover write order per block, like
  Elle's list-append; then the Gibbons–Korach `O(n log n)` "read-mapping + write-order"
  case applies.
- Infer unknown write contents from observed reads (`p_w < 1`): every unknown symbol
  that some observed read returns becomes known; propagate.
- Deliver a CHECK mode that reuses Porcupine-style backtracking as a cross-check.

### 3.6 Incremental / online solver (SOLVE-INC)
- Maintain possibility sets as steps and observations stream in. Invariants to enforce
  and test: adding an observation never enlarges any set; appending unconstrained steps
  never shrinks the sets of completed reads.
- Data structures: per-block interval structures keyed by timestamps; union-find over
  forced-order facts; incremental SAT for the symbolic case.
- Benchmark against re-solving from scratch.

### 3.7 Complexity study (theory track)
- Classify SOLVE variants by (fixed `L`?) × (constants / terms / unknowns) ×
  (fixed N?) × (RCW on/off) × (K = 0 / K > 0). Fill a table with P / NP-hard /
  #P-hard / FPT / open, with reductions from Gibbons–Korach and the 2026 writers-per-
  location trichotomy, and with algorithms from §3.2–3.4.

Dependencies: linearizer (for enumeration-based oracles), shared semantics module (§6),
optionally an SMT solver binding (Z3).

---

## 4. Validator (VAL-*)

- **VAL-LIN**: check timestamps respect `P`. Trivial, but the first test everyone runs.
- **VAL-ENUM**: enumerator output is a set (no duplicates), each element passes VAL-LIN,
  cardinality equals DP count; for Gray-code enumerators, consecutive outputs differ by
  the promised transpositions.
- **VAL-SOLVE (soundness)**: for every returned value, produce a *witness* full schedule
  and re-execute it; the solver should emit witnesses itself so this is cheap.
- **VAL-SOLVE (completeness)**: differential testing against the brute-force oracle on
  small instances; metamorphic tests on large ones (adding a sync edge can only shrink
  sets; renaming blocks/threads/sync points is a symmetry; reversing all program orders and swapping
  start/end endpoints maps the problem to a dual instance).
  *The dual-instance claim is unverified and probably false as stated.* With
  read-dependent data, reversal puts a write before the read it depends on. Even with
  constant data, a reversed read would see the *next* write rather than the previous
  one. See §10, problem X4.
- **Property-based fuzzing**: generator → solver → validator loop with shrinking of
  failing setups to minimal counterexamples.
- **Proof obligations**: keep a list of lemmas (e.g. the §3.2 characterization) with
  either a pen-and-paper proof or a mechanized one (Lean/Coq) as a stretch goal.

Dependencies: everything; the validator is the integration point.

---

## 5. Extensions beyond the draft

- **Crashes**: add crash steps; study strict vs. durable linearizability variants of
  `Poss`. Relevant to real block devices.
- **Weaker block semantics**: regular/safe registers, torn writes, per-queue ordering
  (NVMe submission queues) as an extra partial order.
- **Multi-block atomic ops**: scatter/gather, atomic write units spanning blocks.
- **Probabilistic view**: instead of sets, compute the *distribution* of read values
  under uniform linearizations — directly uses LIN-COUNT/LIN-SAMPLE.
- **Visualizer**: draw threads as lanes, ops as intervals, possibility sets as labels;
  Porcupine's history visualization is a model.
- **Learning-based heuristics**: train a model to guess linearization points to speed
  up backtracking (order of trying minimal actions), validated by the oracle.

---

## 6. Shared infrastructure (do this first)

- **Setup / trace format**: specified in `formats.md` (YAML with a JSON data model):
  `setup`, `linearization`, `schedule`, `outcomes`, `count`, `trace`, `report`,
  `hyperparams`. Versioned; instances can be hand-written in tests.
- **Core library** (one language for the reference implementation; suggestion:
  Python for speed of iteration, with a Rust or C++ port of hot paths later):
  poset construction and transitive closure, chain decomposition, positions-DP,
  interval utilities, register semantics interpreter (atomic / regular / safe / RCW),
  term algebra, witness objects.
- **CLI**: `gen`, `lin count|enum|sample`, `solve`, `check`, `validate`, each reading
  and writing the shared format, so sub-projects can be developed and tested
  independently and composed by pipes.
- **Benchmark corpus**: generated instances at fixed seeds, spanning the hardness dials,
  with oracle answers stored for small ones.
- **Test harness**: property-based tests over the corpus; CI runs the differential
  suite.

---

## 7. Suggested decomposition into sub-projects

| Sub-project | Owner-able alone? | Depends on | First milestone |
|---|---|---|---|
| S0 Format + core library + CLI skeleton | yes | — | schema v1, poset + DP count, semantics interpreter, brute-force oracle |
| S1 Generator | yes | S0 | seeded random generator with hardness dials; realizability check |
| S2 Linearizer | yes | S0 | Pruesse–Ruskey enumerator; DP exact sampler; Bubley–Dyer sampler; count cross-checks |
| S3 Solver (constants) | yes | S0, S2 for oracles | §3.2 characterization proved + implemented + differentially tested |
| S4 Solver (symbolic / observations) | joint with S3 | S3 | SMT-backed `Poss` with witnesses; CHECK mode |
| S5 Online solver | joint with S3/S4 | S3 | incremental sets with monotonicity tests |
| S6 Validator + fuzzing | yes | S0..S5 | metamorphic suite; shrinking; CI |
| S7 Theory | yes | reading only | complexity table (§3.7); at least one new result (e.g. fixed-N tractability of §3.3, or hardness with unknowns) |

Phasing: S0 → {S1, S2, S7} in parallel → S3 → {S4, S5, S6} in parallel → extensions (§5).

---

## 8. Research questions we would like to answer

- RQ1. Is `Poss(r)` for a single read with constant writes computable in polynomial time
  when `L` ranges over all linearizations? For fixed N? In general?
- RQ2. How does the size of `Poss(r)` scale with in-flight depth, N, M, K, and sync density?
  Is there a phase transition (most reads determined vs. most reads wide open)?
- RQ3. With non-commutative terms and `p_w = 1`, does CHECK become `O(n log n)` in our
  asynchronous-thread model as it does for sequential threads (LinP)?
- RQ4. What is the smallest `p_r` that typically pins down the linearization (or the
  reads-from relation) uniquely? How does it depend on the term class?
- RQ5. Can the online solver achieve amortized polylog work per step for constants?
- RQ6. Does the writers-per-block trichotomy (1 / 2 / 3+) survive the move from
  sequential threads to asynchronous I/O and to RCW?
- RQ7. How well do MCMC samplers mix on trace posets with dense sync edges, compared
  with the exact positions-DP? Do `at` barriers (which cut the poset) help mixing?

---

## 9. Risks and mitigations

- **Definition drift** between sub-projects → freeze `premise.md` §2 and §6 before S1.
- **Oracle too slow to validate interesting sizes** → enumerate modulo reads-from
  equivalence (§2.4) and use the DP to bound state space; cache oracle results in the corpus.
- **Symbolic solver blow-up** → restrict term depth in early phases; use witnesses to
  short-circuit.
- **Over-scoping** → each sub-project must ship its brute-force twin and validator tests
  before optimizing.

---

## 10. Problems for model testing (extrapolation)

The second purpose of this study is to find which problems AI code-generation models
fail. Problems that are textbook material only test recall. So this section collects
problems that, as far as our survey found, the literature does not answer. A model has
to derive something new, and we can still grade the result mechanically.

**Protocol.** The rules are in the root `AGENTS.md` ("Model tests"):
- a spec-only prompt, with no algorithm names or hints;
- one isolated directory per model and trial;
- a declared closed-book or open-book condition, and a `SOURCES.md` log of searches and
  of where each idea came from;
- grading by the orchestrator against the brute-force oracle.

**What rounds 1–4 showed** (`python/attempts/_archive/round1_4/REPORT.md`):
- **Every implementation passed every independent check**, including the new
  feasibility theory in the observed case.
- **The prompts named candidate algorithms**, so those rounds measured
  guided implementation.
- **To expose failures, a problem needs at least one of these:**
  - a *trap*: a natural lemma that is false in this setting;
  - a need for a *compact representation* or output-sensitive cost;
  - a *claim that must be proved or refuted*, rather than just tested.

**Grading.**
- Anything with an exact answer is checked against `brute` (`python/harness/solve/brute.py`)
  on small instances, and against `backtrack-feasible` for linearizations.
- Theory answers must come with a mechanical artefact, such as a reduction implemented
  as an instance generator, or a counterexample setup, so that they too can be checked
  by the oracle.

Items marked *(verify)* may have prior work that our survey missed.

### X1. Exact solvers

| # | Problem | Why it is off the map | Known trap |
|---|---|---|---|
| X1.1 | Compute `Poss(r)` for every read, over all of `Lin(P)`, in case `b` with **constant** data. Polynomial for fixed `N`? (RQ1) | The literature decides linearizability (yes/no). It does not compute exact value sets over all interleavings | The union over `L` of `Poss_L(r)` is correct but exponential. Shortcuts that reason "per competing write" miss combinations that are only jointly possible |
| X1.2 | The same in case `b` with **read-dependent** data | Values are terms; sets can be exponentially large, so an output-sensitive algorithm needs a shared or DAG representation of terms | Listing sets explicitly; missing a value that only a specific combination of earlier reads produces |
| X1.3 | Compute the joint set `Poss(r₁, r₂)` exactly | We know of no work on exact joint possibility sets | Returning `Poss(r₁) × Poss(r₂)`, which the example in "Terms" shows is wrong |
| X1.4 | Compute `Poss(r)` and `Poss(b)` in case `o` | Needs feasibility of every candidate value against all observations, across blocks | Handling blocks separately. With read-dependent data, a read on one block determines a write on another |
| X1.5 | All of the above in cases `s` and `so` | Sync plus data flow has not been treated | See X2.1 |

### X2. Linearizations under observations

| # | Problem | Why it is off the map | Known trap |
|---|---|---|---|
| X2.1 | Enumerate `LinFeas(P)` in case `so` (observations and sync) | The one case with no model-written code yet | **Barrier splitting.** An `at` barrier that every thread passes splits `Lin(P)` into a product of the segments before and after it. It does *not* split `LinFeas(P)`, because values written before the barrier are read after it. Reusing a segment-product enumerator is natural and wrong |
| X2.2 | Sample uniformly from `LinFeas(P)` without rejection | Listed as open in `surveys.md` §7.2 | Samplers that are nearly uniform, or uniform over `Lin(P)`. Grade with exact counts and a statistical test on small instances |
| X2.3 | Count `|LinFeas(P)|` in time polynomial for a fixed number of threads, independent of how many actions are in flight at once | Known FPT results for register checking assume each thread runs one operation at a time *(verify)* | State spaces that grow with the number of in-flight actions |
| X2.4 | Enumerate one `L` per distinct reads-from assignment `rf` (one representative per outcome class) | Related to partial-order reduction for programs, not to traces with free-term data | Emitting two representatives of one class, or merging classes that differ only in a nested term |
| X2.5 | Count the linear extensions of an interval order (the action order within one thread under `L`) | `surveys.md` §7.2: "no definitive result found" *(verify)* | Citing a complexity result that does not exist |

### X3. New semantics

A model must extend the definitions consistently before building on them.

| # | Problem | Why it is off the map | Known trap |
|---|---|---|---|
| X3.1 | Add RCW (compare-and-write; the result is the old content) to CHECK and to X2.1 | Tractable fragments are unclear (`surveys.md` §7.2); whether an RCW succeeds depends on a value, so data flows back into the block | Treating a failed RCW as a plain read, or ignoring that the returned old content hides whether it succeeded |
| X3.2 | Replace the atomic register by a *regular* register: a read that overlaps writes may return any of them, or the last value before them. Then compute `Poss` | Exact possibility sets under weaker registers are barely studied | Reusing the atomic-register fact that admissible effect orders are exactly the extensions of the interval order. It does not apply |
| X3.3 | Allow equal effect points for different actions (`premise.md` §6, open decision 4) | Changes the interval-order argument, because ties become possible | Keeping the strict order silently |
| X3.4 | Torn writes: a block is a tuple of sectors, and a write's sectors take effect separately | "A term equals at most one candidate value" no longer holds | Whole-block reasoning |

### X4. Claims to prove or refute

| # | Problem | How it is graded |
|---|---|---|
| X4.1 | Decide the complexity of `Poss(r)` for a single read, over all of `Lin(P)`: NP-hard in general? polynomial for fixed `N`? | A hardness claim must come with the reduction implemented as a generator; the oracle checks its instances on small sizes. A tractability claim must come with an implementation that is checked against the oracle |
| X4.2 | The "dual instance" claim of §4 (reverse program order, swap start and end endpoints) | Probably false as stated (see §4). The model should state the claim precisely, then prove it or produce a counterexample setup. This also tests whether a model goes along with a claim it was given |
| X4.3 | Find the smallest set of reads whose observation determines `rf` uniquely (RQ4) | Exact optimum by brute force on small instances; the model must also justify its complexity claim |
| X4.4 | Given an algorithm with a planted bug, find the smallest setup on which it gives a wrong answer | Tests search and adversarial thinking rather than construction. The planted bug is known, so grading is exact |
| X4.5 | Maintain `Poss` online, with steps and observations arriving one at a time, in amortized polylogarithmic time per step (RQ5) | Differential test against re-solving from scratch, plus the monotonicity rules in `premise.md` §4 (SOLVE-INC) |

### X5. Beyond enumeration

In these problems, "enumerate everything and check" either cannot state the answer or
gives the wrong one. So a model cannot fall back on brute force, and the harness needs
a new kind of oracle before it can grade them.

**X5.1. Interpreted unknown contents.** Today an unknown write (`data: "*"`) is a free
symbol: its content is the term `w`, which equals only itself, so it never collides with
another value. The original model (`premise.md` §2.6, and open decisions 5 and 6 in §6)
also has an **assignment `θ`**, which gives every unknown an actual value from a domain.
- A full schedule becomes `(L, π, θ)`.
- An unknown can then *equal* a constant or another unknown, and an observed read can
  pin an unknown down.
- With an interpreted algebra (e.g. integers with `+`, so `1+2 = 2+1`), different
  histories can produce the same value.

The task is to compute `Poss(r)` when `θ` ranges over an infinite domain. The answer
is then an infinite set and must be described **symbolically**, e.g. as a finite union
of terms with constraints on the unknowns ("`u + 3`, for every `u ≠ 5`").
- *Why brute force fails:* it cannot enumerate `θ`, or even write the answer down.
- *Grading:* checking the description needs a decision procedure, for example an SMT
  solver, or a restricted term class whose answers are provably finite.
- *Trap:* treating unknowns as free symbols, which is the current, weaker semantics.
  That misses the values where an unknown happens to coincide with another.

**X5.2. Parametric traces (loops).** A thread's program may contain a loop, "repeat
these steps `n` times", where the parameter `n` is left open. Task: give the answer as a
**function of `n`**, e.g. a closed form for `|Lin(P)|(n)` or `|LinFeas(P)|(n)`, or a
description of `Poss(r)` valid for all `n`.
- *Why brute force fails:* it yields only data points for small `n`; the model has to
  generalize.
- *Grading:* compare the formula with brute-force values at small `n`, then at larger
  `n` with the fast algorithms. A formula that only fits the samples it was built from
  is caught by the larger values.
- *Trap:* extrapolating a pattern from small cases that breaks later, e.g. at the point
  where observations or sync points start to interact across iterations.

**X5.3. Distributions (later).** Draw a linearization uniformly from `LinFeas(P)`, then
effect points by a stated rule, e.g. uniformly among the admissible effect orders. Task:
give the **exact probability** of each value in `Poss(r)`, as a rational number.
- *Why brute force fails:* it works only for small cases. Exact answers at scale need
  counting (weighted DP over the same states the solvers use), not sampling.
- *Grading:* compare exact rationals on small cases, and check sampling agreement at
  scale.
- *Status:* recorded for later. The probability model needs choices of its own (which
  distribution over effect points, and whether observations condition it) before it
  can be a task.

### Which problems a brute-force attempt could pass

The harness oracles enumerate linearizations and effect orders. So does the laziest
possible attempt. This decides what the correctness tests can show.

| Group | Problems | What grading must rely on |
|---|---|---|
| **Brute force is correct, only slow** | X1.1–X1.5, X2.1, X2.4, X2.5, X3.1, X3.3 | A lazy attempt passes every small instance, so the **scaling suite** is the real grade. Use adversarial ladders: many writers per block, repeated values, long data chains |
| **Brute force is correct but ruled out by the input size or the requirement** | X2.2 (whole list needed for uniform choice), X2.3 (counts too large to enumerate), X4.5 (re-solving breaks the per-step bound) | Required sizes or time bounds that enumeration cannot meet, e.g. count a 10¹² setup in 5 s |
| **Brute force gives the wrong answer, or no answer** | X3.2 (regular and safe registers are not effect-point models), X3.4 (torn writes), X4.1 (proofs), X5.1, X5.2, X5.3 | New oracles, derived and validated in the harness first; then exact checks on small cases plus symbolic or formula checks |
| **Brute force helps the model** | X4.2, X4.3, X4.4 | Searching small setups is a legitimate method here; grade the artefact (counterexample, minimal set, failing setup) |

### Suggested order

1. **Done in round 5 (bundle v1):** X2.1 and the exact solvers X1.1, X1.2 and X1.4 in all
   four cases. Every attempt passed, and none enumerates and filters. See
   `python/attempts/README.md`.
2. **X1.1 and X1.2 with adversarial scaling ladders:** no new API; tests whether a
   model finds something better than exponential search.
3. **X3.2 (regular registers), X5.2 (loops) and X5.1 (interpreted unknowns):** the
   natural approach is wrong or cannot state the answer. Each needs a new harness
   oracle first.
4. **X1.3 (joint possibility):** a small new API with a known trap.
5. **X4.2 (the dual-instance claim):** tests whether a model checks a claim or
   accepts it.
6. **X3.1 (RCW):** the semantics already exist.
7. **X5.3 (distributions):** later.
