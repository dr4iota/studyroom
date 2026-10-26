# Agent guidance — studyroom

Research studies, one directory per study (`001/`, `002/`, …). `CLAUDE.md` and
`GEMINI.md` are symlinks to this file; keep the guidance tool-agnostic.

This is a shared workspace: several people and agents work on different studies.
Guidance here applies to every study. Anything specific to one study belongs in that
study's own documents.

## Study conventions

Every study is a performance test of AI models (see the root `README.md`). Each study is
self-contained, and its `README.md` states its category in a line under the title
(e.g. `**Category: LLM coding performance test.**`):
- **LLM coding performance test** ("coding test" below): models write code for the
  problem (§ Model tests);
- **LLM response performance test** ("response test" below): models answer instances
  of the problem directly (§ Model tests).

A study may be both. The algorithm study, reference code, oracles and generators a test
needs are supporting work, kept in the study's harness. The layout:

| Path | What |
|------|------|
| `README.md` | What the study is, its category, reading order, status and how to run the checks. |
| `*.md` at the top | The problem documents: definitions, formats, surveys, plans. |
| `python/`, `rust/`, … | Our code per language: the harness, and the coding attempts written in that language. |
| `problems/`, `prompts/`, `attempts/`, … at the top | Data that no language owns: generated problems, prompt templates, response attempts, reports. |

- Every implementation of a study reads and writes the same on-disk formats,
  so any implementation can be checked against any other.
- The harness normally lives in `<lang>/harness/`. A study whose code serves only to
  generate and check problems may keep it in one source file under `<lang>/`.
- Put a new language in its own sibling directory (`rust/`, `cpp/`, …).
- Add each new study to the table in the root `README.md`, with its category.

## Python

- Python 3.10 or newer; keep dependencies minimal (a study's `pyproject.toml`
  lists them).
- Tests use `unittest` (pytest is not assumed to be installed).
- Parsing and validation live in the study's core library. Other code, including
  plugins, receives parsed objects and never parses files itself.

## Rust

- One Cargo workspace per `rust/` directory. Commit `Cargo.lock`.
- Before committing: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`
  and `cargo test`.

## Model tests

A model test finds what a model can and cannot get right **in one shot, by itself**. The
prompt must not do the work for it, and the model must not test its own work. There are
two categories:
- a **coding test**: the model writes code, and the harness runs and grades it;
- a **response test**: the model answers a problem instance in text, and the harness
  grades the answer against exact ground truth.

### Rules for both categories

**Roles.**
- **Harness:** written by us. It holds the spec in code, the reference implementation,
  the oracles and the grader; for a response test, also the problem generator.
- **Attempt:** one model's one-shot output for one task, graded only by the harness.
- **Orchestrator:** the parent model or a person. It writes the prompt, runs the models
  and the grader, and writes the report. Only the orchestrator executes code.

**Closed book.** No web access. The model works from its memory and its own derivation.

**Independence.** Each attempt starts from nothing. A model sees no earlier attempt,
including its own, no other model's output and no report.

**What the prompt may contain:** the problem specification (the relevant definitions
from the study's documents) and the case or instance being tested; what to produce and
in what form.

**What it must not contain:**
- names of algorithms, papers or techniques;
- hints about structure ("exploit barriers", "the lemma may break");
- results from earlier attempts or other models;
- the grader, its instances or their answers.

**Versions.** Prompt material is versioned. Once any attempt has used a version, it is
frozen: a change makes `v<N+1>`. Every attempt records the exact prompt it was given and
its conditions: model, trial, prompt version, harness commit, and settings such as effort.

**Archive.** Superseded work moves to `_archive/` beside it instead of being deleted.

### Coding tests

**One shot, no execution.** The model gets file tools only (read, write, edit, search).
It cannot run code, tests or commands, and it writes no tests: all testing belongs to the
harness.
- Use a restricted agent type for this; `.claude/agents/oneshot-coder.md` gives
  Read/Write/Edit/Glob/Grep only.
- If a restricted type is unavailable, the prompt forbids execution, and the
  orchestrator audits the transcript (e.g. 001's `python -m harness.grade.transcript`).
  An attempt is discarded if it:
  - used a web or agent tool;
  - read outside its allowed files;
  - wrote outside its directory;
  - ran a shell command other than a minor one.
- A **minor** shell call is read-only inspection (`ls`, `cat`, `head`, `wc`, `find`, …)
  of paths inside the attempt's own directory only. It reveals nothing about the problem,
  so it is recorded (`TOOL-MINOR`) but does not discard the attempt.

**Sources.** The model writes `SOURCES.md` in its directory, and for each algorithm
records one of:
- from memory, with the reference it has in mind;
- its own derivation;
- adapted from something it recalls, saying what changed.

**Task documents.** Every model attempting the same task gets the same prompt, which
points to the same documents:
- the study's hint-free spec;
- the language's shared rules (`<lang>/tasks/common.md`);
- one task file per kind and case (`<lang>/tasks/<kind>_<case>.md`).

Only the attempt directory and the name prefix differ between models. The prompt may
also give the interface to implement (API files, registration, capability flags), the
import policy, where to write, and the list of files the model may read.

**Bundles.** The prompt material is a versioned bundle, `<lang>/tasks/v<N>/`, holding the
prompt template, `common.md` and the task files, and `bundle.yaml`, which names the spec
version (`spec/v<N>.md`) and lists the allowed reads. Before launching, the orchestrator
writes `PROMPT.md` (the exact prompt) and `attempt.yaml` (task, model, trial, bundle,
spec, harness commit, conditions) into the attempt directory (001:
`python -m harness.grade.prepare`).

**Grading.** The harness grader (001: `python -m harness grade --plugin attempts.<dir>`)
checks:
- the import policy: attempts may use only the data model and APIs, never reference
  code or oracles;
- correctness on every case the algorithm's capabilities cover, against the oracles,
  on generated instances and a fixed adversarial suite, under time and memory limits;
- throughput.

A crash, a timeout or an import error is a failure.

**Layout and names.** A coding attempt belongs to its language:
`<lang>/attempts/<kind>_<case>_<model><version>_<trial>/`, e.g.
`python/attempts/linear_so_opus55_1/`.
- `kind` and `case` are defined by the study (001: `kind` is `linear` or `solver`;
  `case` is `b`, `s`, `o` or `so`). The trial starts at `1`.
- Registered algorithm names: `<model><version>_<trial>-<case>-<short>`, e.g.
  `opus55_1-so-split`, so any set of attempts can be loaded together.
- The study's `<lang>/attempts/README.md` lists the attempts; `<lang>/attempts/REPORT.md`
  records the grades.

### Response tests

**One shot, no tools.** The model gets no tools at all: no files, no shell, no code
execution, no web. It answers from the prompt alone, in one reply.
- Run it with every tool disabled, from an empty temporary directory, so that no project
  file can reach it (e.g. `claude -p --model <m> --effort <e> --tools ""
  --setting-sources ""` with a one-line system prompt).
- Check the recorded response: one turn, no tool or server-tool use. Any code in the
  reply is text the model traced by itself.

**Ground truth.** The harness computes the exact answer with two independent methods
(e.g. a solver and an exhaustive enumerator). They must agree on every problem. A
disagreement stops generation and is reported before any model sees the problem.

**Problems.** The harness generates instances from parameters and a seed, and stores
each one with its parameters, seed and truth, so it can be rebuilt exactly. Selection
rules that only reject seeds keep a problem reproducible from its seed. Rules that
change the instance (e.g. which questions are asked) are part of its name.

**Answers.** The prompt fixes a machine-readable answer block. The grader compares it
with the truth exactly (for a set: every element and nothing more) and records the
missing and the extra items. An unreadable answer is a failure.

**Model versions.** Request each model by its exact versioned ID, not by an alias that
can move to a newer release, and record in every attempt the model ID that answered and
the version of the client used to call it. Compare models only on attempts made with the
same IDs.

**Trials and effort.** One trial is noisy. Run each model several times per problem
(at least 3; about 9 to compare models), and record the effort setting and the thinking
tokens used. The same effort setting can mean very different thinking budgets for
different models.

**Layout.** Response attempts are not code, so they live at the study level:
- `prompts/v<N>.md`: the prompt template;
- `problems/<name>/`: one problem and its truth;
- `attempts/<name>/prompt-v<N>.txt`: the exact prompt, stored once per problem and
  version;
- `attempts/<name>/<model>-<effort>-<trial>/`: one run (the reply, the raw response,
  the run record and the grade). `<model>` carries the model's version, e.g. `opus55`,
  so runs of different versions never share a name.

## Resource safety

Enumeration problems here grow exponentially, and one run has already crashed the
machine by materializing millions of results.

- Run heavy commands under a memory cap and a timeout, e.g.
  `ulimit -v 2000000; timeout 300 python3 ...`.
- Check a count before enumerating; stream results and never `list()` a large
  enumeration.
- Stop benchmarks on a wall-clock limit as well as an output limit.
- Run at most **two** model attempts at a time (agents or CLI calls); start the next as
  one finishes.
- Grade **one coding attempt at a time** (001's grader caps itself at 2 GB); check free
  memory before starting heavy runs.

## Commit conventions

- Prefix: `<study>: <imperative summary>` (e.g. `001: add solver API`), or `repo:`
  for root-level changes. Keep each commit to one study.
- Keep messages short. Say what the commit contains, without technical details: a
  single line, or a line plus a few more. Details belong in the study's documents.
- Commit related changes together. Don't leave a trail of corrections and fix-ups;
  nobody needs the wrong intermediate versions.
- Before pushing, squash commits to remove incorrect intermediate code or text.
  Don't rewrite history that has already been pushed.
- Run the study's tests before committing; all must pass.
