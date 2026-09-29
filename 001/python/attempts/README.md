# attempts — one-shot model attempts

Each directory is one model's one-shot attempt at one task, written under the protocol in
the root `AGENTS.md` ("Model tests"):
- **file tools only:** the model runs no code and writes no tests;
- **closed book:** no web access;
- **spec-only prompt:** no algorithm names or hints;
- **independent:** the model sees no earlier attempt, including its own.

The task given to every model attempting `<kind>_<case>` is the same, from a frozen,
versioned bundle `python/tasks/v<N>/`:
- `prompt.md`, the template;
- `common.md`;
- `<kind>_<case>.md`;
- the spec version the bundle names (`001/spec/v<N>.md`).

Each attempt directory also holds two files written by the orchestrator, not the model:
- `PROMPT.md`: the exact prompt sent;
- `attempt.yaml`: task, model, trial, bundle and spec versions, the harness commit,
  conditions, and the audit and grade results.

Attempts are graded only by the harness:

```sh
python3 -m harness grade --plugin attempts.<dir> [--budget full] -o report.yaml
python3 -m harness.grade.transcript <agent-transcript.jsonl> attempts.<dir>   # protocol audit
```

An attempt whose transcript shows a shell, web or agent tool, a read outside its task's
allowed files, or a write outside its directory is discarded.

## Names

- **Directory:** `<kind>_<case>_<model><version>_<trial>/`, where
  - `kind` is `linear` (enumerators, counters) or `solver`;
  - `case` is `b` (base), `s` (base + sync), `o` (observed reads) or `so` (both);
  - `model` is e.g. `opus55` (Opus 5.5) or `fable51` (Fable 5.1);
  - the trial starts at `1`.
- **Registered algorithm names:** `<model><version>_<trial>-<case>-<short>`, e.g.
  `opus55_1-so-split`.

Each attempt contains its code and a `SOURCES.md`. For every algorithm, `SOURCES.md` says
whether it came from the model's memory (with the reference it had in mind), its own
derivation, or an adaptation.

## Planned attempts

| Kind | Case | Opus 5.5 | Fable 5.1 |
|------|------|----------|-----------|
| linear | b | `linear_b_opus55_1` | `linear_b_fable51_1` |
| linear | s | `linear_s_opus55_1` | `linear_s_fable51_1` |
| linear | o | `linear_o_opus55_1` | `linear_o_fable51_1` |
| linear | so | `linear_so_opus55_1` | `linear_so_fable51_1` |
| solver | b | `solver_b_opus55_1` | `solver_b_fable51_1` |
| solver | s | `solver_s_opus55_1` | `solver_s_fable51_1` |
| solver | o | `solver_o_opus55_1` | `solver_o_fable51_1` |
| solver | so | `solver_so_opus55_1` | `solver_so_fable51_1` |

None exist yet. Grades go in `REPORT.md` in this directory.

## `_archive/`

- `round1_4/` holds the four earlier comparison rounds. That code was self-tested by the
  models, written with prompts that named candidate algorithms, and done without
  source logs, so it does not meet the current protocol.
- Graded by the harness, all 32 of its algorithms pass on correctness.
- Two of its implementation files break the current import policy:
  - `linear_fable51_1/obs/common.py` uses the oracle `is_feasible`;
  - `linear_fable51_1/obs/dp.py` uses the reference DP counter.
