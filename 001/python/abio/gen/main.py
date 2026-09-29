"""``abio gen``: generate setups from hyperparameters.

    abio gen [HYPERPARAMS.yaml] [--set key.sub=value ...] [--seed S] [-o SETUP] [--truth TRUTH]
    abio gen [HYPERPARAMS.yaml] --count 20 --out-dir corpus/    # seeds S, S+1, ...

``--truth`` writes the hidden full schedule (a ``schedule`` document) that produced the
observations; with ``--out-dir`` it is always written next to each setup.
"""

from __future__ import annotations

import argparse
import os

from .. import cli_common as C
from ..formats import load_document, schedule_doc, write_document
from .generator import generate
from .hyperparams import resolve


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("gen", help="generate setups (GEN)")
    p.add_argument("hyperparams", nargs="?", help="hyperparams document (defaults if omitted)")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="override a hyperparameter")
    p.add_argument("--seed", type=int, help="override the seed")
    p.add_argument("-o", "--output", default="-", help="setup output path")
    p.add_argument("--truth", help="write the hidden schedule here")
    p.add_argument("--count", type=int, default=1, help="generate this many setups (seeds seed..seed+count-1)")
    p.add_argument("--out-dir", help="with --count: directory for <id>.setup.yaml and <id>.truth.yaml")
    p.add_argument("--json", action="store_true")
    p.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    doc = load_document(args.hyperparams, "hyperparams") if args.hyperparams else {}
    overrides = list(args.set) + ([f"seed={args.seed}"] if args.seed is not None else [])
    try:
        hp = resolve(doc, overrides)
    except (KeyError, ValueError) as ex:
        C.die(str(ex))
    if args.count > 1 and not args.out_dir:
        C.die("--count > 1 needs --out-dir")
    syntax = "json" if args.json else None
    ext = "json" if args.json else "yaml"
    base_seed, base_id = hp["seed"], hp["id"]
    for i in range(args.count):
        hp_i = dict(hp, seed=base_seed + i, id=f"{base_id}-{i}" if base_id and args.count > 1 else base_id)
        setup, truth = generate(hp_i)
        if args.out_dir:
            os.makedirs(args.out_dir, exist_ok=True)
            write_document(setup.to_doc(), os.path.join(args.out_dir, f"{setup.id}.setup.{ext}"), syntax)
            write_document(schedule_doc(setup, truth), os.path.join(args.out_dir, f"{setup.id}.truth.{ext}"), syntax)
        else:
            write_document(setup.to_doc(), args.output, syntax)
            if args.truth:
                write_document(schedule_doc(setup, truth), args.truth, syntax)
    return 0
