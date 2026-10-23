# Premise: deducing the outcomes of a concurrent I/O trace

Study 001 tests whether a model can *write code* that solves trace problems. This study
tests whether a model can *solve one by reasoning*. The model reads a small trace in plain
language and lists every possible combination of a few asked values. A program computes
the exact answer, and the model's list is graded against it.

## 1. The problem

- `N` threads, `M` blocks (`x`, `y`, …) and `K` sync points (`P`, `Q`, …). Every block
  holds 0 at the start.
- Each thread runs a list of operations one at a time (synchronous I/O). An operation
  has a start and an end, and takes effect at one instant between them. Operations of
  different threads may overlap.
- Operations:
  - `read x`. The read may come with its result (`read x, returned 2`). A given result
    restricts the executions to those that produce it.
  - `write c to x`, where `c` is a constant `1..V`. Two writes may carry the same
    constant.
  - `write the value read by A2 to x`, which copies an earlier read of the same thread
    whose result is not given.
- Sync lines sit between steps (starts and ends):
  - `-- before P`: the thread's steps above the line come before the instant `P`.
  - `-- after P`: the steps below the line come after `P`.
  - `-- at P`: both. Several `at P` lines on different threads form a barrier.
- A sync line may sit inside an operation, between its start and its end. Only that
  operation's start or end is then ordered by the line, not its effect. Without such
  lines, synchronous intervals behave exactly like atomic operations.
- No two operations take effect at the same instant. A read returns the last value
  written to its block before it.

The problem asks for 1–3 locations. A location is either the value returned by a read
whose result is not given, or the final content of a block. The answer is the **joint**
set of value combinations over all executions that agree with the given results. This
set is generally not the product of the per-location sets. The generator keeps an
answer only if it has between 12 and 99 combinations (adjustable): big enough that
guessing fails, small enough to write down.

## 2. Ground truth

`python/deduce.py` holds two exact solvers that share nothing but the effect of a single
operation:

- **brute** (the enumerator): every interleaving of all steps of the step poset,
  including an explicit effect step per operation, merging identical states.
- **solve** (the solver): only the order of effects. Operation `a` must take effect
  before `b` exactly when `a`'s end precedes `b`'s start in the step poset. The effect
  orders are the linear extensions of that relation. It walks those orders layer by layer
  and keeps a read value only while something still needs it.

Every generated problem is solved by both. A disagreement stops generation and is
reported. The given read results come from one random execution, so every problem has
at least one solution.

**Traps.** `truth.json` also records each answer's *trap rows*: combinations a reader is
likely to get wrong, by kind. The kinds come from the errors in the first 610 runs. The
rate is how often such a row was answered wrongly; for other rows it was 0.3%.

| Kind | Rows | Wrong |
|---|---|---|
| `interval` | rows that change when a sync line inside an operation is read as outside it, i.e. as ordering the whole operation | 35% |
| `depth2` | true rows that every execution reaches through at least 2 copy hops | 4.7% |
| `depth1` | true rows that need exactly 1 copy hop | 2.3% |
| `decoys` | impossible rows made of values each asked location can take on its own | 1.2% |

Decoys account for 82 of the 107 impossible rows models listed in those runs. The grade
counts, for each kind, how many of its rows the answer got wrong (`trap_wrong`).

**Adversarial selection** (`adversarial: 1`, name suffix `x`). Among the sets of asked
locations that pass the size filter, pick the one with the highest score,
`10·interval + 2·depth2 + depth1 + decoys/2`, roughly the expected number of wrong rows.
Reject the seed if no set scores above 0. This changes which locations are asked, so it
is part of the name.

## 3. Generator parameters

| Parameter | Meaning | Default |
|---|---|---|
| `threads` | `N` | 2 |
| `ops` | max operations per thread (each thread gets `ops-1` or `ops`) | 3 |
| `blocks` | `M` | 1 |
| `values` | constants `1..V` | 3 |
| `syncs` | `K`; each is a before/after pair on two threads or an `at` barrier on 2+ threads | 0 |
| `relations` | allowed sync kinds, `pair,at` | both |
| `p_read` | chance that an operation is a read | 0.5 |
| `p_obs` | chance that a read's result is given | 0 |
| `p_copy` | chance that a write copies an earlier unobserved read (if one exists) | 0 |
| `min_given` | with `p_obs > 0`, the least number of given results | 1 |
| `min_copies` | the least number of writes that copy a read | 0 |
| `adversarial` | 1: ask the locations with the most traps (§2) | 0 |
| `mixed` | 1: every thread both reads and writes, at least half the threads start with a write, and every block is written at least once and used by at least two threads | 0 |
| `max_queries` | asked locations, 1..this | 3 |
| `min_answers`, `max_answers` | accepted answer-set size | 12, 99 |

Given results shrink the answer set, so the answer-size filter favours seeds where no read
happens to be given. Without `min_given`, a `g3` problem can end up with no given result.
The problems generated before this rule record `min_given: 0`. Copies are thinned out the
same way: a copy repeats a value, which shrinks the answer set. A write can also copy only
if its thread has read something earlier. So `c8` alone gives 0–3 copies per problem;
`min_copies` sets a floor. Random traces can also be logically weak: a thread of only reads
or only writes, or a block that one thread uses alone. `mixed` rejects those.

`min_given`, `min_copies` and `mixed` are **selection rules**: they only reject seeds and never
change a draw. An accepted seed gives the same trace with or without them, so they are not
part of the name. The report lists them for each problem as "selected".

**Names.** A problem is named `<parameters>-<case>`. The parameter part is
`t<threads>op<ops>b<blocks>v<values>`, followed by `s<syncs>`, `g<p_obs>`, `c<p_copy>`,
`r<p_read>` and `x` (adversarial) when they are nonzero or not the default. Probabilities are in tenths. `s` takes
a suffix `p` (pairs only) or `a` (barriers only) when `relations` is restricted. The case
number counts problems with the same parameters (`01`, `02`, …). The seed is recorded in
`problem.json`.

**Seeds.** Each parameter set starts its seed search at a seed derived from its name.
Neighbouring sets that start from the same seed draw the same operations, so `g3` and
`g6` would otherwise share skeletons. Each new case continues after the seeds its
earlier cases used. Example: `t2op4b2v3s1pg3c5-01`.

## 4. Protocol

- **Prompt.** `prompts/v<N>.md` holds the rules, a toy example and the answer
  format. The instance is pasted in at `{instance}`. The prompt is short enough for a
  person to type. It names no technique. A prompt version is frozen once any attempt
  has used it.
- **One shot, no tools.** Each run is
  `claude -p --model <m> --effort <e> --tools "" --setting-sources ""`, started from an
  empty temporary directory with a one-line system prompt. The model sees only the
  prompt and a short environment block (date, working directory, model name).
- **Plan.** Each problem is run on Fable ×1 and on Opus, Sonnet and Haiku ×3, starting
  at effort `low`. The CLI cannot turn thinking off, so `low` is the lowest effort
  available. Higher efforts come later.
- **Grading.** The rows of the last `BEGIN … END` block, compared as a set with the
  truth: exact, missing and extra counts, and Jaccard similarity.
- **Ladder.** Start from 2 threads, one block and no sync. Add one dimension at a time
  (ops, blocks, given results, copies, sync pairs, barriers, sync inside operations,
  threads) until models break.
