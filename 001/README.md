# 001 — Trace analysis for asynchronous multi-threaded block I/O

**Category: LLM coding performance test.**

Threads issue asynchronous reads and writes on storage blocks, optionally coupled by
sync points. Given such a trace, the study asks:

- Which global orders of the steps are possible (the linearizations)?
- Exactly which values can each read have returned, and which contents can each
  block end with? The answer must be "no more, no less".
- How do partially observed read results narrow both?

Models write code that answers these questions; their attempts live under
`python/attempts/` and are graded by the harness. To grade them, the study surveys the
known algorithms and builds a reference implementation and oracles.

## Reading order

1. [`premise.md`](premise.md): the problem class, definitions and sub-problems.
2. [`formats.md`](formats.md): the on-disk documents every implementation shares.
3. [`surveys.md`](surveys.md): related work.
4. [`visions.md`](visions.md): what could be built and studied. Its "Terms" section defines
   every notion used here (`Lin(P)`, `LinFeas(P)`, `Poss(r)`, joint possibility, the four
   cases), and §10 lists open problems for testing AI models.

## Layout

| Path | What |
|------|------|
| `python/harness/` | Our code, package `harness`: data model, formats, generator, linearization and solver APIs, brute-force oracles, grader, CLI. See [`python/README.md`](python/README.md). |
| `python/attempts/` | One-shot model attempts, graded by the harness. See [`attempts/README.md`](python/attempts/README.md). |
| `python/attempts/_archive/round1_4/` | Earlier model-written linearizers (four rounds, self-tested, with hinted prompts), and their comparison report. |
| `rust/` | Not started. |

## Status

The work is split into four cases:
- **base:** reads and writes; write data is a constant, unknown, or depends on earlier
  reads of the same thread.
- **observed:** some read results are known.
- Each of the two comes with and without sync.

| Case | Harness linearizers | Harness solvers | Graded attempts |
|------|---------------------|-----------------|-----------------|
| base (`b`) | `backtrack`, `dp-positions` | `brute` | round 5: 2 models, linear + solver ([report](python/attempts/REPORT.md)) |
| base + sync (`s`) | `backtrack`, `dp-positions` | `brute` | round 5: 2 models, linear + solver ([report](python/attempts/REPORT.md)) |
| observed (`o`) | `backtrack-feasible`, `enum-count` | `brute` | round 5: 2 models, linear + solver ([report](python/attempts/REPORT.md)) |
| observed + sync (`so`) | `backtrack-feasible`, `enum-count` | `brute` | round 5: 2 models, linear + solver ([report](python/attempts/REPORT.md)) |

## Checks

From `python/`:

```sh
ulimit -v 3000000
(cd tests && python3 -m unittest)                          # harness: 33 tests
python3 -m harness grade --plugin attempts.<dir>           # grade an attempt; exit 0 iff all pass
```

The grader caps its own memory (`--mem-mb`, default 2000) and time per call (`--seconds`).
