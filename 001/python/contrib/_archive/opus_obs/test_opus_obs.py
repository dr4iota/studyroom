"""Tests for the opus observed-reads enumerators. Run from ``python/``:

    python3 -m unittest contrib._archive.opus_obs.test_opus_obs -v

Every instance is checked against the brute-force oracle ``backtrack-feasible`` /
``enum-count`` (small instances only: <= ~10 actions and <= 20k linearizations).
"""

from __future__ import annotations

import os
import random
import subprocess
import sys
import tempfile
import unittest

import contrib._archive.opus_obs  # noqa: F401  (registers the algorithms)
from abio.gen import generate
from abio.lin.backtrack import linear_extensions
from abio.lin.dp import count_linearizations
from abio.lin.feasible import EnumerationCounter, FeasibleBacktrack
from abio.model import Setup
from abio.registry import available
from abio.semantics import is_feasible
from contrib._archive.opus_obs.core import ObsModel, is_feasible_fast

ENUMS = ["opus-o-filter", "opus-o-prune", "opus-o-memo", "opus-o-split"]
COUNTERS = ["opus-o-dpcount", "opus-o-splitcount"]
LIMIT = 20_000
HERE = os.path.dirname(os.path.abspath(__file__))
PYROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "abio").is_dir()).__str__()


def mk(threads: list[list[dict]], init=(0,), blocks: int = 1, K: int = 0) -> Setup:
    return Setup.from_doc({
        "format": "setup", "version": 2, "id": "h", "blocks": blocks, "sync_points": K, "init": list(init),
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
    K = kw.get("K", rng.choice([0, 1, 2]))
    hp = {"seed": s, "threads": kw.get("T", rng.choice([2, 3])), "blocks": kw.get("B", rng.choice([1, 1, 2])),
          "actions_per_thread": kw.get("A", rng.choice([2, 3])), "max_in_flight": rng.choice([1, 2, 3]),
          "sync_points": K, "events_per_thread": min(kw.get("E", rng.choice([0, 1, 2])), 3 * K) if K else 0,
          "relations": kw.get("rel", ["before", "after", "at"]),
          "content": {"classes": {"const": 1.0}, "value_pool": kw.get("P", rng.choice([1, 2, 3]))},
          "knowledge": {"p_w": kw.get("pw", 1.0), "p_r": kw.get("pr", 0.7), "init_known": kw.get("ik", 1.0)}}
    return generate(hp)[0]


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
            self.assertTrue(algo.capabilities.observed_reads and algo.capabilities.sync)
            self.assertFalse(algo.capabilities.rcw)
            seen = set()
            for o in algo.enumerate(setup):
                self.assertNotIn(o, seen, f"{name}: duplicate")
                seen.add(o)
                self.assertIn(o, ref, f"{name}: infeasible or invalid output {P.to_names(o)}")
            self.assertEqual(seen, ref, f"{name}: missing outputs")
        # every oracle output is valid and feasible (spot-check the oracle and the API)
        for o in list(ref)[:200]:
            self.assertEqual(P.check(P.to_names(o)), [])
            self.assertTrue(is_feasible(setup, o))
        creg = available("lin-count")
        for name in COUNTERS:
            r = creg[name]().count(setup)
            self.assertEqual(r.linearizations, nl, name)
            self.assertEqual(r.feasible if observed else r.linearizations, nf, name)
            if not observed:
                self.assertIsNone(r.feasible)
        return nf

    def check_fast(self, setup: Setup) -> None:
        m = ObsModel(setup)
        for o in linear_extensions(setup):
            self.assertEqual(is_feasible_fast(setup, o, m), is_feasible(setup, o), setup.poset.to_names(o))


class TestHandMade(Base):
    def test_no_observations(self):
        s = mk([W("w1", 1) + R("r1"), W("w2", 2) + R("r2")])
        self.assertEqual(self.check(s), count_linearizations(s))

    def test_observed_init_forces_read_first(self):
        # r1 sees init 0: it must take effect before both writes
        s = mk([R("r1", 0), W("w1", 1), W("w2", 2)])
        n = self.check(s)
        self.assertGreater(n, 0)
        self.assertLess(n, count_linearizations(s))
        P = s.poset
        for o in FeasibleBacktrack().enumerate(s):
            pos = P.positions(o)
            for w in ("w1", "w2"):
                self.assertLess(pos[P.start_node["r1"]], pos[P.done_node[w]])

    def test_only_overlapping_write(self):
        # t0 reads 1 while t1's only write of 1 must overlap it (w1 starts after r1 starts,
        # then r1 ends before w1 ends is fine; w1 entirely after r1 is not)
        s = mk([R("r1", 1), W("w1", 1)])
        self.check(s)
        P = s.poset
        for o in FeasibleBacktrack().enumerate(s):
            pos = P.positions(o)
            self.assertLess(pos[P.start_node["w1"]], pos[P.done_node["r1"]])

    def test_two_reads_force_write_order(self):
        # one thread reads 1 then 2; writers of 1 and 2 in other threads
        s = mk([R("r1", 1) + R("r2", 2), W("w1", 1), W("w2", 2)])
        self.check(s)

    def test_new_old_inversion(self):
        # r1 sees 2 then r2 sees 1: w2 before w1 in effect order
        s = mk([R("r1", 2) + R("r2", 1), W("w1", 1), W("w2", 2)])
        self.check(s)

    def test_infeasible_by_sync(self):
        # w2 (value 2) is forced before w1 (value 1) by sync; r1 after w1 sees 2: impossible
        s = mk([[{"after": 0}] + W("w1", 1) + R("r1", 2), W("w2", 2) + [{"before": 0}]], K=1)
        self.check(s, expect=0)

    def test_infeasible_by_barrier(self):
        s = mk([W("w1", 1) + [{"at": 0}] + R("r1", 0), [{"at": 0}] + W("w2", 2)], K=1)
        self.check(s, expect=0)

    def test_value_nobody_writes(self):
        s = mk([W("w1", 1) + R("r1", 7), W("w2", 2)])
        self.check(s, expect=0)

    def test_repeated_constants_need_two_writers(self):
        # reads 1, 2, 1 in program order: needs w1 < w2 < w3 or w3 < w2 < w1 (both value 1)
        s = mk([R("r1", 1) + R("r2", 2) + R("r3", 1), W("w1", 1) + W("w3", 1), W("w2", 2)])
        self.assertGreater(self.check(s), 0)

    def test_repeated_constants_one_writer_infeasible(self):
        s = mk([R("r1", 1) + R("r2", 2) + R("r3", 1), W("w1", 1), W("w2", 2)])
        self.check(s, expect=0)

    def test_unknown_symbol(self):
        s = mk([[{"write": 0, "id": "w1", "data": "*"}, {"done": "w1"}], R("r1", "w1") + R("r2", 3), W("w2", 3)])
        self.check(s)

    def test_unknown_init(self):
        s = mk([R("r1", "init.0") + R("r2", 1), W("w1", 1)], init=["*"])
        self.check(s)

    def test_init_equals_written_constant(self):
        # the value 0 is both init and w1's constant: r2 may read either
        s = mk([R("r1", 1) + R("r2", 0), W("w1", 0), W("w2", 1)])
        self.assertGreater(self.check(s), 0)

    def test_async_overlap(self):
        # in-flight actions on one thread
        s = mk([[{"write": 0, "id": "w1", "data": 1}, {"read": 0, "id": "r1"}, {"done": "w1"},
                 {"done": "r1", "data": 2}], W("w2", 2) + R("r2", 1)])
        self.check(s)

    def test_two_blocks_independent(self):
        s = mk([W("a1", 1, 0) + R("rb", 2, 1), W("b1", 2, 1) + R("ra", 1, 0)], init=[0, 0], blocks=2)
        self.check(s)

    def test_cluster_cycle(self):
        # classic 2-cycle: two writes, each with a reader, that must overlap both ways
        s = mk([W("w1", 1) + R("r2", 2), W("w2", 2) + R("r1", 1)])
        self.check(s)

    def test_fast_on_hand_made(self):
        for s in [
            mk([R("r1", 1) + R("r2", 2) + R("r3", 1), W("w1", 1), W("w2", 2), W("w3", 1)]),
            mk([W("w1", 1) + R("r2", 2), W("w2", 2) + R("r1", 1)]),
            mk([R("r1", 1) + R("r2", 1), W("w1", 1) + W("w2", 2), W("w3", 1)]),
        ]:
            self.check_fast(s)


class TestGenerated(Base):
    def sweep(self, seeds, **kw):
        n = feas_total = infeasible = 0
        for s in seeds:
            setup = gen(s, **kw)
            if len(setup.actions) > 10 or count_linearizations(setup) > LIMIT:
                continue
            nf = self.check(setup)
            n += 1
            feas_total += nf
            infeasible += nf < count_linearizations(setup)
        self.assertGreater(n, 0)
        return n, infeasible

    def test_pr_pw_grid(self):
        for pr in (0.0, 0.3, 0.7, 1.0):
            for pw in (1.0, 0.7):
                with self.subTest(pr=pr, pw=pw):
                    self.sweep(range(12), pr=pr, pw=pw, ik=0.5)

    def test_no_sync(self):
        self.sweep(range(100, 130), K=0, pr=1.0)

    def test_sync(self):
        for rel in (["before"], ["after"], ["at"], ["before", "after", "at"]):
            with self.subTest(rel=rel):
                self.sweep(range(200, 215), K=2, E=2, rel=rel, pr=1.0)

    def test_single_block_many_threads(self):
        self.sweep(range(300, 330), B=1, T=3, A=2, P=2, pr=1.0, K=1, E=1, rel=["at"])
        self.sweep(range(300, 330), B=1, T=3, A=3, P=2, pr=1.0, K=2, E=2, rel=["at"])
        self.sweep(range(300, 320), B=1, T=4, A=2, P=1, pr=1.0, K=2, E=2, rel=["at"])

    def test_fast_vs_semantics(self):
        m = 0
        for s in range(400, 440):
            setup = gen(s, pr=1.0, P=2)
            if len(setup.actions) > 9 or count_linearizations(setup) > 3000:
                continue
            self.check_fast(setup)
            m += 1
        self.assertGreater(m, 5)


class TestCLI(unittest.TestCase):
    def test_count_only_matches_enum_count(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "s.yaml")
            run = lambda *a: subprocess.run([sys.executable, "-m", "abio", *a], cwd=PYROOT, check=True,
                                            capture_output=True, text=True).stdout
            run("gen", "--set", "content.classes={const: 1.0}", "--set", "knowledge.p_r=0.5", "--set", "content.value_pool=2", "--set", "sync_points=1",
                "--set", "events_per_thread=1", "-o", f)
            ref = run("lin", "count", f, "--algo", "enum-count")
            feas = int([ln for ln in ref.splitlines() if ln.strip().startswith("feasible")][0].split(":")[1])
            for name in ENUMS:
                out = run("lin", "enum", f, "--plugin", "contrib._archive.opus_obs", "--algo", name, "--count-only")
                self.assertEqual(out.split()[0], str(feas), name)
            for name in COUNTERS:
                out = run("lin", "count", f, "--plugin", "contrib._archive.opus_obs", "--algo", name)
                self.assertIn(f"feasible: {feas}", out, name)


if __name__ == "__main__":
    unittest.main()
