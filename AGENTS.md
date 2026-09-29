# Agent guidance — studyroom

Research studies, one directory per study (`001/`, `002/`, …). `CLAUDE.md` and
`GEMINI.md` are symlinks to this file; keep the guidance tool-agnostic.

## Study conventions

Each study is self-contained, with the same layout:

| Path | What |
|------|------|
| `README.md` | What the study is, reading order, status and how to run the checks. |
| `*.md` at the top | The problem documents: definitions, formats, surveys, plans. |
| `python/` | The Python implementation. |
| `rust/` | The Rust implementation, when there is one. |

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

## Model-written code

Code written by AI models for comparison goes in the study's `contrib/`, one
directory per kind, model and trial: `<kind>_<model><version>_<trial>/`, e.g.
`linear_opus55_1`. The trial number always starts at `_1`. Superseded work moves
to `contrib/_archive/` instead of being deleted. The study's `contrib/README.md`
maps directories to cases.

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
