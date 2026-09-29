# 001 — Trace analysis for asynchronous multi-threaded block I/O

Threads issue asynchronous reads and writes on storage blocks, optionally coupled by
sync points. Given such a trace, the study asks:

- Which global orders of the steps are possible (the linearizations)?
- Exactly which values can each read have returned, and which contents can each
  block end with? The answer must be "no more, no less".
- How do partially observed read results narrow both?

## Reading order

1. [`premise.md`](premise.md): the problem class, definitions and sub-problems.
2. [`formats.md`](formats.md): the on-disk documents every implementation shares.
3. [`surveys.md`](surveys.md): related work.
4. [`visions.md`](visions.md): what could be built and studied.

## Layout

| Path | What |
|------|------|
| `python/` | Reference implementation, package `abio`: model, formats, generator, linearization and solver APIs, brute-force oracle, CLI. See [`python/README.md`](python/README.md). |
| `python/contrib/` | Linearizers written by Fable 5.1 and Opus 5.5. See [`contrib/README.md`](python/contrib/README.md) for the directory map and [`contrib/REPORT.md`](python/contrib/REPORT.md) for the model comparison. |
| `rust/` | Not started. |

## Status

The work is split into four cases:
- **base:** reads and writes; write data is a constant, unknown, or depends on earlier
  reads of the same thread.
- **observed:** some read results are known.
- Each of the two comes with and without sync.

| Case | Linearizers | Solvers |
|------|-------------|---------|
| base | core, plus two model implementations | `brute` oracle only |
| base + sync | core, plus two model implementations | `brute` oracle only |
| observed | core oracle, plus two model implementations | `brute` oracle only |
| observed + sync | core oracle only | `brute` oracle only |

## Checks

From `python/`, under a memory cap (enumerations grow exponentially):

```sh
ulimit -v 2000000
(cd tests && python3 -m unittest)                         # core: 31 tests
python3 -m unittest contrib.linear_opus55_1.obs.test_opus_dep   # each contrib suite, 35 s – 4 min
```

Last run: core 31, active contrib suites 84, archived suites 33; all pass.
