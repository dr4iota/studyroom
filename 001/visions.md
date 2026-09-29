# Visions: What We Could Build and Study

Status: v0.1, 2026-09-28. Companion to `premise.md` (definitions) and `surveys.md`
(literature). This is a menu, not a plan: each item is a candidate sub-project with its
inputs, outputs, dependencies, and the questions it would answer. §7 proposes how to
cut the menu into separately-owned pieces with shared code.

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
