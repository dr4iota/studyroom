# Task `linear`, case `or`

**Setups:** no sync points (`K = 0`), observed results and RCW actions allowed (spec §6). Actions are reads, writes and RCWs (spec §1, §4). Write and
RCW data, and RCW expected values, may depend on earlier reads (spec §4).

**Build:** an enumerator of `LinFeas(P)`, as defined in spec §3 and §5. It must list every
feasible linearization, each exactly once, and nothing else. Observed results of reads
and of RCWs both restrict feasibility.

## Files you may read

- `001/spec/v2.md`: the problem;
- `001/python/tasks/v2/common.md`: the rules for all tasks;
- this file;
- `001/python/harness/model.py`, `poset.py`, `terms.py`, `capabilities.py`,
  `registry.py`: the data model;
- `001/python/harness/lin/api.py`: the linearization API.

## What to deliver

In your attempt directory:
- **Exactly one enumerator** (required): a subclass of `harness.lin.api.LinEnumerator`.
  - `capabilities = Capabilities(rcw=True, sync=False, observed_reads=True)`.
  - `enumerate(setup)` yields linearizations: tuples of node indices of `setup.poset`,
    earliest first.
  - Be lazy: the caller may stop early, so do not build the whole list first.
  - Be deterministic.
- **At most one counter** (optional): a subclass of `harness.lin.api.LinCounter`, with
  the same capabilities. `count(setup)` returns a `CountResult`:
  - `feasible`: `|LinFeas(P)|`, filled when the setup has observed results;
  - `linearizations`: `|Lin(P)|`, or `None`.
- **`SOURCES.md`**, and an `__init__.py` that imports your modules (see
  `tasks/v2/common.md`).

Decorate each class with `@register` from `harness.registry`. Leave `gray_code` False
unless every pair of consecutive outputs differs by exactly one swap of adjacent
positions.

## Grading

Your algorithms are graded on cases b, o, br, or, the cases your capabilities cover:
- the enumerator's output set must equal the reference set, with no duplicates and
  every output valid;
- the counter's numbers must equal the reference counts;
- throughput and the largest setups handled within the time limit are measured.
