# Task `loopsol`, case `b`

**Setups:** loop setups (spec §8) with no sync points (spec §6). Actions are reads and writes, and
write data may depend on earlier reads (spec §4, §8).

**Build:** a solver that computes, exactly, `Poss_n(r)` for every read `r` of the loop
setup and `Poss_n(b)` for every block `b` (spec §5, §7), for any `n ≥ 1`. For a body read,
`Poss_n(r)` is the union over its `n` instances.

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
- **Exactly one solver:** a subclass of `harness.loop.api.LoopSolver`.
  - `capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)`, from
    `harness.capabilities`.
  - `solve(setup, n)` returns a `harness.loop.api.LoopOutcomes`:
    - `results`: a map from every read id of the loop setup to a set of terms;
    - `final`: a map from every block to a set of terms.
- **`SOURCES.md`**, and an `__init__.py` that imports your modules (see
  `tasks/v3/common.md`).

Decorate the class with `@register` from `harness.registry`.

## Grading

Your solver is graded on cases b:
- exact sets on many setups, for small and for large `n`;
- the largest `n` handled within the time limit.
