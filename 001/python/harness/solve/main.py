"""``harness solve``: run a pluggable solver on a setup.

    harness solve list
    harness solve run SETUP [--algo brute] [--lin LIN.yaml [--index I]] [-o OUT] [--witnesses PATH]

Without ``--lin`` the solver runs in mode ``all`` (every linearization); with ``--lin``
it runs in mode ``fixed`` on the ``I``-th linearization document of the stream
(default the first). Output is an ``outcomes`` document; witnesses, if the solver
produces them and ``--witnesses`` is given, are written as a ``schedule`` stream.
"""

from __future__ import annotations

import argparse
import sys
import time

from .. import cli_common as C
from ..formats import FormatError, Output, load_documents, outcomes_doc, parse_linearization, schedule_doc
from .api import Solver


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("solve", help="compute possibility sets (SOLVE-*)")
    ssub = p.add_subparsers(dest="solve_cmd", required=True)
    lp = ssub.add_parser("list", help="list registered solvers")
    C.add_plugin_arg(lp)
    r = ssub.add_parser("run", help="run a solver")
    C.add_io_args(r)
    C.add_algo_args(r, "brute")
    C.add_plugin_arg(r)
    r.add_argument("--lin", help="linearization stream: solve in mode fixed")
    r.add_argument("--index", type=int, default=0, help="which document of --lin (0-based)")
    r.add_argument("--witnesses", help="write witness schedules to this path")
    p.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    C.setup_plugins(args)
    if args.solve_cmd == "list":
        return C.list_algorithms("solver")
    setup = C.load(args.setup)
    algo = C.instantiate("solver", args.algo, Solver, args.opt)
    setup = C.admit(setup, algo, args.ignore_observed)
    mode = "fixed" if args.lin else "all"
    if mode not in algo.capabilities.modes:
        C.die(f"solver '{algo.name}' does not support mode {mode} (modes: {', '.join(sorted(algo.capabilities.modes))})")

    order, lin_ref = None, None
    if args.lin:
        try:
            docs = load_documents(args.lin)
            order = parse_linearization(setup, docs[args.index])
        except (OSError, IndexError, FormatError) as ex:
            C.die(f"{args.lin}: {ex}")
        lin_ref = {"path": args.lin, "index": args.index}

    t0 = time.perf_counter()
    out = algo.solve(setup, order)
    out.meta.setdefault("algo", algo.name)
    print(f"solved in {time.perf_counter() - t0:.3f}s", file=sys.stderr)

    wpath = None
    if args.witnesses and out.witnesses:
        wpath = args.witnesses
        with Output(wpath, "json" if args.json else None) as w:
            for s in out.witnesses:
                w.write(schedule_doc(setup, s))
    with Output(args.output, "json" if args.json else None) as o:
        o.write(outcomes_doc(setup, out, linearization=lin_ref, witnesses=wpath))
    return 0
