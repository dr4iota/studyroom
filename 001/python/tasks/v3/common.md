# Rules common to all tasks (Python)

You are writing an **attempt**: code that the harness will import and grade once. Your
task file (`tasks/v3/<kind>_<case>.md`) says what to build. This file gives the rules every
task shares.

## Rules

- **You cannot run anything:** no programs, tests or commands. Get the code right by
  reading and reasoning. To see what is in a directory, use the file search tool (glob),
  not a shell.
- **No web access.** Work from the specification and your own knowledge.
- **Write no tests.** The harness does all testing.
- **Read only** the files your task file lists.
- **Write only** in your attempt directory, `001/python/attempts/<dir>/`. Your prompt
  gives `<dir>` and your name prefix.

## What you write

- **`__init__.py`**, which imports your modules so their `@register` decorators run. The
  grader loads your attempt with `import attempts.<dir>`.
- **Your modules.**
- **`SOURCES.md`.** For each algorithm, say where it came from:
  - from memory, with the reference you have in mind (author, title, year, as best you
    recall);
  - your own derivation;
  - an adaptation of something you recall, saying what you changed.

  Also note anything you were unsure about.

Register each algorithm with `name = "<prefix><short>"` (your prompt gives the prefix)
and a one-line `description`. Every algorithm you register is graded, and a wrong one
counts against you, so register only what the task asks for.

## Inputs you receive

Your code receives already-parsed objects; you never read files. Your task file describes
them.

## Import policy (checked statically; a violation fails the attempt)

- **Allowed:**
  - the Python standard library, except modules that execute programs or reach the
    network (`subprocess`, `socket`, `urllib`, `http`, `ctypes`, `multiprocessing`,
    `asyncio`, and similar);
  - your own package (relative imports are fine);
  - `harness.model`, `harness.poset`, `harness.terms`, `harness.capabilities`,
    `harness.registry`, `harness.lin.api`, `harness.solve.api`, `harness.loops`,
    `harness.loop.api`;
  - from `harness.semantics`, only `Schedule`;
  - from `harness.loop`, only `api` and the names it defines.
- **Not allowed:**
  - any other harness module;
  - other attempts;
  - third-party packages;
  - `open`, `exec`, `eval` and `__import__`.

## Grading and limits

- Your algorithms are tested on every case their declared capabilities cover, against
  exact reference answers, on many setups, including adversarial ones.
- Setups for correctness are small. Iteration counts range from 1 to very large.
- Each call has a time limit, 20 seconds by default, and the grader process is capped at
  about 2 GB of memory.
- A crash, a timeout, a wrong answer or a policy violation is a failure.
