# contrib — model-written algorithms

This directory holds algorithms written by AI models against the `abio` APIs, one
directory per **kind × model × trial**:

```
<kind>_<model><version>_<trial>/      e.g. linear_opus55_1, linear_fable51_1, solver_opus55_1
    base/        base problem, no sync          names <model><version>-b-*
    base_sync/   base problem, sync             names <model><version>-s-*
    obs/         observed reads, no sync        names <model><version>-o-*
    obs_sync/    observed reads, sync           names <model><version>-so-*
```

- **kind:** `linear` means linearization enumerators and counters (`abio/lin/api.py`);
  `solver` means possibility-set solvers (`abio/solve/api.py`).
- **model and version:** `opus55` is Opus 5.5, `fable51` is Fable 5.1.
- **trial:** always appended, starting at `_1`. A rerun of the same task is `_2`, and so
  on.

The four cases are the base problem crossed with observations and with sync:

- **Base problem:** reads and writes; write data is a constant, unknown `"*"`, or an
  expression over earlier reads and writes of the same thread (`r1~7`); no observed
  results.
- **Observed:** the base problem plus some observed read results. Observations only ever
  remove linearizations and values.
- **Sync:** `before`/`after`/`at` sync points, added to either of the above.

Everything here is a plugin, loaded with `--plugin contrib.<dir>` (a whole directory) or
`--plugin contrib.<dir>.<case>`. Parsing stays in `abio`: contributed code receives
already-parsed `Setup` objects and never reads files.

## What exists

| Case | `linear_opus55_1` | `linear_fable51_1` | `solver_*` |
|---|---|---|---|
| base (`b`) | `base/` | `base/` | **missing** |
| base + sync (`s`) | `base_sync/` | `base_sync/` | **missing** |
| observed (`o`) | `obs/` | `obs/` | **missing** |
| observed + sync (`so`) | **missing** | **missing** | **missing** |

The only solver today is the core `brute` oracle (`abio/solve/brute.py`), which covers
all four cases.

- **The `obs/` enumerators also cover the base case.** With no observations they list
  all of `Lin(P)`, so they are a second base implementation (verified against
  `backtrack`).
- **The `base*/` enumerators accept read-dependent data**, because without observations
  data never affects `Lin(P)`.

## Algorithms

Enumerators unless marked *(counter)*. The "Fidelity" column says how closely an
algorithm follows published work:

- **As published:** a textbook algorithm, used unchanged apart from mapping a
  linearization to or from its sequence of thread labels.
- **Adapted:** a published algorithm, with its core rule or setting changed.
- **New:** the model's own construction; correctness rests on its argument plus
  differential tests against the oracle.

### base (`b`)
| Name | File | Idea | Fidelity |
|---|---|---|---|
| `opus55-b-lex` | `linear_opus55_1/base/enumerators.py` | Knuth 7.2.1.2 Algorithm L on the thread word | As published |
| `opus55-b-coollex` | same | Williams cool-lex, loopless | As published |
| `opus55-b-vr` | same | Varol–Rotem specialised to chains (fastest of its round) | As published |
| `opus55-b-neargray` | same | own construction: 1 adjacent swap or 1 two-place move per step | New |
| `opus55-b-multinomial` *(counter)* | same | multinomial coefficient | As published |
| `fable51-b-lex` | `linear_fable51_1/base/lex.py` | Narayana next-permutation | As published |
| `fable51-b-coollex` | `.../base/coollex.py` | Williams cool-lex on a linked list | As published |
| `fable51-b-unrank` | `.../base/unrank.py` | multinomial unranking; `start`/`stop`/`step` | As published |
| `fable51-b-gray` | `.../base/gray.py` | SJT over threads plus Chase-style lists; 1–2 swaps per step | New |
| `fable51-b-count` *(counter)* | `.../base/unrank.py` | multinomial coefficient | As published |

### base + sync (`s`)
| Name | File | Idea | Fidelity |
|---|---|---|---|
| `opus55-s-vr` | `linear_opus55_1/base_sync/enumerators.py` | Varol–Rotem on the general poset | As published |
| `opus55-s-pr` | same | Pruesse–Ruskey, reconstructed from memory; ≤ 2 swaps per step | As published (not transcribed) |
| `opus55-s-tree` | same | reverse-search family tree; ≤ 3 swaps per step | Adapted |
| `opus55-s-seg` | same | product over segments between barrier cuts | Adapted |
| `opus55-s-segcount` *(counter)* | same | per-segment DP product | Adapted |
| `fable51-s-vr` | `linear_fable51_1/base_sync/vr.py` | Varol–Rotem (fastest of its round) | As published |
| `fable51-s-pr` | `.../base_sync/pr.py` | Pruesse–Ruskey, from Ruskey's book (fetched from the web) | As published |
| `fable51-s-tree` | `.../base_sync/tree.py` | Ono–Nakano-style family tree, own parent rule | Adapted |
| `fable51-s-dp` | `.../base_sync/dp.py` | down-set positions DP, rank/unrank | As published |
| `fable51-s-cut` | `.../base_sync/cut.py` | cut segments, Pruesse–Ruskey per segment, with a cache | Adapted |
| `fable51-s-count` *(counter)* | `.../base_sync/dp.py` | per-segment DP product | Adapted |

### observed (`o`)
Both models' feasibility theory is in the module docstrings: `linear_opus55_1/obs/core.py`
(cluster theorem plus term-matching closure) and `linear_fable51_1/obs/common.py`
(data-flow components, class abstraction, and slot and automaton criteria). Each exposes
`is_feasible_fast(setup, order)`.

| Name | File | Idea | Fidelity |
|---|---|---|---|
| `opus55-o-filter` | `linear_opus55_1/obs/enumerators.py` | Varol–Rotem plus exact fixed-L test (`--opt pins=1`: static pins) | enumeration published, filter New |
| `opus55-o-prune` | same | prefix DFS, stored witness reused | New |
| `opus55-o-memo` | same | prune plus a dead-state memo | New |
| `opus55-o-split` | same | branch on precedence pairs; accept or drop whole sub-posets (fastest) | New |
| `opus55-o-splitcount`, `opus55-o-dpcount` *(counters)* | same | split partition / state DP | New |
| `fable51-o-filter` | `linear_fable51_1/obs/filter.py` | Pruesse–Ruskey plus per-component re-test | enumeration published, filter New |
| `fable51-o-prune` | `.../obs/prune.py` | prefix DFS with reads-from criterion | New |
| `fable51-o-auto` | `.../obs/auto.py` | incremental component automaton plus lookahead | New |
| `fable51-o-dp` | `.../obs/dp.py` | DP over (down-set, automaton state), zero dead ends, rank/unrank | New |
| `fable51-o-count` *(counter)* | `.../obs/dp.py` | same DP | New |

## Dependencies

- Only one contributed module imports another package:
  `linear_fable51_1/obs/filter.py` uses `linear_fable51_1/base_sync/pr.py`.
- Importing a top-level directory (e.g. `contrib.linear_fable51_1`) registers all of its
  cases.
- Nothing active imports `_archive/`.

## `_archive/`

This directory holds superseded work that is not loaded by default.

- `_archive/opus_obs/` and `_archive/fable_obs/` are from comparison round 3:
  observations with **constant data only**, now superseded by `obs/`.
- They keep their original names (`opus-o-*`, `fable-o-*`), so nothing clashes with
  the active code.
- Their imports point at the new paths, so `--plugin contrib._archive.opus_obs` still
  loads.
- They are correct only for constant data, but the CLI no longer checks for
  read-dependent data. Run them only on constant-data setups; their own tests do.

## Running

From `python/`:

```sh
python3 -m abio lin list --plugin contrib.linear_opus55_1           # what a directory registers
python3 -m abio lin enum examples/base.setup.yaml --plugin contrib.linear_fable51_1 \
        --algo fable51-s-vr --count-only                            # 924
ulimit -v 2000000; python3 -m unittest contrib.linear_opus55_1.obs.test_opus_dep   # 35 s – 4 min per suite
```

The history of how this code was produced, with benchmarks, is in [`REPORT.md`](REPORT.md).
