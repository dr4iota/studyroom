# Task `looplin`, case `b`

**Setups:** loop setups (spec §8) with no sync points (spec §6). Actions are reads and writes, and
write data may depend on earlier reads (spec §4, §8).

**Build:** a counter of `|Lin(P_n)|` (spec §3, §7): the exact number of linearizations of
the unrolled trace poset, for any `n ≥ 1`.

## Files you may read

- `001/spec/v3.md`: the problem;
- `001/python/tasks/v3/common.md`: the rules for all tasks;
- this file;
- `001/python/harness/model.py`, `poset.py`, `terms.py`, `capabilities.py`,
  `registry.py`: the data model;
- `001/python/harness/loops.py`: loop setups;
- `001/python/harness/loop/api.py`: the loop API.

## Input

`setup` is a `harness.loops.LoopSetup` (spec §8), with these fields:
- `blocks`, `sync_points` (`K`), `loop_sync_points` (`Kb`);
- `init`: a term per block;
- `threads`: `LoopThread` objects, each with `id` and the step lists `prefix`, `body`
  and `suffix`. Each step is a `harness.model.Step`.
- `actions`: a map from action id to `LoopAction`, with fields `kind` (`read` or
  `write`), `block`, `thread`, `segment` (`prefix`, `body` or `suffix`) and `data` (an
  expression for writes).

`setup.unroll(m)` builds the ordinary `harness.model.Setup` for `P_m`.
`n` is an `int ≥ 1` and may be arbitrarily large.

## What to deliver

In your attempt directory:
- **Exactly one counter:** a subclass of `harness.loop.api.LoopCounter`.
  - `capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)`, from
    `harness.capabilities`.
  - `count(setup, n)` returns `|Lin(P_n)|` as an exact Python `int`.
- **`SOURCES.md`**, and an `__init__.py` that imports your modules (see
  `tasks/v3/common.md`).

Decorate the class with `@register` from `harness.registry`.

## Grading

Your counter is graded on cases b:
- exact answers on many setups, for small and for large `n`;
- the largest `n` handled within the time limit.
