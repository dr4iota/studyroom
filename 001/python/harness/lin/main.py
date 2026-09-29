"""``harness lin``: run a pluggable enumerator, counter or sampler on a setup.

    harness lin list
    harness lin enum   SETUP [--algo backtrack]   [--limit N] [-o OUT] [--json]
    harness lin count  SETUP [--algo dp-positions]
    harness lin sample SETUP [--algo dp-uniform]  [-n N] [--seed S]

Common options: ``--opt KEY=VALUE`` (algorithm options), ``--plugin MODULE``,
``--ignore-observed``. Output documents follow formats.md (``linearization`` stream,
``count``).
"""

from __future__ import annotations

import argparse
import random
import time

from .. import cli_common as C
from ..formats import Output, count_doc, linearization_doc
from .api import LinCounter, LinEnumerator, LinSampler


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("lin", help="enumerate / count / sample linearizations")
    lsub = p.add_subparsers(dest="lin_cmd", required=True)

    lp = lsub.add_parser("list", help="list registered linearization algorithms")
    C.add_plugin_arg(lp)

    e = lsub.add_parser("enum", help="enumerate linearizations (LIN-ENUM)")
    C.add_io_args(e)
    C.add_algo_args(e, "backtrack")
    C.add_plugin_arg(e)
    e.add_argument("--limit", type=int, default=None, help="stop after N linearizations")
    e.add_argument("--count-only", action="store_true", help="print the number enumerated instead of the stream")

    c = lsub.add_parser("count", help="count linearizations (LIN-COUNT)")
    C.add_io_args(c)
    C.add_algo_args(c, "dp-positions")
    C.add_plugin_arg(c)

    s = lsub.add_parser("sample", help="sample random linearizations (LIN-SAMPLE)")
    C.add_io_args(s)
    C.add_algo_args(s, "dp-uniform")
    C.add_plugin_arg(s)
    s.add_argument("-n", type=int, default=1, help="number of samples")
    s.add_argument("--seed", type=int, default=0)
    p.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    C.setup_plugins(args)
    if args.lin_cmd == "list":
        for cat, extra in (("lin-enum", "gray_code"), ("lin-count", ""), ("lin-sample", "distribution")):
            print(f"== {cat}")
            C.list_algorithms(cat, extra)
        return 0
    setup = C.load(args.setup)
    syntax = "json" if args.json else None

    if args.lin_cmd == "enum":
        algo = C.instantiate("lin-enum", args.algo, LinEnumerator, args.opt)
        setup = C.admit(setup, algo, args.ignore_observed)
        n = 0
        t0 = time.perf_counter()
        with Output(args.output, syntax) as out:
            for order in algo.enumerate(setup):
                if args.limit is not None and n >= args.limit:
                    break
                if not args.count_only:
                    out.write(linearization_doc(setup, order, {"index": n, "algo": algo.name}))
                n += 1
            if args.count_only:
                print(n, file=out.fh)
        _stats(f"enumerated {n} in {time.perf_counter() - t0:.3f}s")
        return 0

    if args.lin_cmd == "count":
        algo = C.instantiate("lin-count", args.algo, LinCounter, args.opt)
        setup = C.admit(setup, algo, args.ignore_observed)
        res = algo.count(setup)
        with Output(args.output, syntax) as out:
            out.write(count_doc(setup, res, {"algo": algo.name}))
        return 0

    algo = C.instantiate("lin-sample", args.algo, LinSampler, args.opt)
    setup = C.admit(setup, algo, args.ignore_observed)
    rng = random.Random(args.seed)
    with Output(args.output, syntax) as out:
        for i, order in enumerate(algo.samples(setup, rng, args.n)):
            out.write(linearization_doc(setup, order, {"index": i, "algo": algo.name, "seed": args.seed,
                                                       "distribution": algo.distribution}))
    return 0


def _stats(msg: str) -> None:
    import sys

    print(msg, file=sys.stderr)
