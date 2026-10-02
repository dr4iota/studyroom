"""Grading the loop tasks (``loop-count``, ``loop-solver``).

Attempts get the iteration count ``n`` as an input, and are told it may be arbitrarily
large. The grader checks in three tiers:

1. **Exact at small n** (``n = 1..4``, within an action budget): unroll to ``P_n`` and
   compare with the validated oracles (``loop.reference``).
2. **Exact at large n,** on instances whose answer is known for every ``n``:
   - *counts in case b*: with no sync, threads are independent chains, so
     ``|Lin(P_n)|`` is the multinomial of the chain lengths;
   - *barrier products*: every thread ends its body with ``at`` on the per-iteration
     sync point, and there are no other events. Then
     ``|Lin(P_n)| = m(prefix+body) · m(body)^(n-1) · m(suffix)``, where ``m`` is the
     multinomial of per-thread segment lengths. The formula is checked against the
     oracle for ``n ≤ 4`` before use;
   - *relays*: a value moves one block per iteration, so the possibility sets change
     until ``n`` reaches the relay length, then every read is forced. The oracle answer
     at ``n = stable_from`` is the answer for all larger ``n``; it is checked to be
     unchanged over three further ``n`` before use.
3. **Scaling:** a ladder of ``n`` under the time limit; the score is the largest ``n``
   cleared.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable

from .. import terms as T
from ..gen.loops import generate_loop
from ..loop.reference import oracle_count, oracle_solve
from ..loops import LoopSetup
from .checks import _guard

COUNT_LADDER = [10, 100, 1000, 3000, 10000]
SOLVE_LADDER = [10, 100, 1000, 10**4, 10**5, 10**6]
MAX_UNROLLED = 26  # actions; the exact tier uses n = 1..4 while P_n stays within this


@dataclass
class LoopInstance:
    id: str
    case: str  # b | s
    setup: LoopSetup
    small_ns: list[int]
    count_at: Callable[[int], int] | None = None  # exact count for any n, when known
    solve_at: Callable[[int], tuple] | None = None  # exact (results, final) for any n, when known


def _m(lengths) -> int:
    total, out = 0, 1
    for k in lengths:
        total += k
        out *= math.comb(total, k)
    return out


def _seg_len(steps) -> int:
    return sum(1 for s in steps if s.kind != "at")  # an `at` step merges into the sync node


def _small_ns(L: LoopSetup) -> list[int]:
    return [n for n in (1, 2, 3, 4) if len(L.unroll(n).actions) <= MAX_UNROLLED] or [1]


def _multinomial_count(L: LoopSetup) -> Callable[[int], int]:
    def f(n):
        return _m([_seg_len(t.prefix) + n * _seg_len(t.body) + _seg_len(t.suffix) for t in L.threads])
    return f


def _barrier_count(L: LoopSetup) -> Callable[[int], int] | None:
    """Count formula when every body ends with `at` on loop sync 0 and nothing else syncs.

    A declared plain sync point that no event uses is an isolated node of P_n and would
    multiply the count, so such setups get no formula.
    """
    if L.sync_points:
        return None
    for t in L.threads:
        evs = [s for seg in (t.prefix, t.body, t.suffix) for s in seg if s.is_event]
        if len(evs) != 1 or not t.body or t.body[-1].kind != "at":
            return None
    first = [_seg_len(t.prefix) + _seg_len(t.body) for t in L.threads]
    mid = [_seg_len(t.body) for t in L.threads]
    last = [_seg_len(t.suffix) for t in L.threads]
    # sync nodes: one per iteration, each a single node between segments
    return lambda n: _m(first) * _m(mid) ** (n - 1) * _m(last)


def _sets(o):
    return ({k: frozenset(v) for k, v in o.results.items()}, {b: frozenset(v) for b, v in o.final.items()})


def _relay(k: int, extra_reader: bool) -> LoopSetup:
    """k threads relay init value 9 from block 0 to block k, one hop per iteration."""
    threads = []
    for j in range(k):
        body = [{"read": j, "id": f"r{j}"}, {"done": f"r{j}"}, {"at": 0},
                {"write": j + 1, "id": f"w{j}", "data": f"r{j}"}, {"done": f"w{j}"}]
        suffix = [{"read": k, "id": "z"}, {"done": "z"}] if j == k - 1 else []
        threads.append({"id": f"t{j}", "prefix": [], "body": body, "suffix": suffix})
    if extra_reader:
        threads.append({"id": "obs", "prefix": [], "body": [{"read": k, "id": "y"}, {"done": "y"}, {"at": 0}], "suffix": []})
    return LoopSetup.from_doc({"format": "loop-setup", "version": 1, "id": f"relay-{k}{'-obs' if extra_reader else ''}",
                               "blocks": k + 1, "sync_points": 0, "loop_sync_points": 1,
                               "init": [9] + [0] * k, "threads": threads})


def _barrier_variant(seed: int) -> LoopSetup:
    """A generated loop, rewritten so every body ends with `at` on a per-iteration sync
    point and nothing else syncs: the barrier-product count formula then applies."""
    base = generate_loop(seed, threads=3, blocks=2, prefix=2, body=2, suffix=1, max_in_flight=2, sync=False)
    d = base.to_doc()
    for t in d["threads"]:
        for seg in ("prefix", "body", "suffix"):
            t[seg] = [st for st in t[seg] if not any(k in st for k in ("before", "after", "at"))]
        t["body"].append({"at": 0})
    d.update(id=f"barrier-{seed}", sync_points=0, loop_sync_points=1)
    return LoopSetup.from_doc(d)


def _stable_solve(L: LoopSetup, stable_from: int):
    ref = _sets(oracle_solve(L, stable_from))
    for n in range(stable_from + 1, stable_from + 4):
        if _sets(oracle_solve(L, n)) != ref:
            raise RuntimeError(f"{L.id}: not stable from n={stable_from}")
    return lambda n: _sets(oracle_solve(L, n)) if n < stable_from else ref


def _checked(L: LoopSetup, f: Callable[[int], int]) -> Callable[[int], int] | None:
    """``f`` if it matches the oracle on every small n; otherwise no large-n count check."""
    for n in _small_ns(L):
        if f(n) != oracle_count(L, n):
            import sys
            print(f"warning: {L.id}: count formula disagrees with the oracle at n={n}; not used", file=sys.stderr)
            return None
    return f


_MEMO: dict = {}


def loop_instances(kind: str, cases: list[str], budget: str) -> list[LoopInstance]:
    key = (kind, tuple(cases), budget)
    if key in _MEMO:
        return _MEMO[key]
    per_case = {"small": 14, "full": 40}[budget]
    out: list[LoopInstance] = []
    for case in cases:
        rng = random.Random(f"loop-{kind}-{case}")
        made = 0
        while made < per_case:
            seed = rng.randrange(10**6)
            try:
                L = generate_loop(seed, threads=rng.choice([1, 2, 2, 3]), blocks=rng.choice([1, 2]),
                                  prefix=rng.choice([0, 1, 2]), body=rng.choice([1, 2]), suffix=rng.choice([0, 1]),
                                  max_in_flight=rng.choice([1, 2]), sync=(case == "s"), value_pool=rng.choice([2, 3]))
            except RuntimeError:
                continue
            inst = LoopInstance(f"{case}-gen-{made}", case, L, _small_ns(L))
            if case == "b":
                inst.count_at = _checked(L, _multinomial_count(L))
            else:
                f = _barrier_count(L)
                inst.count_at = _checked(L, f) if f else None
            out.append(inst)
            made += 1
        if case == "s":  # exact large-n counts: barrier products
            for seed in range(3 if budget == "small" else 8):
                L = _barrier_variant(7000 + seed)
                f = _barrier_count(L)
                out.append(LoopInstance(L.id, "s", L, _small_ns(L), count_at=_checked(L, f) if f else None))
        if case == "s":  # the n-dependent traps
            for k, extra in ((2, False), (2, True), (3, False)):
                L = _relay(k, extra)
                out.append(LoopInstance(L.id, "s", L, [n for n in (1, 2, 3, 4)],
                                        count_at=_checked(L, _barrier_count(L) or _multinomial_count(L)) if _barrier_count(L) else None,
                                        solve_at=_stable_solve(L, k + 2)))
    _MEMO[key] = out
    return out


def _err(code, inst, n, msg):
    return {"code": code, "where": {"instance": inst.id, "case": inst.case, "n": n}, "message": msg}


def check_loop_count(algo, inst: LoopInstance, seconds: float) -> list[dict]:
    errs = []
    checks = [(n, oracle_count(inst.setup, n)) for n in inst.small_ns]
    if inst.count_at:
        checks += [(n, inst.count_at(n)) for n in (50, 1000)]
    for n, want in checks:
        got, e = _guard(inst_like(inst, n), seconds, lambda: algo.count(inst.setup, n))
        if e:
            errs += [dict(x, where={**x["where"], "n": n, "case": inst.case}) for x in e]
            continue
        if got != want:
            errs.append(_err("COUNT", inst, n, f"{_short(got)}, expected {_short(want)}"))
    return errs


def check_loop_solve(algo, inst: LoopInstance, seconds: float) -> list[dict]:
    errs = []
    checks = [(n, _sets(oracle_solve(inst.setup, n))) for n in inst.small_ns]
    if inst.solve_at:
        checks += [(n, inst.solve_at(n)) for n in (50, 10**6)]
    for n, (want_r, want_f) in checks:
        got, e = _guard(inst_like(inst, n), seconds, lambda: algo.solve(inst.setup, n))
        if e:
            errs += [dict(x, where={**x["where"], "n": n, "case": inst.case}) for x in e]
            continue
        cells = [({"id": r}, set(got.results.get(r, ())), set(want_r.get(r, ()))) for r in inst.setup.reads()]
        cells += [({"block": b}, set(got.final.get(b, ())), set(want_f.get(b, ()))) for b in range(inst.setup.blocks)]
        for where, g, w in cells:
            for v in T.sorted_terms(g - w):
                errs.append({**_err("OVER", inst, n, f"lists {T.format_term(v)}"), "where": {**_err("", inst, n, "")["where"], **where}})
            for v in T.sorted_terms(w - g):
                errs.append({**_err("UNDER", inst, n, f"misses {T.format_term(v)}"), "where": {**_err("", inst, n, "")["where"], **where}})
    return errs


def inst_like(inst, n):
    class _I:  # what checks._guard needs for its error records
        id = f"{inst.id}@n={n}"
    return _I


def _short(x) -> str:
    s = str(x)
    return s if len(s) <= 40 else f"{s[:18]}…({len(s)} digits)"


def loop_scaling(cat: str, algo, cases: list[str], seconds: float) -> dict:
    """Largest n on the ladder each case's scaling setups clear within the time limit."""
    ladder = COUNT_LADDER if cat == "loop-count" else SOLVE_LADDER
    stats = {}
    for case in cases:
        setups = [generate_loop(900 + i, threads=3, blocks=2, prefix=2, body=2, suffix=1, max_in_flight=2,
                                sync=(case == "s"), value_pool=3) for i in range(2)]
        if case == "s":
            setups.append(_relay(3, True))
        top = 0
        for n in ladder:
            ok = True
            for L in setups:
                fn = (lambda: algo.count(L, n)) if cat == "loop-count" else (lambda: algo.solve(L, n))
                _, e = _guard(inst_like(LoopInstance(L.id, case, L, []), n), seconds, fn)
                if e:
                    ok = False
                    break
            if not ok:
                break
            top = n
        stats[case] = {"max_n": top}
    return stats
