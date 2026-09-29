"""Argument parsing and plumbing shared by the ``lin``, ``solve`` and ``gen`` mains."""

from __future__ import annotations

import argparse
import sys
from typing import Any, NoReturn

import yaml

from .capabilities import Capabilities
from .formats import load_setup
from .model import Setup
from .registry import Algorithm, available, load_plugins, resolve


class CLIError(Exception):
    pass


def die(msg: str) -> NoReturn:
    raise CLIError(msg)


def add_algo_args(p: argparse.ArgumentParser, default: str) -> None:
    p.add_argument("--algo", default=default, help=f"registered name or module:Class (default {default})")
    p.add_argument("--opt", action="append", default=[], metavar="KEY=VALUE", help="algorithm option (repeatable)")


def add_io_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("setup", help="setup document (.yaml/.json, - for stdin)")
    p.add_argument("-o", "--output", default="-", help="output path (default stdout)")
    p.add_argument("--json", action="store_true", help="write JSON / JSON Lines instead of YAML")
    p.add_argument("--ignore-observed", action="store_true",
                   help="drop observed read results instead of refusing an algorithm without observed_reads")


def add_plugin_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--plugin", action="append", default=[], metavar="MODULE", help="import MODULE to register algorithms")


def parse_opts(items: list[str]) -> dict[str, Any]:
    out = {}
    for it in items:
        k, sep, v = it.partition("=")
        if not sep:
            die(f"--opt expects KEY=VALUE, got {it!r}")
        out[k] = yaml.safe_load(v)
    return out


def instantiate(category: str, spec: str, base: type[Algorithm], opts: list[str]) -> Algorithm:
    try:
        cls = resolve(category, spec, base)
        return cls(**parse_opts(opts))
    except (KeyError, TypeError, ValueError, ImportError, AttributeError) as ex:
        die(str(ex))


def admit(setup: Setup, algo: Algorithm, ignore_observed: bool) -> Setup:
    """Refuse a setup that uses features the algorithm does not support."""
    if not setup.semantics.is_default():
        die(f"semantics {setup.semantics} not implemented (only atomic registers with distinct effects)")
    feats = setup.features()
    if ignore_observed and feats.observed_reads:
        setup = setup.without_observations()
        feats = setup.features()
    missing = algo.capabilities.missing(feats)
    if missing:
        hint = " (or pass --ignore-observed)" if missing == ["observed_reads"] else ""
        die(f"algorithm '{algo.name}' does not support {', '.join(missing)}, which setup '{setup.id}' uses{hint}")
    return setup


def load(path: str) -> Setup:
    try:
        return load_setup(path)
    except (OSError, ValueError, yaml.YAMLError) as ex:
        die(f"{path}: {ex}")


def list_algorithms(category: str, extra: str = "") -> int:
    algos = available(category)
    if not algos:
        print(f"(no {category} algorithms registered)")
    for name, cls in algos.items():
        caps: Capabilities = cls.capabilities
        more = f" {extra}={getattr(cls, extra)}" if extra else ""
        print(f"{name:20s} {cls.description}")
        print(f"{'':20s}   {caps.summary()}{more}")
        for k, v in cls.options.items():
            print(f"{'':20s}   --opt {k}=...  {v}")
    return 0


def run(main_fn: Any, argv: list[str] | None) -> int:
    try:
        return main_fn(argv)
    except CLIError as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


def setup_plugins(args: argparse.Namespace) -> None:
    try:
        load_plugins(getattr(args, "plugin", []))
    except ImportError as ex:
        die(f"cannot import plugin: {ex}")
