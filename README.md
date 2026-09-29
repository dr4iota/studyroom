# studyroom

Research studies, one directory per study. The studies have two purposes:

1. **Algorithms.** Study existing algorithms for a family of combinatorial problems
   around multi-threaded reads and writes: which global orders of the steps are possible,
   and which values each read can return. Where the literature stops, look for new
   directions and results.
2. **Model testing.** Test AI code-generation models on these problems, to find out what
   kinds of problem make them fail. A model gets only the problem specification and the
   interface to implement, not hints or known algorithms. Its output is graded against a
   brute-force oracle. We record whether each result came from the model's memory, from
   web sources it looked up, or from its own derivation.

Each study has problem documents (definitions, formats, surveys, plans) and, per
language (Python, Rust), two parts that share the same on-disk formats:
- **`harness/`**: our code. It holds the data model and APIs, the reference
  implementation, the oracles and the grader.
- **`attempts/`**: model output, one directory per one-shot attempt. Attempts are graded
  only by the harness.

Start with a study's `README.md`.

| Study | What |
|-------|------|
| [`001/`](001/README.md) | Trace analysis for asynchronous multi-threaded block I/O: problem documents, Python reference implementation, archived model-written linearizers (round 1–4) |

Agent guidance, including the protocol for model tests, is in `AGENTS.md`.
