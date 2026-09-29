# Task `solver`, case `br`

**Setups:** no sync points (`K = 0`), no observed results, RCW actions allowed (spec §6). Actions are reads, writes and RCWs (spec §1, §4). Write and
RCW data, and RCW expected values, may depend on earlier reads (spec §4).

**Build:** a solver that computes, exactly, `Poss(r)` for every read and every RCW `r`
(for an RCW, the old content it finds), `Poss(b)` for every block `b`, and whether the
setup is consistent (spec §5). There are no observed results, so every setup is consistent.

## Files you may read

- `001/spec/v2.md`: the problem;
- `001/python/tasks/v2/common.md`: the rules for all tasks;
- this file;
- `001/python/harness/model.py`, `poset.py`, `terms.py`, `capabilities.py`,
  `registry.py`: the data model;
- `001/python/harness/solve/api.py`: the solver API.

## What to deliver

In your attempt directory:
- **Exactly one solver:** a subclass of `harness.solve.api.Solver`.
  - `capabilities = SolverCapabilities(rcw=True, sync=False, observed_reads=False, modes=..., witnesses=...)`.
  - `modes` must include `"all"` (over all linearizations). Add `"fixed"` if you also
    support `solve(setup, linearization)` for one given `L`, which computes
    `Poss_L(r)` and `Poss_L(b)`.
  - `solve(setup, linearization=None)` returns an `Outcomes`, following the output
    contract in `solve/api.py`:
    - `results` has one entry per read id and per RCW id, and `final` one per block;
    - each entry is a set of terms.
- **Witnesses** (optional; set `witnesses=True` only if you return them): a list of
  `harness.semantics.Schedule` objects, one per (read or RCW, value) and per
  (block, value).
  - A `Schedule` is a dataclass, `Schedule(order, effects, results, final, consistent,
    meta)`:
    - `order`: a linearization;
    - `effects`: all action ids in effect order (spec §4);
    - `results`: read or RCW id to returned term;
    - `final`: a list of terms per block;
    - `consistent`: a bool;
    - `meta`: a dict.
  - Import it with `from harness.semantics import Schedule`. You may not read
    `semantics.py`; this description is its full interface.
  - `meta["certifies"]` is `{"id": r, "value": v}` or `{"block": b, "value": v}`,
    where `v` is the term as a document value: a bare constant as an int, anything else
    as its canonical string.
  - The grader re-executes every witness.
- **`SOURCES.md`**, and an `__init__.py` that imports your modules (see
  `tasks/v2/common.md`).

Decorate the class with `@register` from `harness.registry`.

## Grading

Your solver is graded on cases b, br, the cases your capabilities cover:
- in mode `"all"`, and in mode `"fixed"` if you declare it, the sets and the consistency
  verdict must equal the reference exactly;
- every witness you return must re-execute to what it certifies;
- the largest setups handled within the time limit are measured.
