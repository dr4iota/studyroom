"""``harness grade``: grade attempts against the harness oracles (see ``__init__``)."""

from __future__ import annotations

import argparse
import importlib
import pathlib
import resource
import sys
import time
from collections import Counter

from .. import cli_common as C
from ..formats import Output, report_doc
from ..gen import generate
from ..lin.api import LinCounter, LinEnumerator, LinSampler
from ..registry import available
from ..solve.api import Solver
from . import checks, policy, scaling, tasks
from .instances import covered_cases, instances

CATEGORIES = {"lin-enum": LinEnumerator, "lin-count": LinCounter, "lin-sample": LinSampler, "solver": Solver}


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("grade", help="grade attempts against the oracles (GRADE)")
    p.add_argument("--plugin", action="append", default=[], metavar="MODULE", help="attempt package to grade (repeatable)")
    p.add_argument("--algo", action="append", default=[], help="grade only these algorithm names")
    p.add_argument("--budget", choices=["small", "full"], default="small")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--seconds", type=float, default=20.0, help="time limit per algorithm call")
    p.add_argument("--mem-mb", type=int, default=2000, help="address-space cap for the whole grader")
    p.add_argument("--no-throughput", action="store_true")
    p.add_argument("--no-scaling", action="store_true", help="skip the scaling suite")
    p.add_argument("-o", "--output", default="-")
    p.set_defaults(handler=handle)


def _registered() -> dict[str, dict[str, type]]:
    return {c: dict(available(c)) for c in CATEGORIES}


def _perf_setups() -> dict[str, object]:
    out = {}
    for label, hp in [("b", dict(threads=3, actions_per_thread=3)),
                      ("s", dict(threads=3, actions_per_thread=3, sync_points=2, events_per_thread=2)),
                      ("o", dict(threads=3, actions_per_thread=3, knowledge={"p_r": 1.0}, content={"value_pool": 2})),
                      ("so", dict(threads=3, actions_per_thread=3, sync_points=2, events_per_thread=2,
                                  knowledge={"p_r": 1.0}, content={"value_pool": 2}))]:
        out[label] = generate({"seed": 7, **hp})[0]
    return out


def handle(args: argparse.Namespace) -> int:
    lim = args.mem_mb * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except (ValueError, OSError):
        pass
    before = _registered()
    errors: list[dict] = []
    roots: dict[str, pathlib.Path] = {}
    for mod in args.plugin:
        try:
            m = importlib.import_module(mod)
        except Exception as ex:
            errors.append({"code": "IMPORT", "where": {"plugin": mod}, "message": f"{type(ex).__name__}: {ex}"[:300]})
            continue
        root = pathlib.Path(m.__file__).parent
        errors += policy.check_package(mod, root)
        roots[mod] = root
    after = _registered()
    for mod, root in roots.items():
        task = tasks.parse(mod)
        if task is not None:
            mine = [(c, n, k) for c, algos in after.items() for n, k in algos.items()
                    if n not in before[c] and k.__module__.startswith(mod)]
            errors += tasks.conformance(task, root, mine)
    todo = []
    for cat, algos in after.items():
        for name, cls in algos.items():
            new = name not in before[cat]
            if (args.algo and name in args.algo) or (not args.algo and new):
                todo.append((cat, name, cls))
    if not todo and not errors:
        C.die("nothing to grade: no --plugin registered new algorithms and no --algo matched")

    stats: dict = {}
    perf = None if args.no_throughput else _perf_setups()
    for cat, name, cls in sorted(todo):
        t0 = time.perf_counter()
        try:
            algo = cls()
        except Exception as ex:
            errors.append({"code": "CRASH", "where": {"algo": name}, "message": f"constructor: {ex}"[:300]})
            continue
        caps = cls.capabilities
        cases = covered_cases(caps.sync, caps.observed_reads, caps.rcw)
        insts = instances(cases, args.budget, args.seed)
        check = checks.CHECKS.get(cat)
        if check is None:
            stats[name] = {"category": cat, "note": "not graded (no checker for this category)"}
            continue
        fails = Counter()
        n_fail = 0
        for inst in insts:
            errs = check(algo, inst, args.seconds)
            for e in errs:
                e["where"] = {"algo": name, "case": inst.case, **e["where"]}
                fails[e["code"]] += 1
            n_fail += bool(errs)
            errors += errs
        st = {"category": cat, "cases": cases, "instances": len(insts), "failed": n_fail,
              "errors": dict(fails), "seconds": round(time.perf_counter() - t0, 1)}
        if perf and cat == "lin-enum":
            st["throughput"] = {c: (round(r) if (r := checks.throughput(algo, s)) is not None else "error")
                                for c, s in perf.items() if c in cases}
        if not args.no_scaling:
            try:
                sc, sc_errs = scaling.run(cat, algo, name, cases, args.budget)
            except Exception as ex:  # a harness bug must not abort the whole grade
                sc, sc_errs = {}, [{"code": "GRADER", "where": {"algo": name},
                                    "message": f"scaling suite failed: {type(ex).__name__}: {ex}"[:300]}]
            st["scaling"] = sc
            errors += sc_errs
            fails.update(e["code"] for e in sc_errs)
        stats[name] = st
        print(f"{name:28s} {cat:10s} cases={','.join(cases):9s} {len(insts) - n_fail}/{len(insts)} passed"
              f"  {dict(fails) or ''}"
              + (f"  scale={ {c: v['max_level'] for c, v in st['scaling'].items()} }" if "scaling" in st else ""),
              file=sys.stderr)
    with Output(args.output) as out:
        out.write(report_doc("grade:" + ",".join(args.plugin or args.algo), "grade", errors, stats))
    return 0 if not errors else 1
