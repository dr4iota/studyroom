"""Tests for the opus read-dependent-data enumerators. Run from ``python/``:

    python3 -m unittest contrib.linear_opus55_1.obs.test_opus_dep -v

Every instance is checked against the brute-force oracles ``backtrack-feasible`` /
``enum-count`` (small instances only: <= ~10 actions and <= 20k linearizations), and every
output against ``poset.check`` and ``semantics.is_feasible``.
"""

from __future__ import annotations

import os
import random
import subprocess
import sys
import tempfile
import unittest

import contrib.linear_opus55_1.obs  # noqa: F401  (registers the algorithms)
from abio import terms as T
from abio.gen import generate
from abio.lin.backtrack import linear_extensions
from abio.lin.dp import count_linearizations
from abio.lin.feasible import EnumerationCounter, FeasibleBacktrack
from abio.model import Setup
from abio.registry import available
from abio.semantics import is_feasible, iter_schedules
from contrib.linear_opus55_1.obs.core import DepModel, is_feasible_fast, static_pins
from contrib.linear_opus55_1.obs.enumerators import enum_filter

ENUMS = ["opus55-o-filter", "opus55-o-prune", "opus55-o-memo", "opus55-o-split"]
COUNTERS = ["opus55-o-dpcount", "opus55-o-splitcount"]
LIMIT = 20_000
HERE = os.path.dirname(os.path.abspath(__file__))
PYROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "abio").is_dir()).__str__()


def mk(threads: list[list[dict]], init=(0,), blocks: int | None = None) -> Setup:
    init = list(init)
    return Setup.from_doc({
        "format": "setup", "version": 2, "id": "h", "blocks": blocks or len(init), "sync_points": 0, "init": init,
        "threads": [{"id": f"t{i}", "steps": s} for i, s in enumerate(threads)],
    })


def W(aid: str, v, b: int = 0) -> list[dict]:
    return [{"write": b, "id": aid, "data": v}, {"done": aid}]


def R(aid: str, v=None, b: int = 0) -> list[dict]:
    d = {"done": aid}
    if v is not None:
        d["data"] = v
    return [{"read": b, "id": aid}, d]


def gen(s: int, **kw) -> Setup:
    rng = random.Random(s)
    cls = kw.get("cls") or rng.choice([{"const": 1.0}, {"copy": 1.0}, {"combine": 1.0},
                                       {"const": 0.3, "copy": 0.4, "combine": 0.3}])
    hp = {"seed": s, "threads": kw.get("T", rng.choice([2, 3])), "blocks": kw.get("B", rng.choice([1, 2, 3])),
          "actions_per_thread": kw.get("A", rng.choice([2, 3, 4])), "max_in_flight": rng.choice([1, 2, 3]),
          "kind_mix": {"read": 0.55, "write": 0.45},
          "content": {"classes": cls, "max_depth": rng.choice([1, 2, 3]), "value_pool": kw.get("P", rng.choice([1, 2, 3]))},
          "knowledge": {"p_w": kw.get("pw", rng.choice([1.0, 0.7])), "p_r": kw.get("pr", 0.7),
                        "init_known": kw.get("ik", 0.5)}}
    return generate(hp)[0]


def small(setup: Setup) -> bool:
    return len(setup.actions) <= 10 and count_linearizations(setup) <= LIMIT


class Base(unittest.TestCase):
    def check(self, setup: Setup, expect: int | None = None) -> int:
        """All enumerators and counters vs the oracle; returns |LinFeas|."""
        nl = count_linearizations(setup)
        self.assertLessEqual(nl, LIMIT, "test instance too large for the oracle")
        observed = setup.features().observed_reads
        ref = set(FeasibleBacktrack().enumerate(setup))
        cnt = EnumerationCounter().count(setup)
        nf = cnt.feasible if observed else cnt.linearizations
        self.assertEqual(len(ref), nf)
        if expect is not None:
            self.assertEqual(nf, expect)
        P = setup.poset
        reg = available("lin-enum")
        for name in ENUMS:
            algo = reg[name]()
            caps = algo.capabilities
            self.assertTrue(caps.observed_reads)
            self.assertFalse(caps.rcw or caps.sync)
            seen = set()
            for o in algo.enumerate(setup):
                self.assertNotIn(o, seen, f"{name}: duplicate")
                seen.add(o)
                self.assertIn(o, ref, f"{name}: infeasible or invalid output {P.to_names(o)}")
            self.assertEqual(seen, ref, f"{name}: missing outputs")
        self.assertEqual(set(enum_filter(setup, pins=True)), ref, "filter with pins")
        for o in list(ref)[:300]:
            self.assertEqual(P.check(P.to_names(o)), [])
            self.assertTrue(is_feasible(setup, o))
        creg = available("lin-count")
        for name in COUNTERS:
            for pins in ("1", "0"):
                r = creg[name](pins=pins).count(setup)
                self.assertEqual(r.linearizations, nl, name)
                self.assertEqual(r.feasible if observed else r.linearizations, nf, name)
                if not observed:
                    self.assertIsNone(r.feasible)
        return nf

    def check_fast(self, setup: Setup) -> int:
        m = DepModel(setup)
        k = 0
        for o in linear_extensions(setup):
            self.assertEqual(is_feasible_fast(setup, o, m), is_feasible(setup, o), setup.poset.to_names(o))
            k += 1
        return k


class TestHandMade(Base):
    def test_no_observations(self):
        s = mk([R("r1") + W("w1", "r1~1"), W("w2", 2) + R("r2")])
        self.assertEqual(self.check(s), count_linearizations(s))

    def test_compound_pins_inner_read_init(self):
        # r2 sees init.1~7: w1 = r1~7 was read, and r1 must have seen init.1 (before w2)
        s = mk([R("r1", b=1) + W("w1", "r1~7", 0), W("w2", 5, 1), R("r2", "init.1~7", 0)], init=[0, "*"])
        n = self.check(s)
        self.assertGreater(n, 0)
        P = s.poset
        for o in FeasibleBacktrack().enumerate(s):
            pos = P.positions(o)
            self.assertLess(pos[P.start_node["r1"]], pos[P.done_node["w2"]])
            self.assertLess(pos[P.start_node["w1"]], pos[P.done_node["r2"]])
        self.assertTrue(static_pins(DepModel(s)))  # term structure gives pins

    def test_compound_pins_inner_read_write(self):
        # an unobserved read (r1) feeding a write whose content is observed elsewhere
        s = mk([R("r1", b=1) + W("w1", "r1~7", 0), W("w2", 5, 1), R("r2", "5~7", 0)], init=[0, "*"])
        n = self.check(s)
        self.assertGreater(n, 0)
        P = s.poset
        for o in FeasibleBacktrack().enumerate(s):
            pos = P.positions(o)
            self.assertLess(pos[P.start_node["w2"]], pos[P.done_node["r1"]])

    def test_chain_across_blocks(self):
        # r1 (b1) feeds w1 (b0), read by r2, which feeds w2 (b1), observed by r3
        s = mk([R("r1", b=1) + W("w1", "r1~1", 0), R("r2", b=0) + W("w2", "r2~2", 1), R("r3", "init.1~1~2", 1)],
               init=[0, "*"])
        self.assertGreater(self.check(s), 0)

    def test_chain_across_blocks_other_inner(self):
        s = mk([R("r1", b=1) + W("w1", "r1~1", 0), R("r2", b=0) + W("w2", "r2~2", 1), R("r3", "0~2", 1)],
               init=[0, "*"])
        self.assertGreater(self.check(s), 0)

    def test_circular_justification_infeasible(self):
        # r1 would have to read w2 = r2~2 with r2 = w1 = r1~1: a cycle; both observed
        s = mk([R("r1", "init.0~1~2", b=1) + W("w1", "r1~1", 0), R("r2", "init.0~1", b=0) + W("w2", "r2~2", 1)],
               init=["*", "*"])
        self.check(s, expect=0)

    def test_pure_copies(self):
        # copies without tags: values can travel unchanged through several writes
        s = mk([R("r1") + W("w1", "r1"), R("r2") + W("w2", "r2"), R("r3", "init.0")], init=["*"])
        self.check(s)
        s = mk([R("r1") + W("w1", "r1"), W("w2", 4) + R("r2", 4), R("r3", 4)], init=["*"])
        self.check(s)

    def test_same_compound_from_two_threads(self):
        s = mk([R("r1", b=1) + W("w1", "r1~7", 0), R("r2", b=1) + W("w2", "r2~7", 0), R("r3", "init.1~7", 0)],
               init=[0, "*"])
        self.assertGreater(self.check(s), 0)
        s = mk([W("w3", 3, 1) + R("r1", b=1) + W("w1", "r1~7", 0), R("r2", b=1) + W("w2", "r2~7", 0),
                R("r3", "3~7", 0)], init=[0, "*"])
        self.check(s)

    def test_impossible_inner_part(self):
        s = mk([R("r1", b=1) + W("w1", "r1~7", 0), W("w2", 5, 1), R("r2", "9~7", 0)], init=[0, "*"])
        self.check(s, expect=0)
        self.assertIsNone(static_pins(DepModel(s)))

    def test_inner_part_contradicts_observation(self):
        # r1 observed 5 but r2's compound says r1 saw init.1
        s = mk([R("r1", 5, b=1) + W("w1", "r1~7", 0), W("w2", 5, 1), R("r2", "init.1~7", 0)], init=[0, "*"])
        self.check(s, expect=0)

    def test_write_references_write(self):
        s = mk([R("r1", b=1) + W("w1", "r1~4", 0) + W("w2", "w1~5", 1), R("r2", "init.1~4~5", 1)], init=[0, "*"])
        self.assertGreater(self.check(s), 0)
        s = mk([[{"write": 0, "id": "w1", "data": "*"}, {"done": "w1"}] + R("r1", b=1) + W("w2", "w1~r1", 1),
                W("w3", 6, 1), R("r2", "w1~6", 1)], init=[0, 0])
        self.assertGreater(self.check(s), 0)

    def test_non_commutative(self):
        s = mk([R("r1", b=1) + W("w1", "r1~7", 0), W("w2", 5, 1), R("r2", "7~5", 0)], init=[0, "*"])
        self.check(s, expect=0)

    def test_two_reads_combined(self):
        s = mk([R("r1", b=0) + R("r2", b=1) + W("w1", "r1~(r2~1)", 0), W("w2", 3, 0) + W("w3", 4, 1),
                R("r3", "3~(init.1~1)", 0)], init=["*", "*"])
        self.assertGreater(self.check(s), 0)

    def test_constant_data_cases(self):
        self.check(mk([R("r1", 1) + R("r2", 2) + R("r3", 1), W("w1", 1) + W("w3", 1), W("w2", 2)]))
        self.check(mk([R("r1", 1) + R("r2", 2) + R("r3", 1), W("w1", 1), W("w2", 2)]), expect=0)
        self.check(mk([W("w1", 1) + R("r2", 2), W("w2", 2) + R("r1", 1)]))

    def test_async_in_flight(self):
        s = mk([[{"read": 1, "id": "r1"}, {"read": 0, "id": "r0"}, {"done": "r1"}, {"write": 0, "id": "w1", "data": "r1~1"},
                 {"done": "r0", "data": 2}, {"done": "w1"}],
                W("w2", 2, 0) + W("w3", 8, 1) + R("r2", "8~1", 0)], init=[0, 0])
        self.check(s)

    def test_fast_on_hand_made(self):
        for s in [
            mk([R("r1", b=1) + W("w1", "r1~7", 0), R("r2", b=1) + W("w2", "r2~7", 0), R("r3", "init.1~7", 0)], init=[0, "*"]),
            mk([R("r1", b=1) + W("w1", "r1~1", 0), R("r2", b=0) + W("w2", "r2~2", 1), R("r3", "init.1~1~2", 1)], init=[0, "*"]),
            mk([R("r1") + W("w1", "r1"), R("r2") + W("w2", "r2"), R("r3", "init.0")], init=["*"]),
        ]:
            self.check_fast(s)


def mutate(setup: Setup, rng: random.Random) -> Setup:
    """Replace some observed terms by random terms (subterms of plausible values)."""
    pool: list = [T.Init(b) for b in range(setup.blocks)] + list(setup.init)
    for a in setup.actions.values():
        if a.kind == "write":
            pool.append(setup.static_content(a.id) if not setup.depends_on_reads(a.id) else T.Const(rng.randint(1, 3)))
        if a.observed is not None:
            pool.append(a.observed)
    doc = setup.to_doc()
    changed = False
    for th in doc["threads"]:
        for s in th["steps"]:
            if "done" in s and setup.actions[s["done"]].kind == "read" and rng.random() < 0.5:
                t = rng.choice(pool)
                if rng.random() < 0.5:
                    t = T.Pair(t, T.Const(rng.randint(1, 3)))
                s["data"] = T.to_value(t)
                changed = True
    return Setup.from_doc(doc) if changed else setup


class TestGenerated(Base):
    def sweep(self, seeds, **kw):
        n = infeasible = 0
        for s in seeds:
            setup = gen(s, **kw)
            if not small(setup):
                continue
            nf = self.check(setup)
            n += 1
            infeasible += nf < count_linearizations(setup)
        self.assertGreater(n, 0)
        return n, infeasible

    def test_grid(self):
        for cls in ({"const": 1.0}, {"copy": 1.0}, {"combine": 1.0}, {"const": 0.2, "copy": 0.4, "combine": 0.4}):
            for pr in (0.0, 0.3, 0.7, 1.0):
                for pw in (1.0, 0.7):
                    with self.subTest(cls=cls, pr=pr, pw=pw):
                        self.sweep(range(6), cls=cls, pr=pr, pw=pw)

    def test_blocks_and_pools(self):
        for B in (1, 2, 3):
            for P in (1, 2, 3):
                with self.subTest(B=B, P=P):
                    self.sweep(range(20 + 10 * B + P, 28 + 10 * B + P), B=B, P=P, pr=1.0,
                               cls={"copy": 0.5, "combine": 0.5})

    def test_dependent_data_sweep(self):
        # only instances whose observed reads really depend on read-dependent writes
        n = infeasible = 0
        for s in range(800, 1100):
            setup = gen(s, T=2, A=4, pr=0.8, cls={"const": 0.1, "copy": 0.45, "combine": 0.45})
            if not setup.has_data_from_reads() or not setup.features().observed_reads or not small(setup):
                continue
            nf = self.check(setup)
            n += 1
            infeasible += nf < count_linearizations(setup)
            if n >= 40:
                break
        self.assertGreaterEqual(n, 40)
        self.assertGreater(infeasible, 10)

    def test_random_observations(self):
        rng = random.Random(5)
        n = zero = 0
        for s in range(500, 560):
            setup = gen(s, pr=0.7, cls={"copy": 0.5, "combine": 0.5})
            if not small(setup):
                continue
            m = mutate(setup, rng)
            nf = self.check(m)
            n += 1
            zero += nf == 0
        self.assertGreater(n, 10)
        self.assertGreater(zero, 0)

    def test_fast_vs_semantics(self):
        m = 0
        for s in range(600, 660):
            setup = gen(s, pr=1.0, P=2, cls={"const": 0.2, "copy": 0.4, "combine": 0.4})
            if len(setup.actions) > 9 or count_linearizations(setup) > 3000:
                continue
            self.check_fast(setup)
            m += 1
        self.assertGreater(m, 5)

    def test_witness_from_oracle_is_consistent(self):
        # the oracle's own schedules agree with our test on a few instances (sanity)
        for s in range(700, 720):
            setup = gen(s, pr=1.0, cls={"copy": 1.0})
            if not small(setup):
                continue
            mdl = DepModel(setup)
            for o in list(linear_extensions(setup))[:50]:
                has = next(iter_schedules(setup, o), None) is not None
                self.assertEqual(has, is_feasible_fast(setup, o, mdl))


class TestCLI(unittest.TestCase):
    def test_count_only_matches_enum_count(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "s.yaml")
            run = lambda *a: subprocess.run([sys.executable, "-m", "abio", *a], cwd=PYROOT, check=True,
                                            capture_output=True, text=True).stdout
            run("gen", "--set", "knowledge.p_r=0.6", "--set", "content.value_pool=2",
                "--set", "content.classes={const: 0.3, copy: 0.4, combine: 0.3}", "-o", f)
            ref = run("lin", "count", f, "--algo", "enum-count")
            feas = int([ln for ln in ref.splitlines() if ln.strip().startswith("feasible")][0].split(":")[1])
            for name in ENUMS:
                out = run("lin", "enum", f, "--plugin", "contrib.linear_opus55_1.obs", "--algo", name, "--count-only")
                self.assertEqual(out.split()[0], str(feas), name)
            for name in COUNTERS:
                out = run("lin", "count", f, "--plugin", "contrib.linear_opus55_1.obs", "--algo", name)
                self.assertIn(f"feasible: {feas}", out, name)


if __name__ == "__main__":
    unittest.main()
