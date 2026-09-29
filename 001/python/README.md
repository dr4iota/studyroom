# abio — Python reference implementation

This is the Python scaffold for the problem class in `../premise.md`, using the documents
of `../formats.md` (v2). Other languages go in their own sibling directories
(`../rust/`, `../cpp/`, …) and read and write the same documents, so any implementation
can be checked against any other.

Requirements: Python ≥ 3.10 and PyYAML. No install is needed:

```sh
cd python
python3 -m abio --help                       # or: pip install -e .  →  abio --help
(cd tests && python3 -m unittest)            # 31 tests, a few seconds
```

## Layout

| Path | Contents |
|---|---|
| `abio/terms.py` | Terms and expressions (`a~b`, non-commutative), parse/print canonical form, `substitute`, `seq` builder |
| `abio/model.py` | `Setup`, `Thread`, `Step`, derived `Action`; parsing and validation (formats.md §1 rules 1–5); `features()` |
| `abio/poset.py` | Trace poset (quotient by `at`), `Linearization = tuple[int, ...]`, VAL-LIN `check()` |
| `abio/semantics.py` | Atomic-register interpreter, effect-order check, brute-force full-schedule enumeration, `is_feasible` |
| `abio/capabilities.py` | `Features` (what a setup uses) vs. `Capabilities` (what an algorithm supports) |
| `abio/registry.py` | Plugin registry and `Algorithm` base (name, description, capabilities, options) |
| `abio/formats.py` | All document readers and writers (YAML / JSON / JSON Lines streams) |
| `abio/gen/` | **(1)** GEN: `hyperparams.py` (defaults = base problem), `exprgen.py` (expression helpers), `generator.py`, `main.py` |
| `abio/lin/` | **(2)(3)** Linearization APIs `api.py` + algorithms + `main.py` |
| `abio/solve/` | **(4)** Solver API `api.py` + algorithms + `main.py` |
| `abio/validate.py` | Minimal VAL-LIN and differential VAL-SOLVE |
| `examples/` | `formats-example.setup.yaml` (formats.md §1, all features), `base.setup.yaml`, `base/full.hyperparams.yaml` |
| `tests/` | `unittest` suite: terms/model, linearizers, solvers vs. oracle, generator and CLI |
| `contrib/` | Plugin linearizers written by Fable 5.1 and Opus 5.5 (`linear_<model>_<trial>/`, one subpackage per case); map in [`contrib/README.md`](contrib/README.md), comparison in [`contrib/REPORT.md`](contrib/REPORT.md) |

## The base problem and capabilities

The **base problem** has `Read`/`Write` only, no sync (`K = 0`), no observed results, and
atomic registers. Write data can be any expression: constants, unknown `"*"`, earlier
reads and writes of the same thread, and `~`-trees of these (`r1~7`). Unknown `init` is
also part of the base. Read-dependent data never changes `Lin(P)`, because a referenced
read always completes earlier in program order. It does change solver results, and the
feasible linearizations once reads are observed.

The work is organised in four cases:

| | no sync | sync |
|---|---|---|
| **base** | `b` | `s` |
| **observed reads** | `o` | `so` |

Every algorithm declares what it supports on top of the base:

| Capability | Meaning |
|---|---|
| `rcw` | RCW actions (compare-and-write; the result is the old content) |
| `sync` | `K > 0`: `sync.k` virtual steps and `before`/`after`/`at` edges |
| `observed_reads` | Observed read/RCW results. Linearizers then work on *feasible* linearizations only; solvers on feasible schedules. |

Sync edges and observations both **shrink** the answer: they remove linearizations and
possible values. So an algorithm cannot quietly ignore them. The CLI refuses a setup that
uses an unsupported feature. `--ignore-observed` removes the observations explicitly
instead.

| Algorithm | API | rcw | sync | observed | notes |
|---|---|---|---|---|---|
| `backtrack` | enumerator | ✓ | ✓ | – | Varol–Rotem style, reference |
| `backtrack-feasible` | enumerator | ✓ | ✓ | ✓ | backtrack + brute feasibility filter |
| `dp-positions` | counter | ✓ | ✓ | – | exact DP over per-chain positions |
| `enum-count` | counter | ✓ | ✓ | ✓ | counts by enumeration; also reports `feasible` |
| `random-topo` | sampler | ✓ | ✓ | – | distribution `any` (not uniform) |
| `dp-uniform` | sampler | ✓ | ✓ | – | exactly `uniform` |
| `rejection` | sampler | ✓ | ✓ | ✓ | `uniform-feasible` |
| `brute` | solver | ✓ | ✓ | ✓ | oracle; modes all/fixed; witnesses |

`abio lin list` and `abio solve list` print this table from the code.

## The APIs (full contracts are in the docstrings)

**Linearization, all permutations** (`abio/lin/api.py`, `LinEnumerator`):
`enumerate(setup) -> Iterator[Linearization]` yields every element of `Lin(P)`, or of the
feasible subset when there are observations. Each element appears exactly once. The
iterator is lazy and deterministic. `gray_code = True` promises that consecutive outputs
differ by one adjacent swap.

**Linearization, counting only** (`LinCounter`): `count(setup) -> CountResult(linearizations,
feasible, method, error)`. `error` is set only for estimates. A counter with
`observed_reads` must fill in `feasible`.

**Randomized linearization** (`LinSampler`): `sample(setup, rng)` and `samples(setup, rng, n)`.
Override `samples` to reuse precomputation. `distribution` is one of `any`, `uniform` or
`uniform-feasible`. All randomness comes from `rng`.

**Solver** (`abio/solve/api.py`, `Solver`): `solve(setup, linearization=None) -> Outcomes`.
The answer must be exact ("no more, no less"). It gives `Poss` for every read/RCW id and
every block, plus `consistent` (CHECK). `linearization` is given only in mode `fixed`.
`SolverCapabilities` adds `modes` and `witnesses` to the capabilities above. `Collector`
helps enumeration-based solvers.

A linearization is a tuple of node indices into `setup.poset.names`. The poset gives
`preds`/`succs`, the per-thread `thread_chains`, and a chain partition `chains`
(threads plus singleton sync nodes) for DP-style algorithms.

### Adding an algorithm

```python
from abio.capabilities import Capabilities
from abio.lin.api import CountResult, LinCounter
from abio.registry import register

@register
class MyCounter(LinCounter):
    name = "my-count"
    description = "what it does"
    capabilities = Capabilities(rcw=True, sync=False, observed_reads=False)
    options = {"eps": "tolerance"}              # --opt eps=0.1  →  self.opts["eps"]

    def count(self, setup):
        ...
        return CountResult(n, None, "my-count")
```

Put it in `abio/lin/` or `abio/solve/` and import it from that package's `__init__.py`.
Out-of-tree code can instead use `--plugin mypkg.mymod` or `--algo mypkg.mymod:MyCounter`.
Differential-test it against `enum-count` / `brute` (see `tests/test_solve.py`).

## CLI

```sh
abio gen examples/base.hyperparams.yaml --set threads=3 --seed 4 -o s.yaml --truth t.yaml
abio gen examples/full.hyperparams.yaml --count 20 --out-dir corpus/
abio lin enum   s.yaml [--algo backtrack] [--limit N | --count-only] -o lins.yaml
abio lin count  s.yaml [--algo dp-positions]
abio lin sample s.yaml [--algo dp-uniform] -n 10 --seed 1
abio solve run  s.yaml [--algo brute] [--witnesses w.yaml]           # mode all
abio solve run  s.yaml --algo brute --lin lins.yaml --index 3        # mode fixed
abio validate lin   s.yaml lins.yaml
abio validate solve s.yaml outcomes.yaml [--oracle brute] [--lin lins.yaml --index 3]
```

`--json` switches output to JSON (streams become JSON Lines). `-` means stdin/stdout.

## Known limits and next steps

* The oracles are exponential. `brute` enumerates every linearization × every effect order.
  A 3-thread, 3-action setup with sync already takes seconds, and `|Lin(P)|` explodes
  quickly (3 threads × 6 steps ≈ 17M orders). Keep differential tests tiny, and do not
  `list()` an enumerator.
* `brute` is the only solver, in all four cases. The earlier `window` solver (visions.md
  §3.2, constant data only) was removed when read-dependent data became part of the base.
  A polynomial solver is RQ1.
* Only atomic registers with distinct effect points are implemented. Setups with other
  `semantics` are refused.
* Not yet built: Gray-code enumerator (Pruesse–Ruskey), rank/unrank, MCMC samplers,
  symbolic/SMT solver, online solver (`trace` documents), VAL-ENUM, and the
  `schedule`-level validator CLI.
