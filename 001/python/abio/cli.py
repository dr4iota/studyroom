"""``abio`` command line: ``gen``, ``lin``, ``solve``, ``validate``."""

from __future__ import annotations

import argparse

from . import cli_common as C
from . import lin, solve  # noqa: F401  (registers built-in algorithms)
from . import validate
from .gen import main as gen_main
from .lin import main as lin_main
from .solve import main as solve_main


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="abio", description="Trace analysis for asynchronous multi-threaded block I/O")
    sub = p.add_subparsers(dest="cmd", required=True)
    gen_main.add_parser(sub)
    lin_main.add_parser(sub)
    solve_main.add_parser(sub)
    validate.add_parser(sub)
    return p


def _main(argv: list[str] | None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)


def main(argv: list[str] | None = None) -> int:
    return C.run(_main, argv)
