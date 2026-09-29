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
