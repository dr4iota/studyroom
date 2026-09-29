# Attempts report — round 5 (bundle v1)

Status: 2026-09-29. Sixteen one-shot attempts: 2 kinds (`linear`, `solver`) × 4 cases (`b`,
`s`, `o`, `so`) × 2 models (Opus 5.5, Fable 5.1), one trial each.

## Conditions

| | |
|---|---|
| Prompt | bundle `v1` (`python/tasks/v1/`) and spec `v1` (`spec/v1.md`); identical for both models on each task, apart from the directory and name prefix |
| Harness | commit `e1032c5` when prepared; grader `c30f09a` |
| Rules | no execution, closed book, no tests, independent runs, fixed read list |
| Enforcement | `general-purpose` agents, prompt rules, then a transcript audit (`harness.grade.transcript`); a violating attempt is **discarded** but still graded, for information |
| Grading | `harness grade --budget full`: import policy and task conformance; exact checks against the oracles on generated instances and a hidden adversarial suite; a scaling ladder (4 seeds per level, 20 s per call), with sampled soundness checks at sizes beyond the oracles |

Scaling ladder, level = threads × actions per thread / max in flight:
`0 = 2×3/2`, `1 = 3×3/2`, `2 = 3×4/2`, `3 = 4×4/2`, `4 = 4×5/2`, `5 = 4×6/2`, `6 = 5×5/3`,
`7 = 5×6/3`, `8 = 6×6/3`. The score is the highest level cleared on every seed.

## Results

| Task | Model | Algorithm | Kind | Correct | Scale level per case | Audit | Tokens (k) / time (s) |
|---|---|---|---|---|---|---|---|
| linear `b` | fable51 | `fable51_1-b-multinomial` | counter | 45/45 | b 8 | **discarded** | 61.9 / 151 |
| linear `b` | fable51 | `fable51_1-b-interleave` | enumerator | 45/45 | b 8 | **discarded** | 61.9 / 151 |
| linear `b` | opus55 | `opus55_1-b-multinomial` | counter | 45/45 | b 8 | **discarded** | 53.6 / 85 |
| linear `b` | opus55 | `opus55_1-b-interleave` | enumerator | 45/45 | b 8 | **discarded** | 53.6 / 85 |
| linear `s` | fable51 | `fable51_1-s-ideal-dp` | counter | 89/89 | b 8 · s 8 | **discarded** | 79.8 / 386 |
| linear `s` | fable51 | `fable51_1-s-varol-rotem` | enumerator | 89/89 | b 8 · s 8 | **discarded** | 79.8 / 386 |
| linear `s` | opus55 | `opus55_1-s-decomp` | counter | 89/89 | b 8 · s 7 | clean | 46.5 / 83 |
| linear `s` | opus55 | `opus55_1-s-backtrack` | enumerator | 89/89 | b 8 · s 8 | clean | 46.5 / 83 |
| linear `o` | fable51 | `fable51_1-o-count` | counter | 91/91 | b 8 · o 2 | **discarded** | 99.8 / 633 |
| linear `o` | fable51 | `fable51_1-o-enum` | enumerator | 91/91 | b 8 · o 6 | **discarded** | 99.8 / 633 |
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
| solver `so` | fable51 | `fable51_1-so-downset-dp` | solver | 178/178 | b 7 · s 7 · o 5 · so 7 | **discarded** | 88.3 / 472 |
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

**4. Protocol compliance differs sharply.** Five attempts ran one shell command each:

| Model | Attempts with a shell command | What it ran | Disclosed? |
|---|---|---|---|
| Opus 5.5 | 1 of 8 (`linear_b`) | `ls -la` of its own directory | yes |
| Fable 5.1 | 4 of 8 (`linear_b`, `linear_s`, `linear_o`, `solver_so`) | `ls -la` of its own directory, once also a `cat` of its own `attempt.yaml` | none; all four reports say nothing was run or executed |

No attempt read outside its allowed files, searched outside them, wrote outside its
directory, or used the web. The commands revealed nothing about the problem, but the rule
was explicit, and self-reports were unreliable. This is why transcripts are audited.

**5. Cost.**
- **Opus:** 47–77k tokens and 1.5–5 minutes per attempt.
- **Fable:** 62–112k tokens and 2.5–11 minutes, except `solver_s`, which took 31 minutes:
  it hit the 64k output limit in one 14-minute thinking turn before writing any code.

## Protocol-compliant results

Counting a discarded attempt as a failure:

| Kind | Opus 5.5 | Fable 5.1 |
|---|---|---|
| linear (4 cases) | 3 compliant, all correct | 1 compliant (`so`), correct |
| solver (4 cases) | 4 compliant, all correct | 3 compliant, all correct |

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
