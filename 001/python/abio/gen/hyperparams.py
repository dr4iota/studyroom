"""Generator hyperparameters (formats.md §9, premise.md §3).

Every key has a default; the defaults describe the **base problem**: reads and writes
only, write data mixing constants and read-dependent expressions, no sync points, no
observed results, all contents known. Turn extensions on with
``kind_mix.rcw > 0``, ``sync_points > 0`` and ``events_per_thread > 0``,
``knowledge.p_r > 0``, ``knowledge.p_w < 1``, ``knowledge.init_known < 1``.

``content.classes`` weights are per write. A ``copy``/``combine`` draw needs an already
completed read in the same thread; when there is none (e.g. the thread's first actions)
the write gets a constant instead. So the realized mix has more constants than the
weights say, especially with ``max_in_flight`` large or few actions per thread; use
``Setup.has_data_from_reads()`` to check a generated setup.
"""

from __future__ import annotations

import copy
from typing import Any

import yaml

DEFAULTS: dict[str, Any] = {
    "format": "hyperparams",
    "version": 2,
    "seed": 0,
    "id": None,  # setup id; default "gen-<seed>"
    "threads": 2,
    "blocks": 2,
    "sync_points": 0,
    "actions_per_thread": 3,  # int, or {total: {read: n, write: n, rcw: n}}
    "events_per_thread": 0,
    "relations": ["before", "after", "at"],
    "max_in_flight": 2,  # 1 = synchronous I/O
    "kind_mix": {"read": 0.5, "write": 0.5, "rcw": 0.0},
    "block_skew": {"kind": "uniform"},  # or {kind: zipf, s: 1.0}
    "writers_per_block": None,  # max distinct writer threads per block (hardness dial)
    "content": {
        "classes": {"const": 0.4, "copy": 0.3, "combine": 0.3},  # premise §2.5 classes 1/2/3
        "max_depth": 2,
        "value_pool": 8,  # constants are drawn from 1..value_pool (small => repeats)
    },
    "knowledge": {"p_w": 1.0, "p_r": 0.0, "init_known": 1.0},
    "semantics": {"register": "atomic", "rcw_result": "old"},
    "max_attempts": 100,  # retries when random events create a cyclic poset
}


def _merge(base: dict, over: dict, path: str = "") -> dict:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k not in base:
            raise KeyError(f"unknown hyperparameter {path}{k}")
        if isinstance(base[k], dict) and isinstance(v, dict) and k not in ("kind_mix", "actions_per_thread", "block_skew", "classes"):
            out[k] = _merge(base[k], v, f"{path}{k}.")
        else:
            out[k] = copy.deepcopy(v)
    return out


def resolve(doc: dict | None = None, overrides: list[str] | None = None) -> dict:
    """Defaults <- document <- ``key.sub=value`` overrides (values parsed as YAML)."""
    doc = dict(doc or {})
    if doc.get("format", "hyperparams") != "hyperparams":
        raise ValueError("not a hyperparams document")
    doc.pop("meta", None)
    hp = _merge(DEFAULTS, doc)
    for ov in overrides or []:
        key, sep, val = ov.partition("=")
        if not sep:
            raise ValueError(f"override must be key=value: {ov!r}")
        *parents, last = key.split(".")
        d = hp
        for p in parents:
            d = d[p]
        if last not in d:
            raise KeyError(f"unknown hyperparameter {key}")
        d[last] = yaml.safe_load(val)
    _check(hp)
    return hp


def _check(hp: dict) -> None:
    for k in ("threads", "blocks", "sync_points", "events_per_thread", "max_in_flight"):
        if not isinstance(hp[k], int) or hp[k] < 0:
            raise ValueError(f"{k} must be a non-negative integer")
    if hp["threads"] < 1 or hp["blocks"] < 1 or hp["max_in_flight"] < 1:
        raise ValueError("threads, blocks and max_in_flight must be >= 1")
    if hp["events_per_thread"] and not hp["sync_points"]:
        raise ValueError("events_per_thread > 0 needs sync_points > 0")
    if hp["events_per_thread"] > hp["sync_points"] * len(hp["relations"]):
        raise ValueError("events_per_thread exceeds sync_points x relations (one event per pair per thread)")
    bad = set(hp["relations"]) - {"before", "after", "at"}
    if bad:
        raise ValueError(f"unknown relations {bad}")
    for k, v in hp["knowledge"].items():
        if not 0 <= v <= 1:
            raise ValueError(f"knowledge.{k} must be in [0, 1]")
