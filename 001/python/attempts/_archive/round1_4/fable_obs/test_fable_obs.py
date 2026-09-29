"""Tests for the ``fable-o-*`` feasible-linearization algorithms.  Run from ``python/``:

    ulimit -v 2000000; timeout 600 python3 -m unittest attempts._archive.round1_4.fable_obs.test_fable_obs -v

Checks, for every enumerator and every instance: each output is a valid linearization
(``poset.check``) and feasible (``harness.semantics.is_feasible``), there are no
duplicates, the set of outputs equals the set produced by ``backtrack-feasible``, and
the count equals ``enum-count``'s ``feasible`` (``linearizations`` without
observations). ``fable-o-count`` is compared with ``enum-count``. Both fixed-``L``
tests are differentially tested against the oracle on every linearization of every
oracle instance. Oracle instances are small (about 10 actions, at most 20 000
linearizations); larger instances compare the algorithms with each other only. Nothing
large is ever materialised.
"""

from __future__ import annotations

import itertools
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "harness").is_dir()).__str__()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import harness.lin  # noqa: E402,F401  (register built-ins)
from harness.formats import load_setup  # noqa: E402
from harness.gen import generate  # noqa: E402
from harness.lin.dp import count_linearizations  # noqa: E402
from harness.lin.feasible import EnumerationCounter, FeasibleBacktrack  # noqa: E402
from harness.lin.backtrack import linear_extensions  # noqa: E402
from harness.model import Setup  # noqa: E402
from harness.semantics import is_feasible  # noqa: E402

from attempts._archive.round1_4.fable_obs.auto import FableObsAuto  # noqa: E402
from attempts._archive.round1_4.fable_obs.common import Model, is_feasible_auto, is_feasible_fast  # noqa: E402
from attempts._archive.round1_4.fable_obs.dp import FableObsCount, FableObsDP  # noqa: E402
from attempts._archive.round1_4.fable_obs.filter import FableObsFilter  # noqa: E402
from attempts._archive.round1_4.fable_obs.prune import FableObsPrune  # noqa: E402

ENUMERATORS = [FableObsPrune, FableObsAuto, FableObsDP, FableObsFilter]
ORACLE_LIMIT = 20_000  # |Lin(P)| cap for instances checked against the brute-force oracle
LARGE_LIMIT = 100_000  # |Lin(P)| cap for algorithm-vs-algorithm instances
EXAMPLES = os.path.join(ROOT, "examples")
SCRATCH = "/tmp/claude-1000/-home-hanhua-mix-studyroom-001/15b0fc29-0001-4775-b7f2-5b9a9a58524e/scratchpad/fable_obs"


def doc(threads: list[list[dict]], init: list, sync_points: int = 0, id: str = "fable-obs-case") -> dict:
    return {"format": "setup", "version": 2, "id": id, "blocks": len(init), "sync_points": sync_points,
            "init": init, "threads": [{"id": f"t{t}", "steps": s} for t, s in enumerate(threads)]}


def W(b: int, i: str, data) -> list[dict]:
    return [{"write": b, "id": i, "data": data}, {"done": i}]


def R(b: int, i: str, obs=None) -> list[dict]:
    d = {"done": i} if obs is None else {"done": i, "data": obs}
    return [{"read": b, "id": i}, d]


def hand_made() -> dict[str, tuple[dict, str]]:
    """Adversarial setups: ``name -> (document, expectation)`` with expectation in
    ``none`` (no feasible L), ``some`` (feasible for a proper subset), ``all``."""
    c: dict[str, tuple[dict, str]] = {}
    # two reads of one block observing values in an order that forces w1 before w2
    c["ordered values force write order"] = (doc([W(0, "w1", 1), W(0, "w2", 2), R(0, "r1", 1) + R(0, "r2", 2)], [0]), "some")
    # the same, but the reads are on different threads and overlap: still forces w1 < w2
    c["ordered values, reads on two threads"] = (doc([W(0, "w1", 1), W(0, "w2", 2), R(0, "r1", 1), R(0, "r2", 2)], [0]), "some")
    # a read observing a value only an overlapping write can supply
    c["value from overlapping write"] = (doc([W(0, "w1", 5), R(0, "r1", 5)], [0]), "some")
    c["value from overlapping write, two blocks"] = (doc([W(0, "w1", 5) + W(1, "w2", 6), R(1, "r1", 6) + R(0, "r2", 5)], [0, 0]), "some")
    # an observed initial value forces the read before every write
    c["init forces read first"] = (doc([W(0, "w1", 1), R(0, "r1", 0)], [0]), "some")
    c["init forces read first, unknown init"] = (doc([W(0, "w1", 1), R(0, "r1", "init.0")], ["*"]), "some")
    c["init forces read first, two writes"] = (doc([W(0, "w1", 1) + W(0, "w2", 1), R(0, "r1", 0) + R(0, "r2", 1)], [0]), "some")
    # repeated constants from different writes
    c["repeated constants"] = (doc([W(0, "w1", 1) + W(0, "w2", 2), W(0, "w3", 1), R(0, "r1", 1) + R(0, "r2", 2) + R(0, "r3", 1)], [0]), "some")
    c["repeated constants, all writes equal"] = (doc([W(0, "w1", 1) + W(0, "w2", 1), W(0, "w3", 1), R(0, "r1", 0) + R(0, "r2", 1)], [0]), "some")
    c["repeated constants, init repeats too"] = (doc([W(0, "w1", 1), W(0, "w2", 2), R(0, "r1", 1) + R(0, "r2", 1)], [1]), "some")
    # a read observing an unknown write's symbol
    c["unknown write symbol"] = (doc([W(0, "w1", "*") + W(0, "w2", 3), R(0, "r1", "w1") + R(0, "r2", 3)], [0]), "some")
    c["unknown write symbol, wrong one"] = (doc([W(0, "w1", "*"), W(0, "w2", "*"), R(0, "r1", "w2") + R(0, "r2", "w1")], [0]), "some")
    # infeasible for every L
    c["infeasible: value never written"] = (doc([W(0, "w1", 1), R(0, "r1", 7)], [0]), "none")
    c["infeasible: back to init after a write"] = (doc([R(0, "r1", 1) + R(0, "r2", 0), W(0, "w1", 1)], [0]), "none")
    c["infeasible: unknown symbol of another block"] = (doc([W(1, "w1", "*"), R(0, "r1", "w1")], [0, 0]), "none")
    c["infeasible: sync puts the read after the write"] = (
        doc([W(0, "w1", 1) + [{"before": 0}], [{"after": 0}] + R(0, "r1", 0)], [0], 1), "none")
    c["infeasible: cyclic value order on one thread"] = (
        doc([W(0, "w1", 1) + W(0, "w2", 2), R(0, "r1", 2) + R(0, "r2", 1) + R(0, "r3", 2)], [0]), "none")
    c["infeasible: two blocks, one impossible"] = (doc([W(0, "w1", 1) + W(1, "w2", 1), R(0, "r1", 1) + R(1, "r2", 2)], [0, 0]), "none")
    # sync restricts to a few L
    c["sync: barrier then observed read"] = (
        doc([W(0, "w1", 1) + [{"at": 0}] + W(0, "w2", 2), [{"at": 0}] + R(0, "r1", 1) + R(0, "r2", 2)], [0], 1), "some")
    c["sync: before/after with in-flight write"] = (
        doc([[{"write": 0, "id": "w1", "data": 1}, {"before": 0}, {"done": "w1"}, {"write": 0, "id": "w2", "data": 2}, {"done": "w2"}],
             [{"after": 0}] + R(0, "r1", 0) + R(0, "r2", 2)], [0], 1), "some")
    # everything feasible: observations that every L satisfies
    c["all: single writer, observed after it"] = (doc([W(0, "w1", 1) + R(0, "r1", 1), R(1, "r2", 0)], [0, 0]), "all")
    c["all: no observations"] = (doc([W(0, "w1", 1) + R(0, "r1"), W(0, "w2", 2) + R(0, "r2")], [0]), "all")
    # unobserved reads mixed in; three threads; in-flight reads
    c["mixed unobserved reads"] = (
        doc([W(0, "w1", 1) + R(0, "u1") + W(0, "w2", 2), R(0, "r1", 2) + R(0, "u2"), R(0, "r2", 1)], [0]), "some")
    c["in-flight reads"] = (
        doc([[{"read": 0, "id": "r1"}, {"read": 0, "id": "r2"}, {"done": "r2", "data": 1}, {"done": "r1", "data": 0}], W(0, "w1", 1)], [0]), "some")
    c["in-flight reads, impossible order"] = (
        doc([[{"read": 0, "id": "r1"}, {"read": 0, "id": "r2"}, {"done": "r1", "data": 1}, {"done": "r2", "data": 0}], W(0, "w1", 1)], [0]), "some")
    c["three writers, one reader"] = (
        doc([W(0, "w1", 1), W(0, "w2", 2), W(0, "w3", 1), R(0, "r1", 2) + R(0, "r2", 1)], [0]), "some")
    c["empty"] = (doc([[], []], [0]), "all")
    return c


def generated(seeds=range(3), *, cap=6_000):
    """Generated instances with observations (and some without), small enough for the oracle."""
    shapes = [
        {"threads": 2, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 1},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 3},
        {"threads": 2, "actions_per_thread": 4, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 2, "actions_per_thread": 5, "max_in_flight": 3},
    ]
    for seed in seeds:
        for shape in shapes:
            for K, E, rels in ((0, 0, []), (1, 1, ["before", "after", "at"]), (2, 2, ["before", "after"]), (1, 1, ["at"])):
                for p_r in (0, 0.3, 0.7, 1):
                    for p_w in (1, 0.7):
                        for blocks in (1, 2):
                            hp = {"seed": seed, "blocks": blocks, "sync_points": K, "events_per_thread": E, **shape,
                                  "content": {"classes": {"const": 1.0}, "value_pool": 1 + (seed + blocks) % 3},
                                  "knowledge": {"p_w": p_w, "p_r": p_r, "init_known": 0.5 if seed % 2 else 1.0}}
                            if rels:
                                hp["relations"] = rels
                            try:
                                setup, _ = generate(hp)
                            except RuntimeError:
                                continue
                            if count_linearizations(setup) > cap or len(setup.actions) > 10:
                                continue
                            yield hp, setup


class FableObsTests(unittest.TestCase):
    def check_enum(self, algo, setup, ref: set | None, feasible: int | None, tag: str) -> set:
        """Validity, feasibility, uniqueness and (when ``ref`` is given) set equality; returns the set."""
        P = setup.poset
        seen = set()
        for o in algo.enumerate(setup):
            self.assertEqual(len(o), len(P), f"{algo.name} {tag}: wrong length")
            self.assertEqual(P.check(P.to_names(o)), [], f"{algo.name} {tag}: invalid {o}")
            self.assertNotIn(o, seen, f"{algo.name} {tag}: duplicate {o}")
            seen.add(o)
            if ref is not None:
                self.assertIn(o, ref, f"{algo.name} {tag}: infeasible output {P.to_names(o)}")
        if ref is not None:
            self.assertEqual(seen, ref, f"{algo.name} {tag}: output set differs from backtrack-feasible")
        if feasible is not None:
            self.assertEqual(len(seen), feasible, f"{algo.name} {tag}: wrong number of outputs")
        return seen

    def check_against_oracle(self, setup, tag: str, *, counter: bool = True) -> tuple[int, int]:
        """Every enumerator, the counter and both fixed-L tests against the oracle. Returns (total, feasible).

        ``backtrack-feasible`` (the brute-force oracle) runs once; ``enum-count`` is the
        same oracle again, so it is run only when ``counter`` is set.
        """
        total = count_linearizations(setup)
        self.assertLessEqual(total, ORACLE_LIMIT, f"{tag}: too large for the oracle")
        observed = setup.features().observed_reads
        ref = set(FeasibleBacktrack().enumerate(setup))
        expected = len(ref)
        mine = FableObsCount().count(setup)
        self.assertEqual(mine.linearizations, total, tag)
        self.assertEqual(mine.feasible, expected if observed else None, tag)
        if counter:
            cnt = EnumerationCounter().count(setup)
            self.assertEqual((cnt.linearizations, cnt.feasible), (mine.linearizations, mine.feasible), tag)
        for cls in ENUMERATORS:
            self.check_enum(cls(), setup, ref, expected, tag)
        self.check_enum(FableObsFilter(test="auto"), setup, ref, expected, tag)
        model = Model(setup)
        for o in linear_extensions(setup):
            truth = o in ref  # == is_feasible(setup, o): that is how backtrack-feasible decided
            self.assertEqual(model.feasible_slots(o), truth, f"{tag}: slot test differs on {setup.poset.to_names(o)}")
            self.assertEqual(model.feasible_auto(o), truth, f"{tag}: automaton test differs on {setup.poset.to_names(o)}")
        return total, len(ref)

    # ---- hand-made adversarial setups

    def test_hand_made(self):
        for name, (d, expect) in hand_made().items():
            with self.subTest(case=name):
                setup = Setup.from_doc(d)
                total, feasible = self.check_against_oracle(setup, name)
                if expect == "none":
                    self.assertEqual(feasible, 0, name)
                elif expect == "some":
                    self.assertTrue(0 < feasible < total, f"{name}: {feasible} of {total}")
                else:
                    self.assertEqual(feasible, total, name)

    def test_shipped_examples(self):
        for fn in ("base.setup.yaml", "formats-example.setup.yaml"):
            setup = load_setup(os.path.join(EXAMPLES, fn))
            if setup.features().rcw or setup.has_data_from_reads():
                continue  # outside the declared capabilities
            with self.subTest(example=fn):
                self.check_against_oracle(setup, fn)

    # ---- generated setups against the oracle

    def test_generated_against_oracle(self):
        n_inst = n_obs = n_infeasible_lin = n_lin = 0
        for k, (hp, setup) in enumerate(generated()):
            with self.subTest(hp=hp):
                total, feasible = self.check_against_oracle(setup, str(hp), counter=k % 5 == 0)
                n_inst += 1
                n_obs += setup.features().observed_reads
                n_lin += total
                n_infeasible_lin += total - feasible
        self.assertGreater(n_inst, 100)
        self.assertGreater(n_obs, 50)
        self.assertGreater(n_infeasible_lin, 0)

    def test_fixed_l_tests_public_api(self):
        setup = Setup.from_doc(hand_made()["repeated constants"][0])
        for o in linear_extensions(setup):
            truth = is_feasible(setup, o)
            self.assertEqual(is_feasible_fast(setup, o), truth)
            self.assertEqual(is_feasible_auto(setup, o), truth)

    # ---- larger instances: algorithms against each other only

    def test_larger_instances_agree(self):
        shapes = [
            {"threads": 3, "actions_per_thread": 2, "max_in_flight": 2, "blocks": 2},  # 34 650 without sync
            {"threads": 2, "actions_per_thread": 4, "max_in_flight": 3, "blocks": 1},  # 12 870
            {"threads": 4, "actions_per_thread": 1, "max_in_flight": 1, "blocks": 2},  # 2 520
            {"threads": 3, "actions_per_thread": 3, "max_in_flight": 2, "blocks": 2},  # only with enough sync
        ]
        checked = 0
        for seed in range(3):
            for shape in shapes:
                for K, E in ((0, 0), (1, 2)):
                    hp = {"seed": seed, "sync_points": K, "events_per_thread": E, **shape,
                          "content": {"classes": {"const": 1.0}, "value_pool": 2},
                          "knowledge": {"p_w": 0.8, "p_r": 0.6, "init_known": 0.5}}
                    try:
                        setup, _ = generate(hp)
                    except RuntimeError:
                        continue
                    total = count_linearizations(setup)
                    if total > LARGE_LIMIT or not setup.features().observed_reads:
                        continue
                    with self.subTest(hp=hp):
                        feasible = FableObsCount().count(setup).feasible
                        self.assertGreater(feasible, 0)  # the observations come from a real run
                        self.assertLessEqual(feasible, total)
                        sets = []
                        for cls in ENUMERATORS:
                            algo = cls()
                            if total <= 30_000:
                                sets.append(self.check_enum(algo, setup, None, feasible, str(hp)))
                            else:  # stream: count and a digest only
                                n = 0
                                digest = 0
                                for o in algo.enumerate(setup):
                                    n += 1
                                    digest ^= hash(o)
                                self.assertEqual(n, feasible, f"{algo.name}: wrong count")
                                sets.append(digest)
                        self.assertTrue(all(s == sets[0] for s in sets), "enumerators disagree")
                        checked += 1
        self.assertGreater(checked, 5)

    # ---- options and edge cases

    def test_dp_rank_options(self):
        setup = Setup.from_doc(hand_made()["repeated constants"][0])
        full = list(FableObsDP().enumerate(setup))
        self.assertEqual(full, list(FeasibleBacktrack().enumerate(setup)) and full)  # non-empty
        self.assertEqual(list(FableObsDP(start=3, stop=9).enumerate(setup)), full[3:9])
        self.assertEqual(list(FableObsDP(start=1, step=4).enumerate(setup)), full[1::4])
        self.assertEqual(list(FableObsDP(start=len(full)).enumerate(setup)), [])

    def test_impossible_observation_yields_nothing(self):
        setup = Setup.from_doc(hand_made()["infeasible: value never written"][0])
        for cls in ENUMERATORS:
            self.assertEqual(list(cls().enumerate(setup)), [])
        self.assertEqual(FableObsCount().count(setup).feasible, 0)

    def test_no_observations_is_all_of_lin(self):
        for seed in range(3):
            setup, _ = generate({"seed": seed, "threads": 3, "actions_per_thread": 2, "sync_points": 1, "events_per_thread": 1})
            total = count_linearizations(setup)
            ref = set(linear_extensions(setup))
            for cls in ENUMERATORS:
                self.check_enum(cls(), setup, ref, total, f"no-obs seed {seed}")
            res = FableObsCount().count(setup)
            self.assertEqual((res.linearizations, res.feasible), (total, None))

    def test_laziness(self):
        setup, _ = generate({"seed": 1, "threads": 3, "actions_per_thread": 4, "max_in_flight": 2,
                             "content": {"classes": {"const": 1.0}, "value_pool": 2}, "knowledge": {"p_r": 0.5}})
        self.assertGreater(count_linearizations(setup), 1_000_000)
        for cls in ENUMERATORS:
            it = cls().enumerate(setup)
            first = next(it)
            self.assertTrue(is_feasible(setup, first), cls.name)

    # ---- CLI

    def test_cli_count_matches_enum_count(self):
        os.makedirs(SCRATCH, exist_ok=True)
        path = os.path.join(SCRATCH, "cli.setup.yaml")
        env = dict(os.environ, PYTHONPATH=ROOT)
        cmd = [sys.executable, "-m", "harness", "gen", "--set", "content.classes={const: 1.0}", "--set", "knowledge.p_r=0.5", "--set", "content.value_pool=2",
               "--set", "sync_points=1", "--set", "events_per_thread=1", "--seed", "3", "-o", path]
        subprocess.run(cmd, cwd=ROOT, env=env, check=True, capture_output=True)
        setup = load_setup(path)
        self.assertLessEqual(count_linearizations(setup), ORACLE_LIMIT)
        ref = subprocess.run([sys.executable, "-m", "harness", "lin", "count", path, "--algo", "enum-count", "--json"],
                             cwd=ROOT, env=env, check=True, capture_output=True, text=True).stdout
        import json

        expected = json.loads(ref)
        want = expected["feasible"] if setup.features().observed_reads else expected["linearizations"]
        for name in ("fable-o-prune", "fable-o-auto", "fable-o-dp", "fable-o-filter"):
            out = subprocess.run([sys.executable, "-m", "harness", "lin", "enum", path, "--plugin", "attempts._archive.round1_4.fable_obs",
                                  "--algo", name, "--count-only"], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
            self.assertEqual(int(out.stdout.strip()), want, name)
        out = subprocess.run([sys.executable, "-m", "harness", "lin", "count", path, "--plugin", "attempts._archive.round1_4.fable_obs",
                              "--algo", "fable-o-count", "--json"], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
        got = json.loads(out.stdout)
        self.assertEqual((got["linearizations"], got["feasible"]), (expected["linearizations"], expected["feasible"]))


if __name__ == "__main__":
    unittest.main()
