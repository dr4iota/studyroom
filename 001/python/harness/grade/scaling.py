"""Scaling suite: how large a setup each algorithm handles within a time limit.

The correctness instances (``instances.py``) are small, so the oracles can check them
exactly. They do not separate a clever algorithm from a slow one. This suite runs a
fixed ladder of sizes per case:
- the algorithm must finish every seed of a level within ``seconds`` per call;
- its score is the highest level it clears;
- a timeout at a level is not an error, it just ends the climb.

The oracles cannot follow the algorithms to these sizes, so correctness is spot-checked
with methods that do scale (errors are reported with ``scale=True``):

- **solvers:** random full schedules are sampled and executed. Every value a sampled
  schedule produces must be in the answer (catches UNDER), and every returned witness
  must re-execute (catches OVER when witnesses exist). Observed cases keep only the
  sampled schedules that are feasible.
- **enumerators:** the first outputs must be valid and distinct. When the enumeration
  finishes, its length must match the exact count (base cases, by the positions DP).
- **counters:** in cases without observations, counts must equal the positions DP.
"""

from __future__ import annotations

import random
import time

from .. import terms as T
from ..gen import generate
from ..lin.dp import count_linearizations
from ..lin.random_topo import random_linearization
from ..semantics import execute, random_effects
from .checks import Timeout, time_limit

# (threads, actions per thread, max in flight); higher index = harder
LADDER = [(2, 3, 2), (3, 3, 2), (3, 4, 2), (4, 4, 2), (4, 5, 2), (4, 6, 2), (5, 5, 3), (5, 6, 3), (6, 6, 3)]
MIX = {"const": 0.4, "copy": 0.3, "combine": 0.3}
BUDGETS = {"small": {"seeds": 2, "seconds": 5.0, "samples": 200},
           "full": {"seeds": 4, "seconds": 20.0, "samples": 1000}}
_MEMO: dict = {}


def setups(case: str, level: int, seeds: int):
    key = (case, level, seeds)
    if key not in _MEMO:
        t, a, f = LADDER[level]
        out = []
        for seed in range(seeds):
            hp = dict(seed=1000 * level + seed, threads=t, actions_per_thread=a, max_in_flight=f, blocks=2,
                      content={"classes": MIX, "max_depth": 2, "value_pool": 2})
            if "s" in case:
                hp.update(sync_points=2, events_per_thread=2)
            if "r" in case:
                hp["kind_mix"] = {"read": 0.4, "write": 0.3, "rcw": 0.3}
            if "o" in case:
                hp["knowledge"] = {"p_r": 0.5}
            try:
                out.append(generate(hp)[0])
            except (RuntimeError, ValueError):
                pass
        _MEMO[key] = out
    return _MEMO[key]


def _err(code, name, case, level, msg):
    return {"code": code, "where": {"algo": name, "case": case, "level": level, "scale": True}, "message": msg}


def _sample_values(s, n: int, rng: random.Random):
    """Values produced by up to ``n`` random full schedules (feasible ones only)."""
    res: dict = {}
    fin: dict = {}
    for _ in range(n):
        L = random_linearization(s, rng)
        sch = execute(s, L, random_effects(s, L, rng))
        if not sch.consistent:
            continue
        for k, v in sch.results.items():
            res.setdefault(k, set()).add(v)
        for b, v in enumerate(sch.final):
            fin.setdefault(b, set()).add(v)
    return res, fin


def _solver_check(algo, name, case, level, s, out, samples, rng):
    errs = []
    res, fin = _sample_values(s, samples, rng)
    if (res or fin) and not out.consistent:
        errs.append(_err("CONSISTENT", name, case, level, "a sampled feasible schedule exists, solver says inconsistent"))
        return errs
    for k, vs in res.items():
        miss = vs - set(out.results.get(k, ()))
        if miss:
            errs.append(_err("UNDER", name, case, level, f"{k} misses sampled {T.format_term(next(iter(miss)))}"))
    for b, vs in fin.items():
        miss = vs - set(out.final.get(b, ()))
        if miss:
            errs.append(_err("UNDER", name, case, level, f"block {b} misses sampled {T.format_term(next(iter(miss)))}"))
    for w in getattr(out, "witnesses", None) or []:
        try:
            again = execute(s, w.order, w.effects)
            c = w.meta.get("certifies", {})
            got = again.results.get(c["id"]) if "id" in c else again.final[c["block"]]
            if not again.consistent or T.to_value(got) != c.get("value"):
                errs.append(_err("WITNESS", name, case, level, f"witness for {c} does not re-execute"))
        except Exception as ex:
            errs.append(_err("WITNESS", name, case, level, f"witness does not execute: {ex}"[:200]))
    return errs


def run(cat: str, algo, name: str, cases: list[str], budget: str) -> tuple[dict, list[dict]]:
    """Climb the ladder per case. Returns (stats, errors)."""
    cfg = BUDGETS[budget]
    stats, errors = {}, []
    rng = random.Random(name)
    for case in cases:
        levels = []
        top = -1
        for level in range(len(LADDER)):
            ss = setups(case, level, cfg["seeds"])
            if not ss:
                continue
            times, ok, oom = [], True, False
            for s in ss:
                t0 = time.perf_counter()
                try:
                    with time_limit(cfg["seconds"]):
                        if cat == "solver":
                            out = algo.solve(s)
                        elif cat == "lin-count":
                            out = algo.count(s)
                        else:
                            out = _enum_probe(algo, s)
                except Timeout:
                    ok = False
                    break
                except MemoryError:
                    ok, oom = False, True
                    break
                except Exception as ex:
                    errors.append(_err("CRASH", name, case, level, f"{type(ex).__name__}: {ex}"[:200]))
                    ok = False
                    break
                times.append(time.perf_counter() - t0)
                try:
                    if cat == "solver":
                        errors += _solver_check(algo, name, case, level, s, out, cfg["samples"], rng)
                    elif cat == "lin-count":
                        if "o" not in case:  # no exact feasible count at scale: observed counters are only timed
                            exact = count_linearizations(s)
                            got = out.linearizations if out.linearizations is not None else out.feasible
                            if got != exact:
                                errors.append(_err("COUNT", name, case, level, f"{got}, exact {exact}"))
                    else:
                        errors += _enum_check(name, case, level, s, out)
                except MemoryError:  # the attempt's retained memory left no room for the checks
                    ok, oom = False, True
                    break
                finally:
                    out = None
            levels.append({"level": level, "shape": list(LADDER[level]), "cleared": ok, "out_of_memory": oom,
                           "max_seconds": round(max(times), 3) if times else None})
            if not ok:
                break
            top = level
        stats[case] = {"max_level": top, "max_shape": list(LADDER[top]) if top >= 0 else None, "levels": levels}
    return stats, errors


PROBE = 20000  # outputs taken from an enumerator per setup


def _enum_probe(algo, s):
    out, done = [], True
    for o in algo.enumerate(s):
        out.append(tuple(o))
        if len(out) >= PROBE:
            done = False
            break
    return out, done


def _enum_check(name, case, level, s, probe):
    outs, done = probe
    errs = []
    P = s.poset
    bad = sum(1 for o in outs[:200] if len(o) != len(P) or P.check(P.to_names(o)))
    if bad:
        errs.append(_err("INVALID", name, case, level, f"{bad} of the first 200 outputs are not linearizations"))
    if len(set(outs)) != len(outs):
        errs.append(_err("DUPLICATE", name, case, level, "duplicate outputs in the probe"))
    if done and "o" not in case:
        exact = count_linearizations(s)
        if len(outs) != exact:
            errs.append(_err("COUNT", name, case, level, f"enumerated {len(outs)}, exact {exact}"))
    return errs
