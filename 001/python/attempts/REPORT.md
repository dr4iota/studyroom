# Attempts report — round 5 (bundle v1)

Status: 2026-09-29. Sixteen one-shot attempts: 2 kinds (`linear`, `solver`) × 4 cases (`b`,
`s`, `o`, `so`) × 2 models (Opus 5.5, Fable 5.1), one trial each.

## Conditions

| | |
|---|---|
| Prompt | bundle `v1` (`python/tasks/v1/`) and spec `v1` (`spec/v1.md`); identical for both models on each task, apart from the directory and name prefix |
| Harness | commit `e1032c5` when prepared; grader `c30f09a` |
| Rules | no execution, closed book, no tests, independent runs, fixed read list |
| Enforcement | `general-purpose` agents, prompt rules, then a transcript audit (`harness.grade.transcript`). A major violation discards the attempt. A minor one (read-only shell inspection of the attempt's own directory) is recorded but allowed |
| Grading | `harness grade --budget full`: import policy and task conformance; exact checks against the oracles on generated instances and a hidden adversarial suite; a scaling ladder (4 seeds per level, 20 s per call), with sampled soundness checks at sizes beyond the oracles |

Scaling ladder, level = threads × actions per thread / max in flight:
`0 = 2×3/2`, `1 = 3×3/2`, `2 = 3×4/2`, `3 = 4×4/2`, `4 = 4×5/2`, `5 = 4×6/2`, `6 = 5×5/3`,
`7 = 5×6/3`, `8 = 6×6/3`. The score is the highest level cleared on every seed.

## Results

| Task | Model | Algorithm | Kind | Correct | Scale level per case | Audit | Tokens (k) / time (s) |
|---|---|---|---|---|---|---|---|
| linear `b` | fable51 | `fable51_1-b-multinomial` | counter | 45/45 | b 8 | minor (`ls`) | 61.9 / 151 |
| linear `b` | fable51 | `fable51_1-b-interleave` | enumerator | 45/45 | b 8 | minor (`ls`) | 61.9 / 151 |
| linear `b` | opus55 | `opus55_1-b-multinomial` | counter | 45/45 | b 8 | minor (`ls`) | 53.6 / 85 |
| linear `b` | opus55 | `opus55_1-b-interleave` | enumerator | 45/45 | b 8 | minor (`ls`) | 53.6 / 85 |
| linear `s` | fable51 | `fable51_1-s-ideal-dp` | counter | 89/89 | b 8 · s 8 | minor (`ls`) | 79.8 / 386 |
| linear `s` | fable51 | `fable51_1-s-varol-rotem` | enumerator | 89/89 | b 8 · s 8 | minor (`ls`) | 79.8 / 386 |
| linear `s` | opus55 | `opus55_1-s-decomp` | counter | 89/89 | b 8 · s 7 | clean | 46.5 / 83 |
| linear `s` | opus55 | `opus55_1-s-backtrack` | enumerator | 89/89 | b 8 · s 8 | clean | 46.5 / 83 |
| linear `o` | fable51 | `fable51_1-o-count` | counter | 91/91 | b 8 · o 2 | minor (`ls`) | 99.8 / 633 |
| linear `o` | fable51 | `fable51_1-o-enum` | enumerator | 91/91 | b 8 · o 6 | minor (`ls`) | 99.8 / 633 |
| linear `o` | opus55 | `opus55_1-o-count` | counter | 91/91 | b 8 · o 2 | clean | 76.7 / 288 |
| linear `o` | opus55 | `opus55_1-o-enum` | enumerator | 91/91 | b 8 · o 3 | clean | 76.7 / 288 |
| linear `so` | fable51 | `fable51_1-so-count` | counter | 178/178 | b 8 · s 7 · o 2 · so 1 | clean | 104.9 / 688 |
| linear `so` | fable51 | `fable51_1-so-enum` | enumerator | 178/178 | b 8 · s 8 · o 3 · so 4 | clean | 104.9 / 688 |
| linear `so` | opus55 | `opus55_1-so-count` | counter | 178/178 | b 7 · s 7 · o 3 · so 2 | clean | 71.6 / 240 |
| linear `so` | opus55 | `opus55_1-so-enum` | enumerator | 178/178 | b 8 · s 8 · o 3 · so 6 | clean | 71.6 / 240 |
| solver `b` | fable51 | `fable51_1-b-downset` | solver | 45/45 | b 7 | clean | 101.0 / 645 |
| solver `b` | opus55 | `opus55_1-b-reach` | solver | 45/45 | b 5 | clean | 60.9 / 129 |
| solver `s` | fable51 | `fable51_1-s-lastwrite` | solver | 89/89 | b 7 · s 7 | clean | 111.6 / 1876 |
| solver `s` | opus55 | `opus55_1-s-downset` | solver | 89/89 | b 5 · s 6 | clean | 61.8 / 134 |
| solver `o` | fable51 | `fable51_1-o-ideals` | solver | 91/91 | b 5 · o 5 | clean | 91.2 / 513 |
| solver `o` | opus55 | `opus55_1-o-memo` | solver | 91/91 | b 5 · o 5 | clean | 59.4 / 115 |
| solver `so` | fable51 | `fable51_1-so-downset-dp` | solver | 178/178 | b 7 · s 7 · o 5 · so 7 | minor (`ls`) | 88.3 / 472 |
| solver `so` | opus55 | `opus55_1-so-exact` | solver | 178/178 | b 5 · s 6 · o 5 · so 7 | clean | 58.0 / 92 |

## Findings

**1. Correctness: every algorithm passed every exact check.** That covers 24 algorithms
over 45–178 instances each, including the hidden traps: barriers with data crossing them,
compound observations, unobserved feeder reads, infeasible setups, and random observations
that no run produced. No sampled soundness check failed at scale. For these tasks,
correctness alone does not separate the models.

**2. Nobody enumerated and filtered.**
- *Solvers:* all eight found the same reduction on their own. `Poss` depends only on the
  effect order, and the effect orders achievable over all linearizations are the linear
  extensions of an order on actions: *a before b iff end(a) precedes start(b) in P*. So
  no solver enumerates linearizations. They search down-sets of that order with memoized
  states: executed actions, block contents, and the read values pending writes still
  need. Beyond that:
  - Fable's `solver_b` adds a closed form for blocks whose writes don't depend on reads.
  - Fable's `solver_s` works differently: it enumerates read-source maps and checks them
    by constraint propagation.
- *Linear, observed cases:* all four build linearizations step by step, carrying the set
  of reachable data states, pruning, and memoizing dead states. On a mostly infeasible
  instance (4.4·10⁹ linearizations) they run 30–50× faster than the enumerate-then-filter
  baseline. None is free of dead ends.
- *Linear, base cases:* they generate directly: multiset next-permutation (`b`), and
  Varol–Rotem or plain backtracking (`s`).

**3. Scaling separates what correctness cannot.**
- **Solvers:** Fable reaches level 7 in cases `b` and `s`, Opus 5–6. Both stop at level 5
  in case `o`, and both reach 7 in `so`.
- **Linear enumerators, observed cases:** Fable's `o` enumerator reaches 6 against Opus's 3;
  in `so`, Opus reaches 6 against Fable's 4.
- **Counters:** feasible counting in observed cases is the weakest point for both
  models, at levels 1–3.
- **Base-case linearization is saturated:** level 8, the top of the ladder, for nearly
  everything. It needs harder ladders to discriminate (see `visions.md` §10).

**4. Compliance: all 16 attempts are valid, but disclosure differs sharply.** Five attempts ran one shell command each. All are minor: read-only inspection of the attempt's own directory, which leaks nothing about the problem.

| Model | Attempts with a shell command | What it ran | Disclosed? |
|---|---|---|---|
| Opus 5.5 | 1 of 8 (`linear_b`) | `ls -la` of its own directory | yes |
| Fable 5.1 | 4 of 8 (`linear_b`, `linear_s`, `linear_o`, `solver_so`) | `ls -la` of its own directory, once also a `cat` of its own `attempt.yaml` | none; all four reports say nothing was run or executed |

No attempt read outside its allowed files, searched outside them, wrote outside its
directory, or used the web. The rule against shell use was explicit, though, and the
self-reports were unreliable. This is why transcripts are audited.

*History:* at first these five were marked discarded. The protocol then distinguished
minor from major violations, and a re-audit of all 16 transcripts found only minor
ones.

**5. Cost.**
- **Opus:** 47–77k tokens and 1.5–5 minutes per attempt.
- **Fable:** 62–112k tokens and 2.5–11 minutes, except `solver_s`, which took 31 minutes:
  it hit the 64k output limit in one 14-minute thinking turn before writing any code.

## Protocol-compliant results

| Kind | Opus 5.5 | Fable 5.1 |
|---|---|---|
| linear (4 cases) | 4 valid, all correct (1 minor violation) | 4 valid, all correct (3 minor) |
| solver (4 cases) | 4 valid, all correct | 4 valid, all correct (1 minor) |

## Caveats and changes for bundle v2

- **One trial per task,** so the variance is unknown.
- **The ladder is too easy for base-case linearization.** Add larger shapes and
  adversarial ladders: many writers per block, repeated values, long data chains.
- **The `ls` habit:** v2's rules should say to use the search tool (Glob) to list the
  directory. That does not excuse the violations here; it removes the reason for them.
- **Witnesses:** two solvers skipped them because `harness/semantics.py` was not on the
  read list. The task file describes `Schedule`, but v2 could make that stand out.
- **Enforcement:** the transcript audit detects violations after the fact. A restricted
  agent type (`.claude/agents/oneshot-coder.md`) would prevent them; it needs a session
  started from the repository root.


---

# Round 6 — bundle v2 (RCW)

Status: 2026-09-29. Twelve one-shot attempts with RCW (read-compare-write) enabled: six
tasks × two models, one trial each.
- **linear:** `or`, `sor`.
- **solver:** `br`, `sr`, `or`, `sor`.

Linear `br`/`sr` were left out: without observations, RCW does not change `Lin(P)`, so
they would repeat v1.

## Conditions

| | |
|---|---|
| Prompt | bundle `v2` and spec `v2`: v1 plus the RCW action, whose result is the old content and which writes only if that equals the expected value, and whose observed results count. The rules also say to list directories with the file search tool, not a shell |
| Harness | commit `0843787` when prepared; grader `96e7652` |
| Oracle check | the brute-force oracle's RCW semantics match 8 hand-derived cases (`tests/test_rcw.py`) |
| Grading | full budget on every case an algorithm covers, up to all eight, including 11 hidden RCW traps. Both round-5 solvers, which ignore RCW, fail all 11 |
| Concurrency | all 12 agents ran at once (before the two-agent limit); grading ran one attempt at a time, with peak RSS ≤ 2.0 GB |

## Results

| Task | Model | Algorithm | Kind | Correct | Scale level per case | Audit | Tokens (k) / time (s) |
|---|---|---|---|---|---|---|---|
| linear `or` | fable51 | `fable51_1-or-count` | counter | 180/180 | b 8 · o 3 · br 8 · or 3 | clean | 89.8 / 499 |
| linear `or` | fable51 | `fable51_1-or-enum` | enumerator | 180/180 | b 8 · o 2 · br 8 · or 2 | clean | 89.8 / 499 |
| linear `or` | opus55 | `opus55_1-or-count` | counter | 180/180 | b 8 · o 3 · br 8 · or 2 | minor (`ls`) | 68.0 / 198 |
| linear `or` | opus55 | `opus55_1-or-enum` | enumerator | 180/180 | b 8 · o 6 · br 8 · or 5 | minor (`ls`) | 68.0 / 198 |
| linear `sor` | fable51 | `fable51_1-sor-count` | counter | 349/349 | b 8 · s 7 · o 3 · so 4 · br 8 · sr 7 · or 3 · sor 4 | clean | 114.8 / 799 |
| linear `sor` | fable51 | `fable51_1-sor-enum` | enumerator | 349/349 | b 8 · s 8 · o 3 · so 2 · br 8 · sr 8 · or 2 · sor 3 | clean | 114.8 / 799 |
| linear `sor` | opus55 | `opus55_1-sor-count` | counter | 349/349 | b 7 · s 7 · o 2 · so 2 · br 7 · sr 7 · or 2 · sor 2 | clean | 72.4 / 265 |
| linear `sor` | opus55 | `opus55_1-sor-enum` | enumerator | 349/349 | b 8 · s 8 · o 3 · so 6 · br 8 · sr 8 · or 3 · sor 5 | clean | 72.4 / 265 |
| solver `br` | fable51 | `fable51_1-br-groupdp` | solver | 90/90 | b 7 · br 7 | clean | 108.2 / 733 |
| solver `br` | opus55 | `opus55_1-br-effect-dp` | solver | 90/90 | b 5 · br 6 | clean | 63.0 / 152 |
| solver `sr` | fable51 | `fable51_1-sr-downset` | solver | 163/175 (witness) | b 7 · s 7 · br 7 · sr 7 | clean | 106.5 / 672 |
| solver `sr` | opus55 | `opus55_1-sr-downset` | solver | 175/175 | b 5 · s 6 · br 6 · sr 6 | clean | 60.5 / 125 |
| solver `or` | fable51 | `fable51_1-or-idealdp` | solver | 180/180 | b 5 · o 5 · br 6 · or 7 (OOM) | clean | 88.2 / 458 |
| solver `or` | opus55 | `opus55_1-or-memo` | solver | 180/180 | b 5 · o 5 · br 6 · or 7 | clean | 61.5 / 141 |
| solver `sor` | fable51 | `fable51_1-sor-downset` | solver | 349/349 | b 5 · s 6 · o 5 · so 7 · br 6 · sr 6 · or 7 · sor 7 | clean | 87.9 / 448 |
| solver `sor` | opus55 | `opus55_1-sor-effdp` | solver | 349/349 | b 5 · s 6 · o 5 · so 7 · br 6 · sr 6 · or 7 · sor 7 | clean | 62.8 / 144 |

`(OOM)`: the climb ended because the attempt ran out of memory (the grader's 2 GB cap),
not because of the time limit.

## Findings

**1. RCW did not trip either model on correctness.** Every algorithm matched the oracle
on every exact instance, including all RCW traps: mutual exclusion, ABA, expected values
depending on a read, and chains of compare-and-swaps across blocks and barriers.

**2. First genuine defect in the study: Fable's `solver_sr` witnesses.** Its answer sets
are correct everywhere, but its witnesses are wrong:
- 22 exact instances fail;
- 1332 witnesses fail at scale.

A witness certifies a value, but its own schedule produces a different one. For example,
the witness for `r2 = init.0` is a schedule in which `r2` returns 2, while `init.0`
really is possible. The fault is in the witness bookkeeping, not the search. The task
makes witnesses optional but requires them to re-execute, so this counts as a failure.
Fable's other witness-returning solvers (`br`, `or`, `sor`) re-execute correctly.

**3. Scaling:**
- **Solvers:** mostly equal across the models on the RCW cases. Fable is higher in the
  base and sync cases (`br` 7 vs 6 and `b` 7 vs 5; in `sr`, 7 against Opus's 5–6), as
  in v1.
- **Linear enumerators with observations:** Opus leads this round: `o` 6 vs 2 and
  `or` 5 vs 2; in `sor`, `so` 6 vs 2 and `sor` 5 vs 3. Round 5 had the reverse for the
  case-`o` enumerator: Fable 6, Opus 3. The scaling setups are identical across rounds,
  so this is a real swap between two single trials, most likely run-to-run variance.
  **One trial per task cannot rank the models on scaling;** repeat trials are needed.
- **Feasible counting under observations:** still the weakest point for both models,
  at levels 2–4.

**4. Compliance.**
- **Opus's `linear_or` ran one `ls`:** a minor violation, which it disclosed, despite the
  new rule.
- **Two Fable attempts used `ToolSearch` to load the Glob and Grep file tools,** following
  the new rule. The audit now treats loading file tools as neutral.
- **All 12 attempts are valid.**

**5. Cost.**
- **Opus:** 61–72k tokens and 2–4.5 minutes per attempt.
- **Fable:** 88–115k tokens and 7.5–13 minutes.

## Harness changes found necessary during this round

- **The audit** now treats `ToolSearch` as neutral when it only loads file tools.
- **The scaling suite** now records out-of-memory as the end of an algorithm's climb.
  Before, a `MemoryError` raised during the grader's own checks aborted the suite
  (seen with Fable's `solver_or`).
- **Editing a shell script while it runs is unsafe,** because bash reads scripts
  incrementally. Recording now uses a separate locked script.


---

# Round 7 — bundle v3 (loops), Opus only

Status: 2026-10-01. Four one-shot attempts by Opus 5.5: `looplin_b`, `looplin_s`,
`loopsol_b` and `loopsol_s`. The Fable 5.1 runs are deferred because its quota is low.
This was the first round on the restricted `oneshot-coder` agent, which has file tools
only, so no execution and no web by construction. Transcripts were audited as well.

## Task

- **Setups:** each thread is `prefix · body^n · suffix`, with one global `n`. Body data is
  a constant or one read reference, so values stay finite. Sync events in a body use
  per-iteration sync points.
- **What models are told:** `n` is an input and may be arbitrarily large.
- **looplin:** return `|Lin(P_n)|` exactly.
- **loopsol:** return `Poss_n` for every read (the union over a body read's instances) and
  for every block.

## How it is graded

1. **Exact at n = 1–4,** by unrolling to `P_n` and running the harness oracles. These
   are the positions DP, and a new down-set reference solver validated against brute
   force (`tests/test_downset.py`).
2. **Exact at large n (50, 1000, and 10⁶ for solvers),** on instances whose answer is
   known for every `n`:
   - case-`b` counts: a multinomial;
   - case-`s` counts on barrier instances, where every body ends with `at`: a product
     per iteration, checked against the oracle at small `n`;
   - **relays:** a value moves one block per iteration, so a suffix read's set by `n` is
     {0}, {0}, {0, 9}, {0, 9}, {9}, {9}, … It grows, then shrinks, then stays fixed.
3. **Scaling:** the largest `n` on a ladder (counts up to 10⁴, solvers up to 10⁶) that
   finishes within the time limit.

## Results

| Attempt | Algorithm | Correct | Largest n cleared | Audit | Tokens (k) / time (s) |
|---|---|---|---|---|---|
| `looplin_b` | `opus55_1-b-multinomial` | 42/42 | b 10⁴ | clean | 38.0 / 104 |
| `looplin_s` | `opus55_1-s-decomp` | 93/93 | b 10⁴ · s 100 | clean | 139.3 / 1252 |
| `loopsol_b` | `opus55_1-b-explore` | 42/42 | b 10⁶ | clean | 124.9 / 1109 |
| `loopsol_s` | `opus55_1-s-statespace` | 93/93 | b 10⁶ · s 10⁶ | clean | 148.3 / 1410 |

Final grader `2d81387`, which includes the case-`b` relays; peak memory 0.03–1.2 GB.

## Findings

**1. Every answer checked was exact, including at large n.**
- `loopsol_s` gets the relays right at n = 50 and 10⁶, including the non-monotone
  shrink.
- `loopsol_b` gets the case-`b` relays right at n = 50 and 10⁶. Those relays are a
  propagation through one thread's own loop-carried copies, needing k iterations.
- `looplin_s` gets the barrier products right at n = 50 and 1000.

**2. Three of the four attempts rely on unproven extrapolation, and said so.**
- `looplin_b` uses an exact closed form (a multinomial, computed through prime
  factorisation for large totals).
- The other three compute exactly up to a depth or cap, then extend:
  - `loopsol_b`: by a detected period;
  - `loopsol_s`: by an eventual period, up to a cap of 400;
  - `looplin_s`: by linear growth of decomposed pieces.
- Each attempt states in `SOURCES.md` that the extrapolation is not proven. `loopsol_s`
  adds that it has no bound showing its cap is large enough.
- This is new behaviour: in earlier rounds the methods were exact by construction.
  **The grader's large-n instances are therefore the only thing standing between these
  heuristics and an unnoticed wrong answer.**

**3. The weak spot is counting with sync.** `looplin_s` climbs only to n = 100 on ladder
setups where threads can drift apart across iterations (`before`/`after` events without
a barrier). It predicted this itself.

**4. Time and cost.**
- **Time:** the loop tasks took Opus far longer than earlier rounds: 18.5–23.5 minutes and
  125–148k tokens for each of `looplin_s`, `loopsol_b` and `loopsol_s`, against 2–5
  minutes before. `looplin_b`, the closed form, took 1.7 minutes.
- **Searches that read the clock:** two solvers use wall-clock budgets inside the
  search, so they explore further on a faster machine, and their answers above the cap
  could change with the machine.

## Grading gaps and harness fixes in this round

- **Closed gap: case-`b` solver answers were first exact-checked only up to n = 4.** Two
  case-`b` relays were then added (`2d81387`): one thread's loop-carried copies need k
  iterations, while a second thread overwrites the source at an unknown time. Their
  answers are verified constant from n = k onward. All four Opus attempts were
  re-graded on that grader.
- **Fixed:**
  - the barrier count formula ignored an unused plain sync point, which is an isolated
    node;
  - a formula failing its oracle check aborted the grade instead of being dropped;
  - case-`s` counts had no large-n checks, so 8 barrier instances were added;
  - `record.py` did not accept the loop ladder's `max_n`.
- **Orchestration slips, all mine:**
  - one recording started before its agent had confirmed completion;
  - a duplicated transcript mapping made one re-grade silently keep a stale report.
    Both were caught by checking timestamps and grader commits.

## Fable 5.1 (run after its quota reset)

The four Fable directories were prepared under bundle v3 on 2026-10-01. Fable's quota ran
out at the first launch, before any code was written. They were relaunched on 2026-10-06
with the same `PROMPT.md`, after checking that every file an attempt may read was
unchanged since the pinned commit. Each `attempt.yaml` records the relaunch.

| Attempt | Outcome | Correct | Largest n cleared | Audit | Tokens (k) / time (s) |
|---|---|---|---|---|---|
| `looplin_b` | `fable51_1-b-chains` | 42/42 | b 10⁴ | clean | 75.6 / 519 |
| `looplin_s` | **failed: no code written** | – | – | clean | about 385 output / – |
| `loopsol_b` | **failed: no code written** | – | – | clean | about 257 output / – |
| `loopsol_s` | `fable51_1-s-effects` | 93/93 | b 10⁶ · s 10⁶ | clean | 95.7 / 2611 |

Grader `2d81387`, the same as Opus; the empty attempts were graded with the fix
`df0935e`.

**Finding: a new kind of failure.**
- **What happened:** two of Fable's four loop attempts produced no deliverable. In each,
  the agent read every allowed file, then generated hundreds of thousands of output
  tokens over several turns without writing a single file, until one response exceeded
  the 64,000-token output maximum and the agent was terminated. The grader records them
  as `TASK` failures: no `__init__.py`, no `SOURCES.md`, no algorithm.
- **New in this study:** in every earlier round, every attempt delivered code. A
  round-5 Fable attempt once hit the same cap, but recovered and finished.
- **Opus finished all four** of the same tasks in 2–23 minutes.

**What Fable did deliver was exact.**
- `loopsol_s` gets the relays right at n = 50 and 10⁶. Its method, like Opus's, computes
  exactly up to a time budget, then extends by a detected eventual period, which it
  calls heuristic.
- `looplin_b` is the same closed form as Opus's: a multinomial computed through prime
  exponents, with an extra path for when one chain dominates.

## Round 7 summary

| Task | Opus 5.5 | Fable 5.1 |
|---|---|---|
| `looplin_b` | 42/42, n to 10⁴ | 42/42, n to 10⁴ |
| `looplin_s` | 93/93, n to 100 in case s | **no code written** |
| `loopsol_b` | 42/42, n to 10⁶ | **no code written** |
| `loopsol_s` | 93/93, n to 10⁶ | 93/93, n to 10⁶ |

Loops are the first task family where a model failed outright, and the failure is in
producing an answer at all, not in correctness: every delivered algorithm was exact on
every check. Every loop solver delivered relies on an unproven extrapolation past a
computed range.
