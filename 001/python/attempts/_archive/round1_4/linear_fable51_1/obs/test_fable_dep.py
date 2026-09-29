"""Tests for the ``fable51-o-*`` feasible-linearization algorithms.  Run from ``python/``:

    ulimit -v 2000000; timeout 600 python3 -m unittest attempts._archive.round1_4.linear_fable51_1.obs.test_fable_dep -v

Checks, for every enumerator and every instance: each output is a valid linearization
(``poset.check``) and feasible (``harness.semantics.is_feasible``), there are no
duplicates, the set of outputs equals the set produced by ``backtrack-feasible``, and
the count equals ``enum-count``'s ``feasible`` (``linearizations`` without
observations). ``fable51-o-count`` is compared with ``enum-count``. Both fixed-``L``
tests are differentially tested against the oracle on every linearization of every
oracle instance. Oracle instances are small (at most 10 actions, at most 20 000
linearizations); larger instances compare the algorithms with each other only. Nothing
large is ever materialised.
"""

from __future__ import annotations

import os
import random
import subprocess
import sys
import unittest

ROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "harness").is_dir()).__str__()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import harness.lin  # noqa: E402,F401  (register built-ins)
from harness import terms as T  # noqa: E402
from harness.formats import loads  # noqa: E402
from harness.formats import load_setup  # noqa: E402
from harness.gen import generate  # noqa: E402
from harness.lin.backtrack import linear_extensions  # noqa: E402
from harness.lin.dp import count_linearizations  # noqa: E402
from harness.lin.feasible import EnumerationCounter, FeasibleBacktrack  # noqa: E402
from harness.model import Setup  # noqa: E402
from harness.semantics import is_feasible  # noqa: E402

from attempts._archive.round1_4.linear_fable51_1.obs.auto import FableDepAuto  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.obs.common import Model, is_feasible_auto, is_feasible_fast  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.obs.dp import FableDepCount, FableDepDP  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.obs.filter import FableDepFilter  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.obs.prune import FableDepPrune  # noqa: E402

ENUMERATORS = [FableDepPrune, FableDepAuto, FableDepDP, FableDepFilter]
ORACLE_LIMIT = 20_000  # |Lin(P)| cap for instances checked against the brute-force oracle
LARGE_LIMIT = 100_000  # |Lin(P)| cap for algorithm-vs-algorithm instances
EXAMPLES = os.path.join(ROOT, "examples")
SCRATCH = "/tmp/claude-1000/-home-hanhua-mix-studyroom-001/15b0fc29-0001-4775-b7f2-5b9a9a58524e/scratchpad/fable_dep"
MIXES = [{"const": 1.0}, {"copy": 1.0}, {"combine": 1.0}, {"const": 0.3, "copy": 0.4, "combine": 0.3}]


def doc(threads: list[list[dict]], init: list, id: str = "fable-dep-case") -> dict:
    return {"format": "setup", "version": 2, "id": id, "blocks": len(init), "sync_points": 0,
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
    # --- term structure: a compound observed value pins down which write the inner read saw
    c["compound pins inner read to init"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "init.1~7")], [0, "*"]), "some")
    c["compound pins inner read to a write"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "3~7")], [0, "*"]), "some")
    c["compound, inner part impossible"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "9~7")], [0, 0]), "none")
    c["compound, wrong shape"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "7~3")], [0, 0]), "none")
    c["compound, left-associated vs nested"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", "1~2"), R(0, "r2", "1~2~7") + R(0, "r3", "1~(2~7)")], [0, 0]), "none")
    c["nested compound from two reads"] = (
        doc([R(1, "r1") + R(1, "r2") + W(0, "w1", "r1~(r2~2)"), W(1, "w2", 5), R(0, "r3", "init.1~(5~2)")], [0, "*"]), "some")
    c["same read twice in one write"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~r1"), W(1, "w2", 5), R(0, "r2", "5~init.1")], [0, "*"]), "none")
    c["same read twice, consistent"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~r1"), W(1, "w2", 5), R(0, "r2", "5~5")], [0, "*"]), "some")
    # --- an unobserved read feeding a write whose content is observed elsewhere
    c["unobserved feeder read"] = (
        doc([R(0, "u1") + W(1, "w1", "u1"), W(0, "w2", 1) + W(0, "w3", 2), R(1, "r1", 2)], [0, 0]), "some")
    c["unobserved feeder read, init"] = (
        doc([R(0, "u1") + W(1, "w1", "u1~1"), W(0, "w2", 1), R(1, "r1", "0~1")], [0, 0]), "some")
    c["unobserved feeder, two feeders same block"] = (
        doc([R(0, "u1") + R(0, "u2") + W(1, "w1", "u1~u2"), W(0, "w2", 1), R(1, "r1", "0~1")], [0, 0]), "some")
    c["unobserved feeder, impossible order"] = (
        doc([R(0, "u1") + R(0, "u2") + W(1, "w1", "u1~u2"), W(0, "w2", 1), R(1, "r1", "1~0")], [0, 0]), "none")
    # --- a chain of dependence across blocks: read on 1 feeds write on 0, read there feeds a write on 1
    c["chain across blocks"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~1"), R(0, "r2") + W(1, "w2", "r2~2") + R(1, "r3", "init.1~1~2")], [0, "*"]), "some")
    c["chain across blocks, three threads"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~1"), R(0, "r2") + W(1, "w2", "r2~2"), R(1, "r3", "0~1~2")], [0, 0]), "some")
    c["chain across blocks, broken"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~1"), R(0, "r2") + W(1, "w2", "r2~2") + R(1, "r3", "0~2~1")], [0, 0]), "none")
    # --- two writes of the same compound term from different threads
    c["two writes of the same compound term"] = (
        doc([R(0, "r1") + W(1, "w1", "r1~1"), R(0, "r2") + W(1, "w2", "r2~1") + R(1, "r3", "4~1"), W(0, "w3", 4)], [0, 0]), "some")
    c["two copies, only one can match"] = (
        doc([R(0, "r1") + W(1, "w1", "r1~1"), W(0, "w3", 4) + R(0, "r2") + W(1, "w2", "r2~1") + R(1, "r3", "0~1")], [0, 0]), "some")
    # --- a write referencing an earlier write of the same thread
    c["write refs write, feasible"] = (
        doc([W(0, "w1", "*") + W(0, "w2", "w1~2"), R(0, "r1", "w1") + R(0, "r2", "w1~2")], [0]), "some")
    c["write refs write, infeasible order"] = (
        doc([W(0, "w1", "*") + W(0, "w2", "w1~2"), R(0, "r1", "w1~2") + R(0, "r2", "w1")], [0]), "none")
    c["write refs write refs read"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~1") + W(0, "w2", "w1~2"), W(1, "w3", 9), R(0, "r2", "9~1~2")], [0, 0]), "some")
    # --- read-modify-write on one block (a read feeds a write of the same block)
    c["read-modify-write"] = (
        doc([R(0, "r1") + W(0, "w1", "r1~1"), R(0, "r2") + W(0, "w2", "r2~1"), R(0, "r3", "0~1~1")], [0]), "some")
    c["read-modify-write, lost update"] = (
        doc([R(0, "r1") + W(0, "w1", "r1~1") + R(0, "r3", "0~1"), R(0, "r2") + W(0, "w2", "r2~1") + R(0, "r4", "0~1")], [0]), "some")
    # --- observed compound terms that no run produced (random junk)
    c["junk observation: unknown symbol inside"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "w9~7")], [0, 0]), "none")
    c["junk observation: init of the wrong block"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "init.0~7")], [0, "*"]), "none")
    c["junk observation: too deep"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~7"), W(1, "w2", 3), R(0, "r2", "3~7~7")], [0, 0]), "none")
    # --- constant data (the previous round's cases must keep working)
    c["const: ordered values force write order"] = (
        doc([W(0, "w1", 1), W(0, "w2", 2), R(0, "r1", 1) + R(0, "r2", 2)], [0]), "some")
    c["const: repeated constants"] = (
        doc([W(0, "w1", 1) + W(0, "w2", 2), W(0, "w3", 1), R(0, "r1", 1) + R(0, "r2", 2) + R(0, "r3", 1)], [0]), "some")
    c["const: unknown write symbol"] = (
        doc([W(0, "w1", "*") + W(0, "w2", 3), R(0, "r1", "w1") + R(0, "r2", 3)], [0]), "some")
    c["const: init forces read first, unknown init"] = (doc([W(0, "w1", 1), R(0, "r1", "init.0")], ["*"]), "some")
    c["const: infeasible value never written"] = (doc([W(0, "w1", 1), R(0, "r1", 7)], [0]), "none")
    c["const: cyclic value order on one thread"] = (
        doc([W(0, "w1", 1) + W(0, "w2", 2), R(0, "r1", 2) + R(0, "r2", 1) + R(0, "r3", 2)], [0]), "none")
    c["const: in-flight reads"] = (
        doc([[{"read": 0, "id": "r1"}, {"read": 0, "id": "r2"}, {"done": "r2", "data": 1}, {"done": "r1", "data": 0}], W(0, "w1", 1)], [0]), "some")
    # --- everything feasible / nothing observed / empty
    c["all: copy observed after its writer"] = (
        doc([R(1, "r1") + W(0, "w1", "r1~1") + R(0, "r2", "0~1"), R(1, "u1")], [0, 0]), "all")
    c["all: no observations, copies"] = (doc([R(0, "r1") + W(1, "w1", "r1~1"), W(0, "w2", 2) + R(1, "r2")], [0, 0]), "all")
    c["empty"] = (doc([[], []], [0]), "all")
    return c


def corrupted(seed: int) -> Setup:
    """A generated setup whose first observation is replaced by a random term no run may produce."""
    setup, _ = generate({"seed": seed, "threads": 2, "actions_per_thread": 3, "max_in_flight": 2, "blocks": 2,
                         "content": {"classes": MIXES[seed % 4], "max_depth": 2, "value_pool": 2},
                         "knowledge": {"p_w": 0.7, "p_r": 0.7, "init_known": 0.5}})
    rng = random.Random(seed)
    d = setup.to_doc()
    junk = [T.seq(T.Init(1), 7), T.seq(2, T.Unk("w0")), T.seq(1, 2, 3), T.seq(T.Init(0), T.Init(0)), T.Const(9)]
    for th in d["threads"]:
        for s in th["steps"]:
            if "done" in s and "data" in s:
                s["data"] = T.to_value(rng.choice(junk))
                return Setup.from_doc(d)
    return setup


def generated(seeds=range(4), *, cap=8_000):
    """Generated instances over content mixes, value pools, p_r, p_w and blocks, small enough for the oracle."""
    shapes = [
        {"threads": 2, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 1},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 3},
        {"threads": 2, "actions_per_thread": 4, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 2, "actions_per_thread": 5, "max_in_flight": 3},
    ]
    for seed in seeds:
        for si, shape in enumerate(shapes):
            for mi, mix in enumerate(MIXES):
                for p_r in (0, 0.3, 0.7, 1):
                    for p_w in (1, 0.7):
                        blocks = 1 + (seed + si + mi) % 3
                        hp = {"seed": seed, "blocks": blocks, **shape,
                              "content": {"classes": mix, "max_depth": 1 + (seed + mi) % 2, "value_pool": 1 + (seed + blocks + mi) % 3},
                              "knowledge": {"p_w": p_w, "p_r": p_r, "init_known": 0.5 if seed % 2 else 1.0}}
                        setup, _ = generate(hp)
                        if count_linearizations(setup) > cap or len(setup.actions) > 10:
                            continue
                        yield hp, setup


class FableDepTests(unittest.TestCase):
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
        mine = FableDepCount().count(setup)
        self.assertEqual(mine.linearizations, total, tag)
        self.assertEqual(mine.feasible, expected if observed else None, tag)
        if counter:
            cnt = EnumerationCounter().count(setup)
            self.assertEqual((cnt.linearizations, cnt.feasible), (mine.linearizations, mine.feasible), tag)
        for cls in ENUMERATORS:
            self.check_enum(cls(), setup, ref, expected, tag)
        self.check_enum(FableDepFilter(test="auto"), setup, ref, expected, tag)
        model = Model(setup)
        for o in linear_extensions(setup):
            truth = o in ref  # == is_feasible(setup, o): that is how backtrack-feasible decided
            self.assertEqual(model.feasible_rf(o), truth, f"{tag}: reads-from test differs on {setup.poset.to_names(o)}")
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

    def test_corrupted_observations(self):
        for seed in range(8):
            setup = corrupted(seed)
            if count_linearizations(setup) > ORACLE_LIMIT:
                continue
            with self.subTest(seed=seed):
                self.check_against_oracle(setup, f"corrupted {seed}", counter=False)

    def test_shipped_examples(self):
        for fn in ("base.setup.yaml", "formats-example.setup.yaml"):
            setup = load_setup(os.path.join(EXAMPLES, fn))
            if setup.features().rcw or setup.features().sync:
                continue  # outside the declared capabilities
            with self.subTest(example=fn):
                self.check_against_oracle(setup, fn)

    # ---- generated setups against the oracle

    def test_generated_against_oracle(self):
        n_inst = n_obs = n_dep = n_infeasible_lin = n_lin = n_none = 0
        for k, (hp, setup) in enumerate(generated()):
            with self.subTest(hp=hp):
                total, feasible = self.check_against_oracle(setup, str(hp), counter=k % 7 == 0)
                n_inst += 1
                n_obs += setup.features().observed_reads
                n_dep += setup.has_data_from_reads()
                n_lin += total
                n_infeasible_lin += total - feasible
                n_none += feasible == 0
        self.assertGreater(n_inst, 100)
        self.assertGreater(n_obs, 60)
        self.assertGreater(n_dep, 30)
        self.assertGreater(n_infeasible_lin, 0)
        self.assertEqual(n_none, 0)  # observations come from a real run

    def test_fixed_l_tests_public_api(self):
        setup = Setup.from_doc(hand_made()["chain across blocks"][0])
        for o in linear_extensions(setup):
            truth = is_feasible(setup, o)
            self.assertEqual(is_feasible_fast(setup, o), truth)
            self.assertEqual(is_feasible_auto(setup, o), truth)

    # ---- larger instances: algorithms against each other only

    def test_larger_instances_agree(self):
        shapes = [
            {"threads": 3, "actions_per_thread": 2, "max_in_flight": 2, "blocks": 2},  # 34 650
            {"threads": 2, "actions_per_thread": 4, "max_in_flight": 3, "blocks": 1},  # 12 870
            {"threads": 4, "actions_per_thread": 1, "max_in_flight": 1, "blocks": 2},  # 2 520
            {"threads": 3, "actions_per_thread": 2, "max_in_flight": 2, "blocks": 3},  # 34 650
        ]
        checked = 0
        for seed in range(3):
            for shape in shapes:
                for mix in MIXES[1:]:
                    hp = {"seed": seed, **shape, "content": {"classes": mix, "max_depth": 2, "value_pool": 2},
                          "knowledge": {"p_w": 0.8, "p_r": 0.6, "init_known": 0.5}}
                    setup, _ = generate(hp)
                    total = count_linearizations(setup)
                    if total > LARGE_LIMIT or not setup.features().observed_reads:
                        continue
                    with self.subTest(hp=hp):
                        feasible = FableDepCount().count(setup).feasible
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
        setup = Setup.from_doc(hand_made()["chain across blocks"][0])
        full = list(FableDepDP().enumerate(setup))
        self.assertEqual(full, list(FeasibleBacktrack().enumerate(setup)) and full)  # non-empty
        self.assertEqual(list(FableDepDP(start=3, stop=9).enumerate(setup)), full[3:9])
        self.assertEqual(list(FableDepDP(start=1, step=4).enumerate(setup)), full[1::4])
        self.assertEqual(list(FableDepDP(start=len(full)).enumerate(setup)), [])

    def test_impossible_observation_yields_nothing(self):
        for name in ("compound, inner part impossible", "junk observation: unknown symbol inside"):
            setup = Setup.from_doc(hand_made()[name][0])
            for cls in ENUMERATORS:
                self.assertEqual(list(cls().enumerate(setup)), [])
            self.assertEqual(FableDepCount().count(setup).feasible, 0)

    def test_no_observations_is_all_of_lin(self):
        for seed in range(3):
            setup, _ = generate({"seed": seed, "threads": 3, "actions_per_thread": 2, "blocks": 2,
                                 "content": {"classes": MIXES[3], "value_pool": 2}})
            total = count_linearizations(setup)
            ref = set(linear_extensions(setup))
            for cls in ENUMERATORS:
                self.check_enum(cls(), setup, ref, total, f"no-obs seed {seed}")
            res = FableDepCount().count(setup)
            self.assertEqual((res.linearizations, res.feasible), (total, None))

    def test_laziness(self):
        setup, _ = generate({"seed": 1, "threads": 3, "actions_per_thread": 4, "max_in_flight": 2, "blocks": 2,
                             "content": {"classes": MIXES[3], "value_pool": 2}, "knowledge": {"p_r": 0.5}})
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
        cmd = [sys.executable, "-m", "harness", "gen", "--set", "knowledge.p_r=0.6", "--set", "content.value_pool=2",
               "--set", "content.classes={const: 0.3, copy: 0.4, combine: 0.3}", "--seed", "3", "-o", path]
        subprocess.run(cmd, cwd=ROOT, env=env, check=True, capture_output=True)
        setup = load_setup(path)
        self.assertLessEqual(count_linearizations(setup), ORACLE_LIMIT)
        self.assertTrue(setup.features().observed_reads)
        ref = subprocess.run([sys.executable, "-m", "harness", "lin", "count", path, "--algo", "enum-count", "--json"],
                             cwd=ROOT, env=env, check=True, capture_output=True, text=True).stdout
        expected = loads(ref, "count")
        want = expected["feasible"]
        for name in ("fable51-o-prune", "fable51-o-auto", "fable51-o-dp", "fable51-o-filter"):
            out = subprocess.run([sys.executable, "-m", "harness", "lin", "enum", path, "--plugin", "attempts._archive.round1_4.linear_fable51_1.obs",
                                  "--algo", name, "--count-only"], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
            self.assertEqual(int(out.stdout.strip()), want, name)
        out = subprocess.run([sys.executable, "-m", "harness", "lin", "count", path, "--plugin", "attempts._archive.round1_4.linear_fable51_1.obs",
                              "--algo", "fable51-o-count", "--json"], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
        got = loads(out.stdout, "count")
        self.assertEqual((got["linearizations"], got["feasible"]), (expected["linearizations"], expected["feasible"]))


if __name__ == "__main__":
    unittest.main()
