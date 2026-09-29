"""Per-kind checks of one algorithm on one instance, against the harness oracles.

Every check returns a list of report errors (empty = pass). Codes:

CRASH        the algorithm raised
TIMEOUT      the per-instance time limit was hit
INVALID      an output is not a linearization of the setup
DUPLICATE    an enumerator produced the same linearization twice
MISSING      an enumerator missed a linearization the oracle has
EXTRA        an enumerator produced a linearization the oracle does not have (e.g. infeasible)
COUNT        a counter's number differs from the oracle's
CONSISTENT   a solver's CHECK verdict differs from the oracle's
OVER, UNDER  a solver lists a value the oracle does not / misses one
WITNESS      a solver witness does not re-execute to what it certifies
"""

from __future__ import annotations

import random
import signal
import time
from contextlib import contextmanager
from typing import Iterator

from .. import terms as T
from ..lin.backtrack import linear_extensions
from ..lin.dp import count_linearizations
from ..semantics import execute, is_feasible
from ..solve.brute import BruteForce
from .instances import Instance


class Timeout(Exception):
    pass


@contextmanager
def time_limit(seconds: float) -> Iterator[None]:
    def handler(*_):
        raise Timeout()
    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def _err(code: str, inst: Instance, msg: str, **where) -> dict:
    return {"code": code, "where": {"instance": inst.id, **where}, "message": msg}


def _guard(inst: Instance, seconds: float, fn):
    """Run ``fn`` under the time limit; return (result, errors)."""
    try:
        with time_limit(seconds):
            return fn(), []
    except Timeout:
        return None, [_err("TIMEOUT", inst, f"over {seconds:g}s")]
    except MemoryError:
        return None, [_err("CRASH", inst, "MemoryError")]
    except Exception as ex:  # the attempt's own bug
        return None, [_err("CRASH", inst, f"{type(ex).__name__}: {ex}"[:300])]


_CACHE: dict = {}  # oracle answers, keyed by (kind, instance id, linearization)


def _cached(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key]


def feasible_set(setup) -> set:
    return _cached(("feas", setup.id, id(setup)), lambda: {o for o in linear_extensions(setup) if is_feasible(setup, o)})


def check_enumerator(algo, inst: Instance, seconds: float) -> list[dict]:
    s = inst.setup
    want = feasible_set(s)
    limit = 2 * len(want) + 10  # stop a runaway enumerator

    def run():
        out = []
        for o in algo.enumerate(s):
            out.append(tuple(o))
            if len(out) >= limit:
                break
        return out
    got, errs = _guard(inst, seconds, run)
    if errs:
        return errs
    errs = []
    names = s.poset
    bad = [o for o in got if len(o) != len(names) or names.check(names.to_names(o))]
    if bad:
        errs.append(_err("INVALID", inst, f"{len(bad)} outputs are not linearizations"))
    if len(got) != len(set(got)):
        errs.append(_err("DUPLICATE", inst, f"{len(got) - len(set(got))} duplicate outputs"))
    gs = set(got) - set(bad)
    if want - gs:
        errs.append(_err("MISSING", inst, f"{len(want - gs)} of {len(want)} oracle linearizations missing"))
    if gs - want:
        errs.append(_err("EXTRA", inst, f"{len(gs - want)} outputs not in the oracle set (infeasible)"))
    return errs


def check_counter(algo, inst: Instance, seconds: float) -> list[dict]:
    s = inst.setup
    observed = s.features().observed_reads
    total = count_linearizations(s)
    feas = len(feasible_set(s)) if observed else None
    res, errs = _guard(inst, seconds, lambda: algo.count(s))
    if errs:
        return errs
    errs = []
    if res.linearizations is not None and res.linearizations != total:
        errs.append(_err("COUNT", inst, f"linearizations {res.linearizations}, oracle {total}"))
    if observed and res.feasible != feas:
        errs.append(_err("COUNT", inst, f"feasible {res.feasible}, oracle {feas}"))
    if not observed and res.linearizations is None and res.feasible != total:
        errs.append(_err("COUNT", inst, f"no count for linearizations (oracle {total})"))
    return errs


def _compare_outcomes(inst: Instance, got, want, mode: str) -> list[dict]:
    errs = []
    if bool(got.consistent) != want.consistent:
        return [_err("CONSISTENT", inst, f"solver {got.consistent}, oracle {want.consistent}", mode=mode)]
    if not want.consistent:
        return []
    cells = [({"id": a.id}, got.results.get(a.id, set()), want.results.get(a.id, set())) for a in inst.setup.returning()]
    cells += [({"block": b}, got.final.get(b, set()), want.final.get(b, set())) for b in range(inst.setup.blocks)]
    for where, g, w in cells:
        g = set(g)
        for v in T.sorted_terms(g - w):
            errs.append(_err("OVER", inst, f"lists {T.format_term(v)}", mode=mode, **where))
        for v in T.sorted_terms(w - g):
            errs.append(_err("UNDER", inst, f"misses {T.format_term(v)}", mode=mode, **where))
    return errs


def _check_witnesses(inst: Instance, out, mode: str) -> list[dict]:
    errs = []
    for w in getattr(out, "witnesses", []) or []:
        try:
            again = execute(inst.setup, w.order, w.effects)
            c = w.meta.get("certifies", {})
            got = again.results.get(c["id"]) if "id" in c else again.final[c["block"]]
            if not again.consistent or T.to_value(got) != c.get("value"):
                errs.append(_err("WITNESS", inst, f"witness for {c} does not re-execute to it", mode=mode))
        except Exception as ex:
            errs.append(_err("WITNESS", inst, f"witness does not execute: {ex}"[:200], mode=mode))
    return errs


def check_solver(algo, inst: Instance, seconds: float, fixed_samples: int = 2) -> list[dict]:
    s = inst.setup
    errs: list[dict] = []
    oracle = BruteForce(witnesses=False)
    modes = algo.capabilities.modes
    if "all" in modes:
        got, e = _guard(inst, seconds, lambda: algo.solve(s))
        errs += e or (_compare_outcomes(inst, got, _cached(("all", s.id, id(s)), lambda: oracle.solve(s)), "all") + _check_witnesses(inst, got, "all"))
    if "fixed" in modes:
        rng = random.Random(inst.id)
        orders = list(linear_extensions(s))
        for L in rng.sample(orders, min(fixed_samples, len(orders))):
            got, e = _guard(inst, seconds, lambda: algo.solve(s, L))
            errs += e or (_compare_outcomes(inst, got, _cached(("fixed", s.id, id(s), L), lambda: oracle.solve(s, L)), "fixed") + _check_witnesses(inst, got, "fixed"))
    return errs


CHECKS = {"lin-enum": check_enumerator, "lin-count": check_counter, "solver": check_solver}


def throughput(algo, setup, seconds: float = 3.0, cap: int = 200_000) -> float | None:
    """Outputs per second of an enumerator on a large instance (no oracle); None on error."""
    k = 0
    t = time.perf_counter()
    try:
        with time_limit(seconds):
            for _ in algo.enumerate(setup):
                k += 1
                if k >= cap:
                    break
    except Timeout:
        pass
    except Exception:
        return None
    return k / (time.perf_counter() - t)
