# Model comparison: Fable 5.1 vs Opus 5.5 on linearization enumeration

Status: 2026-09-28. Four rounds with the same task structure. In each round, both models
received an identical prompt, apart from their own directory, name prefix and a ban on
reading the other model's code. Each agent ran independently in the background. All
numbers below were measured again by the orchestrating session, not copied from the
agents' self-reports, unless marked "self-reported".

## Where the code is now (reorganized 2026-09-29)

This report uses the names and paths from the time of the rounds. The code has since
moved into the four-case layout described in [`README.md`](README.md):

| Round | Old path | New path | Old name → new name |
|---|---|---|---|
| 1 | `opus/`, `fable/` | `linear_opus55_1/base/`, `linear_fable51_1/base/` | `opus-X` → `opus55-b-X`, `fable-X` → `fable51-b-X` |
| 2 | `opus_sync/`, `fable_sync/` | `linear_*_1/base_sync/` | `opus-s-X` → `opus55-s-X`, `fable-s-X` → `fable51-s-X` |
| 3 | `opus_obs/`, `fable_obs/` | `_archive/opus_obs/`, `_archive/fable_obs/` (superseded) | unchanged |
| 4 | `opus_dep/`, `fable_dep/` | `linear_*_1/obs/` | `opus-d-X` → `opus55-o-X`, `fable-d-X` → `fable51-o-X` |

Read-dependent data is now part of the base problem, and the `window` solver was
removed, so the round-3 code (constant data only) no longer fits any case.

## TL;DR

- **Both models were correct in every round.** No enumerator ever failed an independent
  check. Across 33 enumerators, independent tests found zero wrong, missing or duplicated
  outputs.
- **Opus finished sooner and used fewer tokens in every round.** It used 39–92% of Fable's
  tokens and 21–93% of its wall-clock time. The gap narrowed as the tasks got harder.
- **Speed of the best algorithm varied by round:**
  - Opus won round 1 (base case), round 3 (observed reads) and round 4 (read-dependent
    data), the last two with its precedence-splitting enumerator (`opus-o-split`,
    `opus-d-split`).
  - Fable won round 2 (sync), but it looked up Pruesse–Ruskey on the web in that round.
  - Fable's automaton DP (`fable-o-dp`/`fable-d-dp`) was the most robust design: no
    dead ends, rank/unrank, and the best counter in round 3. In round 4 all counters were
    instant.
- **Both models independently reached the same theory:**
  - a Gray code with exactly one adjacent swap per step is impossible;
  - for observations, effect orders are exactly the extensions of the interval order;
  - blocks are independent;
  - unobserved reads don't matter;
  - checking a fixed L is NP-hard with repeated values;
  - in round 4, both independently found that per-block independence and "unobserved
    reads don't matter" break, that the merging lemma survives, and that free-term
    matching pins down what inner reads saw.
- **Style differed.** Fable wrote more code, more exhaustive property tests and more
  structural extras (rank/unrank, per-segment caching, a second exact feasibility test).
  Opus made sharper algorithmic choices that paid off in speed, above all `opus-o-split`.

## Setup

| | Round 1 — base | Round 2 — sync | Round 3 — observed reads | Round 4 — read-dependent data |
|---|---|---|---|---|
| Scope | R/W, no sync, no observations | + `before`/`after`/`at` sync points | + partially observed read results (sync allowed) | + write data built from reads (`r1~7`), compound observations; **no sync** |
| Output | `Lin(P)` = interleavings of chains | `Lin(P)` of a general DAG | `LinFeas(P)`: feasible linearizations only | `LinFeas(P)` |
| Oracle | `backtrack` + DP count | `backtrack` + DP count | `backtrack-feasible` (brute-force effect-order DFS) | `backtrack-feasible` |
| Web access | not mentioned | not mentioned (Fable used it) | **forbidden** | **forbidden** |
| Directories | `contrib/{opus,fable}` | `contrib/{opus,fable}_sync` | `contrib/{opus,fable}_obs` | `contrib/{opus,fable}_dep` |

Every agent had to deliver at least three enumerators, docstrings with costs, a
`unittest` suite, a CLI check and a benchmark against the reference, all under a 2 GB
memory cap. The cap was added after the first session crashed WSL.

## Round 1 — base case (interleavings of N chains)

| | Opus | Fable |
|---|---|---|
| Enumerators | `lex` (Knuth L), `coollex` (loopless), `vr` (Varol–Rotem), `neargray` (own construction) | `lex`, `coollex`, `unrank` (ranked, chunkable), `gray` (SJT + Chase-style lists) |
| Counter | multinomial | multinomial |
| Near-Gray | `neargray`: 1 swap or a 2-place move per step | `gray`: 1–2 adjacent swaps per step, with a proof sketch |
| Key insight | parity argument: exact 1-swap Gray code impossible (4 vs 2 classes for 2×2) | same; q-multinomial at q=−1; base example is 472/452 |
| Tests (own) | 6 tests, 34 s | 12 tests, 41 s |
| Code / tests | 548 / 171 lines | 783 / 258 lines |
| Tokens / time | ~90k / 11 min | ~230k / 41 min |

Throughput, thousands of outputs per second, first 200k outputs:

| Algorithm | [5,5] | [3,3,3] | [1]×6 | [10,10,1] |
|---|---|---|---|---|
| backtrack | 529 | 656 | 801 | 482 |
| **opus-vr** | **2181** | **2589** | **3186** | **3112** |
| opus-neargray | 2186 | 2322 | 2427 | 2225 |
| opus-coollex | 1850 | 1937 | 1986 | 1612 |
| opus-lex | 1214 | 1319 | 1478 | 885 |
| fable-lex | 1190 | 1281 | 1428 | 872 |
| fable-coollex | 604 | 669 | 832 | 331 |
| fable-gray | 555 | 612 | 768 | 343 |
| fable-unrank | 195 | 191 | 229 | 91 |

**Verdict: Opus.** All four Opus enumerators beat every Fable enumerator except
`fable-lex`. Opus updates only the changed suffix of the output tuple. Fable's
constant-time designs rebuild the whole tuple each step, which dominates in CPython.
Fable's `unrank` is the only enumerator in this round that can be resumed or split
into chunks.

## Round 2 — sync (general DAG, width ≤ N+K)

| | Opus | Fable |
|---|---|---|
| Enumerators | `vr`, `pr` (Pruesse–Ruskey), `tree` (Ono–Nakano-style), `seg` (cut-node product) | `pr`, `vr`, `tree`, `dp` (rank/unrank), `cut` (cut-node product, cached) |
| Counter | per-segment DP product | per-segment DP product |
| Pruesse–Ruskey source | **reconstructed from memory** | **transcribed from Ruskey's book, fetched from the web** |
| Adjacency | `pr` ≤ 2 swaps; `tree` ≤ 3 swaps | `pr` ≤ 2 swaps; `tree` parent/child = 1 swap |
| Tests (own) | 17 tests, 36 s; +600 random DAGs vs brute force | 15 tests, 58 s; ~900 generated + 24 hand-made |
| Code / tests | 882 / 287 lines | 1204 / 376 lines |
| Tokens / time | ~117k / 12 min | ~215k / 56 min |

Throughput, thousands of outputs per second, first 150k outputs:

| Algorithm | base T2A3 | T3A3 K2E2 before/after | T4A2 K2E1 all | T3A3 K3E2 at |
|---|---|---|---|---|
| backtrack | 547 | 625 | 623 | 586 |
| **fable-s-vr** | **2377** | **2786** | **2782** | **2331** |
| opus-s-vr | 1696 | 2653 | 2525 | 1800 |
| opus-s-seg | 1330 | 1714 | 1621 | 1254 |
| fable-s-tree | 1272 | 1274 | 1297 | 1260 |
| opus-s-pr | 1151 | 1271 | 1341 | 1223 |
| opus-s-tree | 1147 | 1217 | 1232 | 1180 |
| fable-s-pr | 1030 | 966 | 1056 | 1013 |
| fable-s-dp | 909 | 1013 | 1101 | 1057 |
| fable-s-cut | 556 | 422 | 499 | 541 |

**Verdict: Fable on speed, with a caveat.**
- `fable-s-vr` was 5–40% ahead of `opus-s-vr`.
- Opus's `pr` and `tree` were slightly faster than Fable's `pr`.
- Fable's use of the web to obtain Pruesse–Ruskey makes this round an unequal
  comparison; round 3 forbade it.
- `fable-s-cut` helps only on posets with full barriers: 2.8M per second self-reported,
  but below `backtrack` elsewhere.

## Round 3 — partially observed reads (`LinFeas(P)`)

| | Opus | Fable |
|---|---|---|
| Fixed-L test | reads-from backtracking with a cluster criterion (no read before its source; no write cluster before an init read; no 2-cycle between clusters) | **two** exact tests: a slot criterion over write orders, and an automaton over (effected in-flight set, content) |
| Enumerators | `filter` (VR + test), `prune` (prefix DFS), `memo` (dead-state memo), **`split`** (branch on undecided precedence pairs; accept or drop whole sub-posets) | `prune`, `auto` (incremental automaton + lookahead), **`dp`** (DP over (down-set, automaton state), zero dead ends, rank/unrank), `filter` (PR Gray code + re-test only affected blocks) |
| Counters | `splitcount`, `dpcount` | `count` (DP) |
| Data classes | constants, `"*"`, unknown init; no read-dependent data | same |
| Tests (own) | 23 tests, 75 s; fuzz on 2,684 random-observation instances | 10 tests, 86 s; 328 generated + 27 hand-made instances |
| Code / tests | 1138 / 267 lines | 1260 / 344 lines |
| Tokens / time | ~152k / 23 min | ~180k / 33 min |

Independent check, the same script run on both models:
- 44 instances, including random unrealizable observations; 11 of them have no
  feasible L at all.
- For every enumerator, the output set equals the oracle's set.
- `is_feasible_fast` against brute force: 22,948 orders, 0 mismatches for each model.

Feasible outputs per second, each pair in its own process with a 40 s limit:

| Algorithm | p_r 0.3, K=0 | p_r 0.7, K=1 | p_r 1.0, K=2 | hand-made 1,2,1,2 |
|---|---|---|---|---|
| backtrack-feasible | 30.7k | timeout | 4.7k | 2.4k |
| **opus-o-split** | **1133k** | **1389k** | **1690k** | **1350k** |
| fable-o-dp | 546k | 496k | 544k | 525k |
| fable-o-auto | 156k | 149k | 213k | 85k |
| fable-o-filter | 132k | 28k | 43k | 13k |
| opus-o-prune | 56k | 58k | 67k | 33k |
| opus-o-memo | 48k | 50k | 56k | 27k |
| fable-o-prune | 37k | 40k | 42k | 14k |
| opus-o-filter | 11k | timeout | timeout | 14k |

Feasible counting: all counters agree on every instance.

| Counter | p_r 0.3 | p_r 0.7 | p_r 1.0 | hand-made |
|---|---|---|---|---|
| **fable-o-count** | instant | instant | instant | **instant** |
| opus-o-splitcount | instant | instant | instant | 4.4 s |
| opus-o-dpcount | 0.4 s | 0.5 s | 0.2 s | 24 s |

**Verdict: split.**
- **Enumeration: Opus.** `opus-o-split` is 2–3× faster than Fable's best and up to
  about 560× faster than the oracle.
- **Counting and structure: Fable.** Its automaton DP counts with no dead ends and
  supports rank/unrank.
- **One weakness found by the independent benchmark:** `opus-o-filter` times out when
  constants repeat, because its fixed-L test goes exponential. Opus's report mentioned
  this worst case but did not benchmark it.

## Round 4 — read-dependent write data (no sync)

Write data may be any expression over constants, `"*"`, earlier reads and earlier writes of
the same thread. Observations may be compound terms such as `init.1~7`. The prompt warned
that some round-3 lemmas might break, and asked each model to say which.

**Lemma audit.** Both models reached the same conclusions independently:

| Lemma | Opus | Fable |
|---|---|---|
| Effect orders = extensions of the interval order | survives | survives |
| Merging per-part orders into one global order | survives | survives, for any partition (shortest-cycle argument) |
| Per-block independence | **breaks**: blocks are coupled through values | **breaks**; replaced by *data-flow components* |
| Unobserved reads never matter | **breaks**: a feeder read must return a specific term | **breaks**; reads mentioned by no goal are still droppable |
| Structural value matching | free-term matching binds every source read to one subterm | same; a term equals at most one goal value, so a class abstraction is exact |

| | Opus | Fable |
|---|---|---|
| Fixed-L tests | reads-from DFS over required reads (closure of bindings) + cluster criterion; 12–69 µs per L | two: a reads-from/precedence-digraph criterion, and an automaton over components |
| Pre-processing | **static pins**: necessary edges derived from forced sources, iterated to a fixpoint | greatest-fixpoint pruning of impossible goals |
| Enumerators | `filter` (± pins), `prune` (witness reuse), `memo`, **`split`** | `prune`, `auto`, **`dp`** (zero dead ends, rank/unrank), `filter` (PR Gray + re-test only affected components) |
| Counters | `splitcount`, `dpcount` | `count` |
| Tests (own) | 23 tests, 203 s; 1,027 additional scratch instances | 11 tests, 93 s; 35 hand-made + 128 generated oracle instances |
| Code / tests | 1512 / 345 lines | 1557 / 395 lines |
| Tokens / time | ~171k / 25 min | ~185k / 27 min |

Independent check, the same script run on both models:
- 70 instances, 32 with read-dependent data.
- 26 of them have no feasible L at all, from random compound observations built out of
  subterms of a real run.
- All 8 enumerators produce exactly the oracle's set.
- Both `is_feasible_fast` implementations agree with brute force on 42,476 orders.

Feasible outputs per second, 10 s cap per run. `*` means the cap was hit before 150k
outputs. copy, combine and pool1 are generated with T3A3 (|Lin| = 1.7·10⁷); chain is a
hand-made cross-block dependence chain with compound observations (|Lin| = 8.2·10⁹).

| Algorithm | copy | combine | pool1 | chain |
|---|---|---|---|---|
| backtrack-feasible | 0 in 10 s | 13.5k* | 23.3k | 0 in 10 s |
| **opus-d-split** | **2638k** | **1942k** | **1861k** | **1427k** |
| fable-d-dp | 485k | 617k | 574k | 491k |
| opus-d-prune | 287k | 358k | 306k | 245k |
| opus-d-memo | 165k | 237k | 191k | 162k |
| fable-d-auto | 73k | 171k | 126k | 102k |
| fable-d-filter | 20k | 495k | 78k | 5.8k* |
| opus-d-filter | 11.3k* | 87k | 34k | 43k |
| fable-d-prune | 20k | 56k | 28k | 18k |

All three counters agree on every instance (2.72·10⁶, 1.70·10⁷, 1.25·10⁷, 2.61·10⁸
feasible) and finish in at most 0.3 s.

**Verdict: Opus.**
- `opus-d-split` is 3–5× faster than Fable's best (`fable-d-dp`). On two instances the
  reference oracle produced nothing in 10 s.
- Opus's `prune` also beats Fable's `auto` and `prune`, helped by reusing a stored
  witness instead of searching again.
- Fable's design is the more principled one: data-flow components, an exact class
  abstraction, and a DP with no dead ends.
- The two were nearly identical in cost this round.

## Cross-round observations

1. **Correctness.** No defect was found in either model's work in any round. Both wrote
   self-checking test suites that my independent checks confirmed.
2. **Honesty about limits.** Both models declined to set `gray_code = True` and
   explained why with a correct parity argument. Both flagged "tested, not proved"
   claims unprompted. Both disclosed going over the benchmark budget (7.5–9M outputs
   against the ~5M guideline); nothing crashed, and everything was streamed under the
   memory cap.
3. **Theory in rounds 3–4** was reached independently with the same core lemmas,
   including the same audit of which lemmas break with read-dependent data. Fable
   went further on structure (a second criterion, an automaton that is polynomial for
   bounded in-flight width). Opus went further on an algorithmic trick: splitting on
   precedence pairs and accepting a whole sub-poset when its upper bound is feasible.
   Opus reused that trick in round 4, and it won both rounds by a wide margin.
4. **Engineering in Python.** Opus consistently avoided rebuilding the output tuple,
   and that alone accounted for most of its round-1 lead. Fable often chose
   asymptotically nicer designs (loopless, constant amortized time, Gray) that lost to
   interpreter overhead.
5. **Cost.** Opus used about 531k tokens and 71 min in total. Fable used about 810k
   tokens and 157 min. In round 4 the two were almost equal (171k vs 185k tokens). Fable also launched background jobs and waited on them, which
   stretched its wall-clock time.

| Totals | Opus 5.5 | Fable 5.1 |
|---|---|---|
| Algorithms delivered (enum + count) | 16 + 6 | 17 + 4 |
| Code (incl. tests) | 4,080 lines | 4,804 lines |
| Tokens | ~531k | ~810k |
| Wall-clock | ~71 min | ~157 min |
| Round wins (best enumerator speed) | R1, R3, R4 | R2 (with web lookup) |
| Independent-check failures | 0 | 0 |

## Caveats

- There is one run per model per round, with no repeats, so the variance is unknown.
- Benchmarks are CPython, single-threaded, on WSL. Absolute numbers are
  machine-specific; the ratios are what matter.
- The round-2 comparison is confounded by web access. Round 3 controls for it.
- My round-3 and round-4 benchmarks used only four instances each. Rankings on instances with many ties
  or very wide posets could differ, and `fable-o-dp`'s memory grows with poset width.

- In round 4 the generator rarely produced read-dependent data on the small instances the
  oracle can handle. Both models compensated with dedicated sweeps and hand-made cases.
- The generator never creates a write that references another write, so that case is
  covered only by hand-made tests.

## Possible next rounds

- **Round 5:** read-dependent data **with** sync. Opus's code runs on any DAG but is
  untested there. Fable's component automaton assumes chains.
- **RCW:** compare-and-write makes success depend on the value read, so data flows back
  into block state.
- **Solvers instead of enumerators:** compute `Poss(r)` exactly (SOLVE-READ). The
  feasibility machinery from rounds 3–4 is the natural starting point.
