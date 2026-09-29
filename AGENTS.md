# Agent guidance — studyroom

Research studies, one directory per study (`001/`, `002/`, …). `CLAUDE.md` and
`GEMINI.md` are symlinks to this file; keep the guidance tool-agnostic.

## Study conventions

Each study is self-contained, with the same layout:

| Path | What |
|------|------|
| `README.md` | What the study is, reading order, status and how to run the checks. |
| `*.md` at the top | The problem documents: definitions, formats, surveys, plans. |
| `python/harness/`, `python/attempts/` | The Python harness (our code) and model attempts. |
| `rust/harness/`, `rust/attempts/` | The same for Rust, when there is one. |

- Every implementation of a study reads and writes the same on-disk formats,
  so any implementation can be checked against any other.
- Put a new language in its own sibling directory (`rust/`, `cpp/`, …).
- Add each new study to the table in the root `README.md`.

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
prompt must not do the work for it, and the model must not test its own work.

**Roles.**
- **Harness:** written by us. It holds the spec in code, the data model and APIs, the
  reference implementation, the oracles and the grader. It lives in `<lang>/harness/`.
- **Attempt:** one model's one-shot output for one task. It lives in
  `<lang>/attempts/<dir>/` and is graded only by the harness.
- **Orchestrator:** the parent model or a person. It writes the prompt, runs the grader
  and writes the report. Only the orchestrator executes code.

**One shot, no execution.** The attempting model gets file tools only (read, write,
edit, search). It cannot run code, tests or commands, and it writes no tests: all
testing belongs to the harness.
- Use a restricted agent type for this; `.claude/agents/oneshot-coder.md` gives
  Read/Write/Edit/Glob/Grep only.
- If a restricted type is unavailable, the prompt forbids execution, and the
  orchestrator audits the transcript (`python -m harness.grade.transcript`). An attempt
  is discarded if it:
  - used a web or agent tool;
  - read outside its allowed files;
  - wrote outside its directory;
  - ran a shell command other than a minor one.
- A **minor** shell call is read-only inspection (`ls`, `cat`, `head`, `wc`, `find`, …)
  of paths inside the attempt's own directory only. It reveals nothing about the problem,
  so it is recorded (`TOOL-MINOR`) but does not discard the attempt.

**Closed book.** No web access. Ideas come from the model's memory or its own
derivation. The model writes `SOURCES.md` in its directory, and for each algorithm
records one of:
- from memory, with the reference it has in mind;
- its own derivation;
- adapted from something it recalls, saying what changed.

**Task documents.** Every model attempting the same task gets the same prompt, which
points to the same documents:
- the study's hint-free spec;
- the language's shared rules (`<lang>/tasks/common.md`);
- one task file per kind and case (`<lang>/tasks/<kind>_<case>.md`).

Only the attempt directory and the name prefix differ between models.

**Versions.** The prompt material is a versioned bundle, `<lang>/tasks/v<N>/`, holding:
- the prompt template;
- `common.md` and the task files;
- `bundle.yaml`, which names the spec version and lists the allowed reads.

Once any attempt has used a bundle, it is frozen: a change makes `v<N+1>`, and the spec
likewise (`spec/v<N>.md`). Before launching, the orchestrator runs
`python -m harness.grade.prepare`. It writes `PROMPT.md` (the exact prompt) and
`attempt.yaml` (task, model, trial, bundle, spec, harness commit, conditions) into the
attempt directory, so every attempt records what it was given.

**What the prompt may contain:**
- the problem specification: the relevant definitions from the study's documents, and
  the case being tested;
- the interface to implement (API files, registration, capability flags), the import
  policy, and where to write;
- the list of files the model may read.

**What it must not contain:**
- names of algorithms, papers or techniques;
- hints about structure ("exploit barriers", "the lemma may break");
- results from earlier attempts or other models;
- the grader or its instances.

**Independence.** Each run is one (kind, case, model) and starts from nothing. A model
sees no earlier attempt, including its own, and no other model's code or the report.

**Grading.** The orchestrator runs `python -m harness grade --plugin attempts.<dir>`
(Python). It checks:
- the import policy: attempts may use only the data model and APIs, never reference
  code or oracles;
- correctness on every case the algorithm's capabilities cover, against the oracles,
  on generated instances and a fixed adversarial suite, under time and memory limits;
- throughput.

A crash, a timeout or an import error is a failure.

**Layout and names.**
- Directory: `attempts/<kind>_<case>_<model><version>_<trial>/`, e.g.
  `attempts/linear_so_opus55_1/`.
  - `kind` is `linear` (enumerators, counters) or `solver`.
  - `case` is `b`, `s`, `o` or `so`.
  - The trial starts at `1`.
- Registered algorithm names: `<model><version>_<trial>-<case>-<short>`, e.g.
  `opus55_1-so-split`, so any set of attempts can be loaded together.
- Superseded work moves to `attempts/_archive/` instead of being deleted.
- The study's `attempts/README.md` lists the attempts; `attempts/REPORT.md` records the
  grades.

## Resource safety

Enumeration problems here grow exponentially, and one run has already crashed the
machine by materializing millions of results.

- Run heavy commands under a memory cap and a timeout, e.g.
  `ulimit -v 2000000; timeout 300 python3 ...`.
- Check a count before enumerating; stream results and never `list()` a large
  enumeration.
- Stop benchmarks on a wall-clock limit as well as an output limit.

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
