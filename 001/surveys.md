# Survey: State of the Art Around Our Problem Class

Status: v0.1, 2026-09-28. Compiled from the literature listed in §9; claims marked
"(unverified)" were not checked against the primary source and should be confirmed
before being relied on.

Our class (see `premise.md`) sits at the intersection of four established areas:

| Our sub-problem | Established problem | Key words |
|---|---|---|
| LIN-ENUM / LIN-SAMPLE / LIN-COUNT | linear extensions of a poset | #P-completeness, Markov chains, Gray codes, width parameterization |
| CHECK, SOLVE with observations | linearizability / sequential-consistency checking of read-write histories | Gibbons–Korach, Wing–Gong, Porcupine, Knossos, LinP |
| SOLVE (prediction of read values, no observations) | predictive trace analysis, maximal causal models, reads-from equivalence | Huang–Meredith–Roșu, Pavlogiannis et al. |
| Content model (terms over prior reads, partial knowledge) | isolation/consistency inference from client observations | Elle, Cobra, Viper, PolySI, Vbox, Biswas–Enea |

---

## 1. Consistency and linearizability checking of histories

### 1.1 Foundations
- **Lamport 1986** defined *safe / regular / atomic* registers; our default block semantics
  is the atomic register, and regular/safe are the natural weaker alternatives.
- **Herlihy & Wing 1990** defined linearizability; the "effect point inside the interval"
  view in `premise.md` §2.4 is exactly theirs.
- **Wing & Gong 1993** gave the classic backtracking checker (try each minimal
  operation, simulate, recurse). Most practical checkers are refinements of it.

### 1.2 Complexity (the core hardness results)
- **Gibbons & Korach 1997, "Testing shared memories"**: verifying sequential consistency
  (VSC) and verifying linearizability (VL) of read/write histories are **NP-complete**,
  and VSC stays NP-complete even with only two operations per processor, only two
  locations, or only three processors. Knowing the *read-mapping* (which write each read
  observed) alone does not help (VSC-read is still NP-complete), but knowing read-mapping
  **and** the per-location write order (the "conflict order") makes it **O(n log n)**.
  This is directly our CHECK problem: our "non-commutative terms" content model is a
  way of making the read-mapping and, partly, the write order recoverable from values.
- **Cantin, Lipasti & Smith 2005**: verifying memory coherence is NP-complete too.
- **Bouajjani, Enea, Guerraoui & Hamza, POPL 2017**: checking *causal consistency* of a
  single history is NP-complete in general, but polynomial for *data-independent*
  read-write memory (each value written at most once). Verifying all executions of an
  implementation is undecidable.
- **Biswas & Enea, OOPSLA 2019**: for transactional histories, read committed / read
  atomic / causal consistency are polynomial; prefix consistency and snapshot isolation
  are NP-complete; serializability was already known NP-complete (Papadimitriou 1979).
  For the NP-complete ones they give algorithms polynomial when the **number of sessions
  is fixed** — the same "width ≤ N" lever we have.
- **Govind, Krishna, Sil & Srivathsan, FM 2026**: consistency testing for release-acquire
  is polynomial when each location is written by at most one thread, NP-hard with two
  writers per location, and (under ETH) has no `2^{o(k)}·poly(n)` algorithm with three
  writers, `k` = threads. Their companion paper **"Verifying SC under bounded
  preemptions" (2026)** shows the same single/two/three-writer trichotomy for SC and
  that SC checking is **W[1]-hard in the number of preemptions**. These "writers per
  block" and "preemptions" parameters are natural generator knobs for us.
- **Lee & Mathur, "Fixed Parameter Tractable Linearizability Monitoring" (POPL 2026)**:
  linearizability monitoring for stacks, queues and "anagram-agnostic" types is FPT in
  the number of processes, `O(c^k · poly(n))`, via reduction to language reachability on
  graphs. Registers are the simplest case of the same phenomenon.
- **Mathur, Pavlogiannis & Viswanathan, LICS 2020**: dynamic data-race *prediction* is
  intractable in general (NP-hard; W[1]-hard in natural parameters) and they identify
  tractable fragments. Race prediction is a "does some linearization exhibit X"
  question, structurally the same as our SOLVE.

### 1.3 Tractable fragments and fast checkers (hard but solved in practice)
- **Horn & Kroening 2015, P-compositionality**: split a history by independent keys
  (blocks) and check each part separately. Our per-block decomposition is exactly this,
  *except* that terms over prior reads re-couple blocks.
- **Lowe 2017, "Testing for linearizability"**: just-in-time linearization and
  competition between algorithms; a good reference for practical backtracking.
- **Porcupine (Athalye)**: Go checker, Wing–Gong plus P-compositionality plus
  memoization; 1,000–10,000× faster than Knossos on typical histories.
- **Knossos / Jepsen (Kingsbury)**: Clojure checkers; Jepsen is the standard harness for
  black-box consistency testing of distributed stores.
- **Lincheck (JetBrains)**: model-checking-based linearizability testing for JVM data
  structures; includes random scenario generation, relevant to our GEN.
- **Emmi & Enea 2018, "Sound, complete and tractable linearizability checking"**
  (unverified details): polynomial monitoring for collections under restrictions.
- **Mathur et al., "Efficient Decrease-and-Conquer Linearizability Monitoring"
  (OOPSLA 2025, tool LinP)**: under the *unambiguity* restriction (each written value is
  distinct), registers, sets, stacks, queues and priority queues admit **log-linear
  time** monitors, scaling to million-operation histories. **This is the single most
  relevant recent result**: our "constants + unique term" content model makes writes
  unambiguous by construction, so CHECK becomes `O(n log n)` for us whenever `p_w = 1`
  and terms are distinct.
- **Raghav et al. 2026, generalized Wing–Gong for non-transactional storage systems**:
  extends the classic algorithm with system-specific ordering constraints (e.g.
  ZooKeeper's ordered SC), reports up to 370× speedups; shows that adding *ordering
  constraints* (our sync points and events) is a practical dimension.
- **OmniLink 2026**: trace validation of unmodified concurrent systems; reports that
  Porcupine degrades past ~200k operations with few threads — a datapoint for scaling.

### 1.4 Transactional checkers (methods transferable to us)
- **Cobra (OSDI 2020)**: serializability checking as SAT over "polygraphs", with
  GPU-accelerated pruning. **Viper (EuroSys 2023)**: BC-polygraphs for snapshot
  isolation. **PolySI**: SMT with compact encodings. **Vbox (2025)**: uses transaction
  *time information* (our intervals) and a simplified SAT formulation, 60–100× faster
  than Cobra at 10K transactions. **Online timestamp-based isolation checking (2025)**
  — an incremental checker; relevant to SOLVE-INC.
- **Elle (VLDB 2021)**: infers Adya-style dependency graphs from client observations.
  Its key trick — use *list-append* so that each read reveals the full version history —
  is the same idea as our non-commutative terms. Elle "can make limited inferences from
  read-write registers but shines with richer datatypes". A 2026 extension handles
  workloads with duplicate values (our `p_w < 1` / non-unique constants case).

---

## 2. Predictive analysis: "what could a read have returned?"

- **Maximal causal models (Șerbănuță, Chen & Roșu 2012; Huang, Meredith & Roșu, PLDI
  2014)**: from one observed trace, the set of feasible reorderings is exactly those
  where every read that *influences control flow* sees the same write as observed; reads
  that do not influence anything may change their writer. This is the semantics behind
  our "write content is a function of earlier reads": a reordering that changes a read's
  value changes every downstream write term.
- **Said, Wang, Yang & Sakallah 2011**: SMT encodings for data-race witnesses with
  data constraints. **Reads-from equivalence (Pavlogiannis et al., OOPSLA 2021)** and
  **"Parametrizing Reads-From Equivalence for Predictive Monitoring" (2026)**: treat
  two schedules as equivalent if every read reads from the same write; our
  `Poss(r)` is a projection of the reads-from space.
- **"Soundness of Predictive Concurrency Analyses" (OOPSLA 2025)** and **"Predictive
  Monitoring with Strong Trace Prefixes" (CAV 2024)**: formal soundness criteria for
  prediction; useful for defining what our validators must certify.
- **Stateless model checking / DPOR** (Flanagan–Godefroid 2005; optimal DPOR, Abdulla et
  al. 2014; GenMC; Nidhugg): enumerate one representative per reads-from (or
  Mazurkiewicz) equivalence class. LIN-ENUM modulo an equivalence is the practical
  version of "enumerate all linearizations". **DPOR for transaction isolation levels
  (2023)** shows the technique transfers to storage-style semantics.

---

## 3. Linear extensions: counting, sampling, enumeration

### 3.1 Hardness
- **Brightwell & Winkler 1991**: counting linear extensions is **#P-complete**.
- **Dittmer & Pak 2020**: still #P-complete for posets of **height 2** and of
  **dimension 2**; the parity version is ⊕P-complete for dimension 2.
- **Felsner et al.**: #P-complete for N-free posets of height 3; conjectured for all
  N-free posets.
- **Interval orders**: we did not find a definitive statement in the sources consulted;
  treat as an open question *for us* (our level-1 poset is not an interval order, but
  the level-2 action order under a fixed `L` is).

### 3.2 Exact algorithms
- DP over down-sets (order ideals) gives `O*(2^n)` in general and is the workhorse for
  small instances; **De Loof et al.** and **Kangas et al. 2016** exploit sparsity.
- **"Breaking the 2^n barrier" (ALGOWIN 2026)**: first `O*(1.89^n)` exact algorithm for
  arbitrary posets, resolving Koivisto's 2013 question.
- **Width parameterization (folklore)**: for a poset covered by `N` chains, the number of
  down-sets is at most `∏(len_i + 1) ≤ (n/N + 1)^N`, so counting, uniform sampling, and
  ranking/unranking are all **polynomial for fixed N** by DP over the `N`-tuple of
  per-chain positions. For our trace poset (`N` thread chains plus sync edges) this DP
  is the natural exact linearizer; `N` is small in most of our setups.
- **Series-parallel / N-free / modular posets** have product formulas or fast DPs
  (e.g. "Counting linear extensions of modular partial orders", 2024).

### 3.3 Sampling and approximate counting
- **Karzanov & Khachiyan 1991**: adjacent-transposition Markov chain, rapidly mixing.
- **Bubley & Dyer 1999**: modified chain with `O(n^3 log n)` mixing via path coupling;
  known to be `Θ(n^3 log n)` for the KK chain.
- **Huber 2006**: bounding chain enabling *perfect* (exact uniform) sampling.
- **TPA and "Approximate counting of linear extensions in practice" (JAIR)**: telescopic
  product estimators and comparisons of MCMC vs. exponential Monte Carlo (AAAI).
- "Combinatorial Markov chains on linear extensions" (Ayyer, Klee, Schilling 2014) —
  promotion-based chains with exactly known spectra on some poset classes.

### 3.4 Enumeration
- **Varol & Rotem 1981**: simple backtracking enumeration.
- **Pruesse & Ruskey 1994**: Gray code enumeration, **constant amortized time**, each
  successive extension differs by one or two adjacent transpositions.
- **Ono & Nakano 2005**: constant-time-per-extension without the Gray-code property
  (unverified details). Any of these is a fine reference LIN-ENUM.

### 3.5 Inverse problem
- **"De-Linearizing Agent Traces: Bayesian Inference of Latent Partial Orders" (2026)**:
  infer the partial order from observed linearizations — the mirror image of our
  observation-constrained sampling (LIN-SAMPLE variant c).

---

## 4. Generation of concurrent test setups

- **diy7 / litmus7 / herd7** (Alglave, Maranget): systematic generation of litmus tests
  by enumerating cycles of relaxed-memory relations; the "generate the shape that
  exhibits a target anomaly" philosophy is directly reusable for targeted GEN.
- **Jepsen generators** and **Lincheck scenario generation**: randomized, seeded,
  parameterized by threads, keys, op mix.
- **Elle's list-append workload**: chosen specifically so observations reveal history;
  our term model plays the same role.
- Generator knobs suggested by the hardness results: writers per block (1/2/3+),
  number of preemptions, fraction of unique values, `K` and event density.

---

## 5. Storage-specific semantics

- **Compare-and-write**: NVMe *Compare and Write* (fused command) and SCSI
  `COMPARE AND WRITE` are the real-world RCW; both are atomic against other commands to
  the same LBA range. Our RCW should mirror "compare, then conditionally write, return
  status" semantics.
- **Torn writes / atomic write units**: real devices guarantee atomicity only per
  sector or per declared atomic write unit; a "torn write" model would make a block a
  vector of sub-registers.
- **Crash semantics**: *strict linearizability* (Aguilera & Frølund 2003): an operation
  interrupted by a crash takes effect before the crash or not at all; *durable
  linearizability* (Izraelevitz, Mendes & Scott 2016): every completed operation is
  persisted before the next crash; "The Path to Durable Linearizability" (POPL 2023).
  Crash-consistency test tools (ALICE, CrashMonkey) are the systems-side analogue. Crash
  steps are an obvious future extension of our step alphabet.
- **Consistency checking for non-transactional distributed storage** (Raghav et al.
  2026): shows demand for checkers that accept extra ordering constraints and that the
  Wing–Gong core still dominates practice.

---

## 6. Where our class differs from everything above

1. **Asynchronous per-thread I/O**: overlapping actions inside one thread. Most
   linearizability checkers assume each thread's operations are sequential; the
   register-history hardness results (Gibbons–Korach) also assume that. Our level-1
   poset is therefore a *chain of steps* (endpoints and events), not a chain of actions, and the induced
   action order within a thread is itself an interval order.
2. **Two nondeterminism levels** (`L` and `π`) treated separately; the literature usually
   collapses them into "choose linearization points".
3. **Exact possibility sets** ("no more, no less") rather than a yes/no verdict. The
   closest notions are reads-from equivalence classes and maximal causal models.
4. **Partial knowledge of both writes and reads** as first-class parameters (`p_w`,
   `p_r`), spanning pure prediction to full checking.
5. **Symbolic non-commutative terms** as content: generalizes Elle's list-append to
   arbitrary dataflow.

---

## 7. Summary tables

### 7.1 Hard but solved (results we can use as-is)
| Problem | Hardness | Practical solution |
|---|---|---|
| CHECK (registers, all values known) | NP-complete | Wing–Gong + P-compositionality (Porcupine); `O(n log n)` if values unique (LinP); FPT in threads |
| LIN-COUNT / uniform LIN-SAMPLE | #P-complete | DP over down-sets (poly for fixed `N`); Bubley–Dyer chain; Huber perfect sampling |
| LIN-ENUM | output exponential | Pruesse–Ruskey CAT Gray code |
| Serializability / SI checking | NP-complete | SAT/SMT + pruning (Cobra, Viper, PolySI, Vbox) |
| Race prediction | NP-hard / W[1]-hard | sound-but-incomplete partial orders (SHB, WCP, SyncP) |
| Version-order recovery | impossible for plain registers | list-append / unique-term encodings (Elle) |

### 7.2 Open (in the literature, or at least unresolved for our setting)
| Question | Status |
|---|---|
| Counting linear extensions of interval orders | no definitive result found by us |
| Exact complexity of `Poss(r)` for a *single* read when `L` is not fixed and writes are constants | unknown to us; likely tractable for fixed `N`, plausibly hard in general |
| Complexity of CHECK / SOLVE with `p_w < 1` (unknown write contents) | not treated directly; related to non-unique-value hardness |
| Complexity of CHECK with RCW actions | CAS histories: hardness inherits from registers; tractable fragments unclear |
| FPT in number of threads for registers with *asynchronous* per-thread I/O | not treated; Lee–Mathur's FPT results assume sequential threads |
| Uniform sampling of linearizations *conditioned on observations* | no dedicated algorithm found; general constrained sampling is hard |
| Optimal incremental (online) possibility-set maintenance | only isolation-level online checkers found (2025) |

---

## 8. Reading order suggestion
1. Gibbons & Korach 1997 (§1.2) — the hardness baseline.
2. Mathur et al. 2025 (LinP) and Lee & Mathur 2026 — modern tractable fragments.
3. Elle 2021 — content encoding that reveals history.
4. Pruesse & Ruskey 1994; Bubley & Dyer 1999; the 2026 `1.89^n` paper — linearizer toolbox.
5. Huang, Meredith & Roșu 2014 — sound prediction with data dependence.
6. Govind et al. FM 2026 — the writers-per-location trichotomy.

---

## 9. Sources
- Gibbons & Korach, Testing Shared Memories: https://www.researchgate.net/publication/2506687_Testing_Shared_Memories
- Cantin, Lipasti, Smith, complexity of verifying memory coherence: https://www.researchgate.net/publication/3300954_The_complexity_of_verifying_memory_coherence_and_consistency
- Bouajjani, Enea, Guerraoui, Hamza, On Verifying Causal Consistency (POPL 2017): https://www.lix.polytechnique.fr/~cenea/papers/popl2017.pdf
- Biswas & Enea, On the Complexity of Checking Transactional Consistency (OOPSLA 2019): https://arxiv.org/pdf/1908.04509
- Govind, Krishna, Sil, Srivathsan, Complexity of Consistency Testing for Release-Acquire (FM 2026): https://arxiv.org/abs/2604.09589
- Govind et al., Verifying Sequential Consistency under Bounded Preemptions (2026): https://arxiv.org/pdf/2605.10625
- Lee & Mathur, Fixed Parameter Tractable Linearizability Monitoring: https://arxiv.org/pdf/2509.05586
- Mathur et al., Efficient Decrease-and-Conquer Linearizability Monitoring (OOPSLA 2025): https://arxiv.org/abs/2410.04581
- Mathur, Pavlogiannis, Viswanathan, The Complexity of Dynamic Data Race Prediction (LICS 2020): https://arxiv.org/abs/2004.14931v2
- Horn & Kroening linearizability checker: https://github.com/ahorn/linearizability-checker
- Porcupine: https://github.com/anishathalye/porcupine
- Verifying linearizability: a comparative survey: https://arxiv.org/pdf/1410.6268
- Raghav et al., Generalizing and accelerating consistency checking for non-transactional distributed storage (2026): https://arxiv.org/pdf/2608.17388
- OmniLink trace validation (2026): https://arxiv.org/pdf/2601.11836
- Cobra (OSDI 2020): https://www.usenix.org/conference/osdi20/presentation/tan
- Viper (EuroSys 2023): https://dl.acm.org/doi/10.1145/3552326.3567492
- PolySI: https://arxiv.org/abs/2301.07313
- Vbox (2025): https://arxiv.org/html/2503.05163
- Online timestamp-based isolation checking (2025): https://arxiv.org/pdf/2504.01477
- Elle (VLDB 2021): http://www.vldb.org/pvldb/vol14/p268-alvaro.pdf ; extension with duplicate values (2026): https://arxiv.org/html/2607.17515
- Huang, Meredith, Roșu, maximal sound predictive race detection (PLDI 2014) via: https://en.wikipedia.org/wiki/Runtime_predictive_analysis
- Soundness of Predictive Concurrency Analyses (OOPSLA 2025): https://web.cs.ucla.edu/~palsberg/paper/oopsla25.pdf
- Predictive Monitoring with Strong Trace Prefixes (CAV 2024): https://dl.acm.org/doi/10.1007/978-3-031-65630-9_9
- Parametrizing Reads-From Equivalence for Predictive Monitoring (2026): https://arxiv.org/pdf/2604.06533
- Reads-From Equivalence for TSO and PSO (OOPSLA 2021): https://cs.au.dk/~pavlogiannis/publications/papers/oopsla21.pdf
- DPOR for transaction isolation levels (2023): https://arxiv.org/pdf/2303.12606
- Brightwell & Winkler, Counting Linear Extensions is #P-complete: https://dl.acm.org/doi/10.1145/103418.103441
- Dittmer & Pak, Counting linear extensions of restricted posets: https://arxiv.org/abs/1802.06312
- Felsner et al., Linear Extensions of N-free Orders: https://arxiv.org/pdf/1311.1612
- Breaking the 2^n Barrier for Counting Linear Extensions (ALGOWIN 2026): https://arxiv.org/abs/2608.19505
- Survey: Linear extensions of finite posets (2023): https://arxiv.org/pdf/2311.02743
- Approximate Counting of Linear Extensions in Practice (JAIR): https://www.jair.org/index.php/jair/article/download/16374/27100
- Counting Linear Extensions in Practice: MCMC vs Exponential Monte Carlo (AAAI): https://ojs.aaai.org/index.php/AAAI/article/view/11528
- Huber, Fast perfect sampling from linear extensions: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=823316de43154bf2d2c02edc5262f97197b76020
- Ayyer, Klee, Schilling, Combinatorial Markov chains on linear extensions: https://arxiv.org/pdf/1205.7074
- Using TPA to count linear extensions: https://arxiv.org/pdf/1010.4981
- De-Linearizing Agent Traces (2026): https://arxiv.org/pdf/2602.02806
- Izraelevitz, Mendes, Scott, durable linearizability: https://link.springer.com/chapter/10.1007/978-3-662-53426-7_23
- The Path to Durable Linearizability (POPL 2023): https://people.mpi-sws.org/~viktor/papers/popl2023-path.pdf
