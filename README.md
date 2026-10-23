# studyroom

This repository tests the performance of AI models: what they can and cannot get right,
and what kinds of problem make them fail. Each study is one such test, built around a
problem family; so far, multi-threaded reads and writes (which global orders of the
steps are possible, and which values each read can return).

## Categories

Every study belongs to one or both of these categories, and states it at the top of its
`README.md`:

| Category | The model … | Graded by |
|----------|-------------|-----------|
| **LLM coding performance test** | writes code for a problem from its specification and the interface to implement, in one shot, with file tools only and no execution | our harness, which runs the code against oracles on generated and adversarial instances |
| **LLM response performance test** | answers one problem instance directly, in one reply, with no tools at all | our harness, which compares the answer with exact ground truth |

Neither kind of prompt contains hints or names known algorithms. A coding test records
whether each idea came from the model's memory or its own derivation. A response test
records the effort setting and the thinking used.

To grade models we need exact answers, so a study also does the supporting work: it
surveys the known algorithms, and writes reference implementations, oracles and
generators. That work lives in the study's **harness**, our code per language. The model
output lives in **attempts**. Coding attempts sit under their language's directory;
response attempts and other language-independent data sit at the study level.

## Studies

Start with a study's `README.md`.

| Study | Category | What |
|-------|----------|------|
| [`001/`](001/README.md) | LLM coding performance test | Trace analysis for asynchronous multi-threaded block I/O: models write linearizers and solvers; problem documents, algorithm survey, Python reference implementation and oracles |
| [`002/`](002/README.md) | LLM response performance test | Deducing the outcomes of such a trace: models list every possible combination of asked values, with no tools; graded against an exact solver and an enumerator |

Agent guidance, including the protocol for both categories, is in `AGENTS.md`.
