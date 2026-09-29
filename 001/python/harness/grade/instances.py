"""Grading instances, per case: generated ones plus a fixed adversarial suite.

Attempts never see this file. Instances are small enough for the brute-force oracles
(``backtrack-feasible`` for linearizations, ``brute`` for solvers).

Cases: ``b`` base, ``s`` base + sync, ``o`` observed, ``so`` observed + sync, and the same
four with RCW actions: ``br``, ``sr``, ``or``, ``sor``. An algorithm is graded on every case
its capabilities cover, e.g. one declaring ``sync``, ``observed_reads`` and ``rcw`` gets all
eight.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .. import terms as T
from ..gen import generate
from ..lin.dp import count_linearizations
from ..model import MalformedSetup, Setup

CASES = ("b", "s", "o", "so", "br", "sr", "or", "sor")
RCW_MIX = {"read": 0.4, "write": 0.3, "rcw": 0.3}
MIXES = [
    {"const": 1.0, "copy": 0.0, "combine": 0.0},
    {"const": 0.4, "copy": 0.3, "combine": 0.3},
    {"const": 0.2, "copy": 0.4, "combine": 0.4},
]


@dataclass
class Instance:
    id: str
    case: str
    setup: Setup
    origin: str  # generated | suite | randomized


def covered_cases(sync: bool, observed: bool, rcw: bool = False) -> list[str]:
    return [c for c in CASES if ("s" not in c or sync) and ("o" not in c or observed) and ("r" not in c or rcw)]


def _fits(s: Setup, max_lin: int, max_actions: int) -> bool:
    return len(s.actions) <= max_actions and count_linearizations(s) <= max_lin


def _randomize_observations(s: Setup, truth_results: dict, rng: random.Random) -> Setup:
    """Replace observations by plausible but random terms (often infeasible)."""
    pool = list(truth_results.values()) + list(s.init) + [T.Const(1), T.Const(2)]
    d = s.to_doc()
    d["id"] = s.id + "-rnd"
    for th in d["threads"]:
        for st in th["steps"]:
            if "done" in st and s.actions[st["done"]].kind == "read":
                st.pop("data", None)
                if rng.random() < 0.6:
                    v = rng.choice(pool)
                    if rng.random() < 0.4:
                        v = T.Pair(v, rng.choice(pool))
                    st["data"] = T.to_value(v)
    return Setup.from_doc(d)


def generated(case: str, n: int, seed: int, max_lin: int, max_actions: int) -> list[Instance]:
    rng = random.Random(f"{case}-{seed}")
    out: list[Instance] = []
    tries = 0
    while len(out) < n and tries < 40 * n:
        tries += 1
        hp = {
            "seed": rng.randrange(10**6), "threads": rng.choice([1, 2, 2, 3]), "blocks": rng.choice([1, 2]),
            "actions_per_thread": rng.choice([1, 2, 3]), "max_in_flight": rng.choice([1, 1, 2, 3]),
            "kind_mix": dict(RCW_MIX) if "r" in case else {"read": 0.55, "write": 0.45},
            "content": {"classes": rng.choice(MIXES), "max_depth": 2, "value_pool": rng.choice([1, 2, 3])},
            "knowledge": {"p_w": rng.choice([1.0, 0.7]), "p_r": 0.0, "init_known": 0.5},
        }
        if "s" in case:
            k = rng.choice([1, 2])
            rels = rng.choice([["before", "after", "at"], ["at"], ["before", "after"], ["before"], ["after", "at"]])
            hp.update(sync_points=k, events_per_thread=min(rng.choice([1, 2]), k * len(rels)), relations=rels)
        if "o" in case:
            hp["knowledge"]["p_r"] = rng.choice([0.3, 0.7, 1.0])
        try:
            s, truth = generate(hp)
        except (RuntimeError, ValueError, KeyError):
            continue
        if not _fits(s, max_lin, max_actions):
            continue
        if "o" in case and not s.features().observed_reads:
            continue
        if "r" in case and not s.features().rcw:
            continue
        out.append(Instance(f"{case}-gen-{len(out)}", case, s, "generated"))
        if "o" in case and len(out) < n and rng.random() < 0.4:
            r = _randomize_observations(s, truth.results, rng)
            if r.features().observed_reads:
                out.append(Instance(f"{case}-rnd-{len(out)}", case, r, "randomized"))
    return out


# --------------------------------------------------------------------------- adversarial suite

def _doc(sid: str, blocks: int, k: int, threads: list[tuple[str, list[dict]]], init=None) -> dict:
    return {"format": "setup", "version": 2, "id": sid, "blocks": blocks, "sync_points": k,
            "init": init if init is not None else ["*"] * blocks,
            "threads": [{"id": t, "steps": st} for t, st in threads]}


def R(i, b, obs=None):
    d = {"done": i} if obs is None else {"done": i, "data": obs}
    return [{"read": b, "id": i}, d]


def W(i, b, data):
    return [{"write": b, "id": i, "data": data}, {"done": i}]


def C(i, b, expect, data, obs=None):
    d = {"done": i} if obs is None else {"done": i, "data": obs}
    return [{"rcw": b, "id": i, "expect": expect, "data": data}, d]


def suite() -> list[Instance]:
    """Hand-made instances: edge cases and known traps. Expected answers come from the oracle."""
    docs: list[tuple[str, dict]] = [
        # --- b: structure edge cases
        ("b", _doc("b-single", 1, 0, [("t0", W("w1", 0, 1) + R("r1", 0))])),
        ("b", _doc("b-empty-thread", 1, 0, [("t0", []), ("t1", W("w1", 0, 2)), ("t2", R("r1", 0))])),
        ("b", _doc("b-inflight", 1, 0, [("t0", [{"write": 0, "id": "w1", "data": 1}, {"write": 0, "id": "w2", "data": 2},
                                                {"done": "w2"}, {"done": "w1"}]), ("t1", R("r1", 0) + R("r2", 0))])),
        # joint-only values: r2's value depends on what r1 saw (read-dependent data)
        ("b", _doc("b-dataflow", 2, 0, [("t0", R("r1", 1) + W("w1", 0, "r1~7")), ("t1", W("w2", 1, 5)),
                                        ("t2", R("r2", 0) + R("r3", 1))], init=[0, 0])),
        ("b", _doc("b-nested", 2, 0, [("t0", R("r1", 0) + R("r2", 1) + W("w1", 0, "r2~(r1~3)")),
                                      ("t1", W("w2", 1, "*") + W("w3", 0, 4)), ("t2", R("r3", 0))])),
        # --- s: sync edge cases
        ("s", _doc("s-unused", 1, 1, [("t0", W("w1", 0, 1)), ("t1", R("r1", 0))])),
        ("s", _doc("s-barrier", 1, 1, [("t0", W("w1", 0, 1) + [{"at": 0}] + W("w2", 0, 2)),
                                       ("t1", R("r1", 0) + [{"at": 0}] + R("r2", 0))])),
        ("s", _doc("s-chain", 2, 2, [("t0", W("w1", 0, 1) + [{"before": 0}]), ("t1", [{"after": 0}] + R("r1", 0) +
                                     W("w2", 1, "r1~2") + [{"before": 1}]), ("t2", [{"after": 1}] + R("r2", 1))])),
        ("s", _doc("s-before-after", 1, 1, [("t0", [{"before": 0}] + W("w1", 0, 3) + [{"after": 0}]), ("t1", R("r1", 0))])),
        # --- o: observation traps
        ("o", _doc("o-compound-pin", 2, 0, [("t0", R("r1", 1) + W("w1", 0, "r1~7")), ("t1", W("w2", 1, 5)),
                                            ("t2", R("r2", 0, "5~7"))], init=[0, 0])),
        ("o", _doc("o-unobserved-feeder", 2, 0, [("t0", R("r1", 1) + W("w1", 0, "r1~1")), ("t1", W("w2", 1, 8) + W("w3", 1, 9)),
                                                 ("t2", R("r2", 0, "9~1") + R("r3", 1))], init=[0, 0])),
        ("o", _doc("o-order", 1, 0, [("t0", W("w1", 0, 1)), ("t1", W("w2", 0, 2)), ("t2", R("r1", 0, 1) + R("r2", 0, 2) + R("r3", 0))], init=[0])),
        ("o", _doc("o-infeasible", 1, 0, [("t0", W("w1", 0, 1) + W("w2", 0, 2)), ("t1", R("r1", 0, 2) + R("r2", 0, 1))], init=[0])),
        ("o", _doc("o-repeated", 1, 0, [("t0", W("w1", 0, 1)), ("t1", W("w2", 0, 1)), ("t2", R("r1", 0, 1) + R("r2", 0, 0))], init=[0])),
        ("o", _doc("o-unknown-symbol", 1, 0, [("t0", W("w1", 0, "*")), ("t1", R("r1", 0, "w1") + R("r2", 0))])),
        # --- so: barriers do NOT split feasibility when values cross them
        ("so", _doc("so-cross-barrier", 2, 1, [("t0", W("w1", 0, 1) + [{"at": 0}] + R("r1", 1)),
                                               ("t1", R("r2", 0) + [{"at": 0}] + W("w2", 1, "r2~2")),
                                               ("t2", W("w3", 0, 3) + [{"at": 0}])], init=[0, 0])),
        ("so", _doc("so-cross-barrier-obs", 2, 1, [("t0", W("w1", 0, 1) + [{"at": 0}] + R("r1", 1, "3~2")),
                                                   ("t1", R("r2", 0) + [{"at": 0}] + W("w2", 1, "r2~2")),
                                                   ("t2", W("w3", 0, 3) + [{"at": 0}])], init=[0, 0])),
        # --- RCW: success depends on the value found; data flows back into the block
        ("br", _doc("br-mutex", 1, 0, [("t0", C("c1", 0, 0, 1)), ("t1", C("c2", 0, 0, 2)), ("t2", R("r1", 0))], init=[0])),
        ("br", _doc("br-aba", 1, 0, [("t0", W("w1", 0, 1) + W("w2", 0, 0)), ("t1", C("c1", 0, 0, 9) + R("r1", 0))], init=[0])),
        ("br", _doc("br-expect-from-read", 1, 0, [("t0", R("r1", 0) + C("c1", 0, "r1", 8)), ("t1", W("w1", 0, 3))], init=[0])),
        ("br", _doc("br-chain", 2, 0, [("t0", R("r9", 1) + C("c1", 0, 0, "r9~1")),
                                       ("t1", C("c2", 1, 0, 5)), ("t2", C("c3", 0, "5~1", 7) + R("r1", 0))], init=[0, 0])),
        ("br", _doc("br-unknown", 1, 0, [("t0", W("w1", 0, "*")), ("t1", C("c1", 0, 0, 4)), ("t2", R("r1", 0))], init=[0])),
        ("sr", _doc("sr-barrier-cas", 1, 1, [("t0", C("c1", 0, 0, 1) + [{"at": 0}]), ("t1", C("c2", 0, 0, 2) + [{"at": 0}] + R("r1", 0))], init=[0])),
        ("or", _doc("or-cas-observed", 1, 0, [("t0", C("c1", 0, 0, 1, obs=2)), ("t1", C("c2", 0, 0, 2))], init=[0])),
        ("or", _doc("or-cas-failed-observed", 1, 0, [("t0", W("w1", 0, 1)), ("t1", C("c1", 0, 0, 5, obs=1) + R("r1", 0, 1))], init=[0])),
        ("or", _doc("or-cas-impossible", 1, 0, [("t0", C("c1", 0, 0, 1, obs=7))], init=[0])),
        ("or", _doc("or-read-sees-cas", 1, 0, [("t0", C("c1", 0, 0, 3)), ("t1", W("w1", 0, 1)), ("t2", R("r1", 0, 3) + R("r2", 0, 1))], init=[0])),
        ("sor", _doc("sor-cross-barrier-cas", 2, 1, [("t0", C("c1", 0, 0, 1) + [{"at": 0}] + R("r1", 1, "1~2")),
                                                     ("t1", R("r2", 0) + [{"at": 0}] + C("c2", 1, 0, "r2~2")),
                                                     ("t2", C("c3", 0, 0, 3) + [{"at": 0}])], init=[0, 0])),
        ("so", _doc("so-sync-infeasible", 1, 1, [("t0", W("w1", 0, 1) + [{"before": 0}]), ("t1", [{"after": 0}] + R("r1", 0, 0))], init=[0])),
    ]
    out = []
    for case, d in docs:
        try:
            out.append(Instance(d["id"], case, Setup.from_doc(d), "suite"))
        except MalformedSetup as ex:  # a broken suite entry is a harness bug
            raise RuntimeError(f"suite instance {d['id']}: {ex}") from None
    return out


BUDGETS = {  # per case: (generated instances, max |Lin|, max actions)
    "small": (12, 3000, 7),
    "full": (40, 6000, 8),
}


_MEMO: dict = {}


def instances(cases: list[str], budget: str, seed: int = 0) -> list[Instance]:
    """The same objects for the same arguments, so oracle answers can be cached."""
    n, max_lin, max_actions = BUDGETS[budget]
    if "suite" not in _MEMO:
        _MEMO["suite"] = suite()
    out = [i for i in _MEMO["suite"] if i.case in cases]
    for c in cases:
        key = (c, budget, seed)
        if key not in _MEMO:
            _MEMO[key] = generated(c, n, seed, max_lin, max_actions)
        out += _MEMO[key]
    return out
