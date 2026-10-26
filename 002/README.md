# 002 — Deducing the outcomes of a concurrent I/O trace

**Category: LLM response performance test.**

Study 001 asks models to write solvers. This study asks them to *be* the solver. A model
gets a small multi-threaded read/write trace in plain language, with no tools. It must
list every possible combination of a few asked values (read results, final block
contents). Two exact solvers provide the answer to grade against.

Models write no code; our code only generates problems, computes the truth, calls the
models and grades their answers.

## Reading order

1. [`premise.md`](premise.md): the problem, the ground truth, the generator parameters
   and the protocol.
2. [`cases/t2op9b3v6s4pnc5x5q4-04.md`](cases/t2op9b3v6s4pnc5x5q4-04.md): a case study of
   one small problem that most models get wrong, solved by hand.
3. [`REPORT.md`](REPORT.md): all results.

## Layout

| Path | What |
|------|------|
| `python/deduce.py` | Everything: model, generator, solver and enumerator, rendering, model runs, grading, report. No dependencies beyond Python 3.10. |
| `python/test_deduce.py` | Hand-checked cases; solver against enumerator on random problems. |
| `prompts/v1.md` | The prompt template. |
| `problems/<name>/` | One problem, named `<parameters>-<case>` (see `premise.md` §3): `problem.json` (structured), `problem.txt` (as the model sees it), `truth.json` (solver and enumerator answers, trap rows). |
| `attempts/<name>/prompt-v<N>.txt` | The exact prompt sent for that problem, once per prompt version; shared by all its runs. |
| `attempts/<name>/<model>-<effort>-<trial>/` | One model run, e.g. `opus55-low-1` (the model name carries its version): `reply.md` (the model's reply), `response.json` (raw CLI output without the reply), `meta.json`, `grade.json`. |
| `attempts/_archive/`, `problems/_archive/` | Superseded cases, kept but not reported. |
| `cases/` | Short case studies of single problems. |

The problems, prompts and runs are not Python-specific, so they sit at the study level;
`python/` holds only the code that builds problems, calls the models and grades them.

## Checks

From `python/`:

```sh
ulimit -v 3000000
python3 -m unittest test_deduce                  # solver vs enumerator, hand cases
python3 deduce.py gen --threads 2 --ops 4 --blocks 2 --p-obs 0.4   # next problem
python3 deduce.py run t2op4b2v3g4-01 --effort low  # fable51 x1, opus55/sonnet55/haiku55 x3
python3 deduce.py regrade                        # add trap data, regrade all replies
python3 deduce.py report                         # rewrite ../REPORT.md
```
