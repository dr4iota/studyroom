"""Tests for the opus sync enumerators. Run from ``python/``:

    python3 -m unittest attempts._archive.round1_4.linear_opus55_1.base_sync.test_opus_sync -v
"""

from __future__ import annotations

import itertools
import os
import random
import subprocess
import sys
import tempfile
import unittest

import attempts._archive.round1_4.linear_opus55_1.base_sync  # noqa: F401  (registers the algorithms)
from harness.gen import generate
from harness.lin.api import LinEnumerator
from harness.lin.dp import count_linearizations
from harness.model import Setup
from harness.registry import available
from attempts._archive.round1_4.linear_opus55_1.base_sync.enumerators import (
    count_segmented,
    family_tree,
    pruesse_ruskey,
    segmented,
    segments,
    varol_rotem,
)

ENUMS = ["opus55-s-vr", "opus55-s-pr", "opus55-s-tree", "opus55-s-seg"]
# Claimed bound on adjacent transpositions (Kendall tau distance) between consecutive outputs.
MAX_SWAPS = {"opus55-s-pr": 2, "opus55-s-tree": 3}
LIMIT = 200_000  # never enumerate more than this in a test
HERE = os.path.dirname(os.path.abspath(__file__))
PYROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "harness").is_dir()).__str__()
RELATION_SETS = [["before"], ["after"], ["at"], ["before", "after"], ["before", "at"], ["after", "at"],
                 ["before", "after", "at"]]


def kendall(a: tuple, b: tuple) -> int:
    """Number of adjacent transpositions between permutations a and b (0 if equal)."""
    lo = 0
    n = len(a)
    while lo < n and a[lo] == b[lo]:
        lo += 1
    if lo == n:
        return 0
    hi = n - 1
    while a[hi] == b[hi]:
        hi -= 1
    pa = {x: i for i, x in enumerate(a[lo : hi + 1])}
    s = [pa[x] for x in b[lo : hi + 1]]
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])


def doc(threads: list[list[dict]], K: int) -> Setup:
    return Setup.from_doc({
        "format": "setup", "version": 2, "id": "h", "blocks": 1, "sync_points": K, "init": [0],
        "threads": [{"id": f"t{i}", "steps": s} for i, s in enumerate(threads)],
    })


def W(aid: str) -> list[dict]:
    """A write followed by its done."""
    return [{"write": 0, "id": aid, "data": 1}, {"done": aid}]


class Base:
    def check_setup(self, setup: Setup, algos=ENUMS) -> int:
        expected = count_linearizations(setup)
        self.assertLessEqual(expected, LIMIT, "test instance too large")
        P = setup.poset
        reg = available("lin-enum")
        for name in algos:
            algo = reg[name]()
            self.assertIsInstance(algo, LinEnumerator)
            self.assertTrue(algo.capabilities.sync)
            self.assertFalse(algo.capabilities.rcw)
            self.assertFalse(algo.gray_code)
            bound = MAX_SWAPS.get(name)
            seen: set[tuple] = set()
            prev = None
            first = None
            for o in algo.enumerate(setup):
                self.assertEqual(P.check(P.to_names(o)), [], (name, o))
                self.assertNotIn(o, seen, name)
                seen.add(o)
                if prev is None:
                    first = o
                elif bound is not None:
                    d = kendall(prev, o)
                    self.assertTrue(1 <= d <= bound, (name, d, prev, o))
                prev = o
            self.assertEqual(len(seen), expected, name)
            self.assertEqual(next(iter(reg[name]().enumerate(setup))), first, "deterministic")
        c = available("lin-count")["opus55-s-segcount"]().count(setup)
        self.assertEqual(c.linearizations, expected)
        return expected


class TestGenerated(Base, unittest.TestCase):
    def test_generated_sync(self) -> None:
        n_cases = 0
        configs = [  # (threads, actions, in_flight, sync_points, events_per_thread)
            (2, 2, 1, 1, 1), (2, 2, 2, 2, 2), (2, 3, 2, 2, 3), (3, 1, 1, 1, 1), (3, 2, 2, 2, 2),
            (3, 2, 1, 3, 3), (4, 1, 1, 2, 2), (2, 4, 3, 3, 2), (3, 2, 2, 1, 1), (4, 1, 2, 3, 3),
            (1, 3, 2, 2, 2), (5, 1, 1, 2, 1),
        ]
        for seed in range(10):
            for T, A, F, K, E in configs:
                for rel in RELATION_SETS:
                    e = min(E, K * len(rel))
                    try:
                        setup, _ = generate({"seed": seed, "threads": T, "blocks": 2, "actions_per_thread": A,
                                             "max_in_flight": F, "sync_points": K, "events_per_thread": e,
                                             "relations": rel})
                    except RuntimeError:  # generator found only cyclic sync patterns
                        continue
                    if count_linearizations(setup) > 20_000:
                        continue
                    with self.subTest(seed=seed, T=T, A=A, F=F, K=K, E=e, rel=rel):
                        self.check_setup(setup)
                        n_cases += 1
        self.assertGreater(n_cases, 350)

    def test_generated_base(self) -> None:
        n_cases = 0
        for seed in range(8):
            for T, A, F in [(1, 3, 2), (2, 2, 1), (2, 3, 2), (3, 2, 2), (4, 1, 2), (5, 1, 1)]:
                setup, _ = generate({"seed": seed, "threads": T, "blocks": 2, "actions_per_thread": A,
                                     "max_in_flight": F})
                if count_linearizations(setup) > 20_000:
                    continue
                with self.subTest(seed=seed, T=T, A=A, F=F):
                    self.check_setup(setup)
                    n_cases += 1
        self.assertGreater(n_cases, 30)

    def test_larger(self) -> None:
        """A few instances up to LIMIT outputs (full streaming check)."""
        done = 0
        for seed in range(40):
            setup, _ = generate({"seed": seed, "threads": 3, "blocks": 2, "actions_per_thread": 2,
                                 "max_in_flight": 2, "sync_points": 2, "events_per_thread": 2})
            c = count_linearizations(setup)
            if 20_000 < c <= LIMIT:
                with self.subTest(seed=seed, count=c):
                    self.check_setup(setup)
                    done += 1
            if done >= 2:
                break
        self.assertGreater(done, 0)


class TestRandomDags(unittest.TestCase):
    """The core functions on arbitrary random DAGs, against brute force over permutations."""

    def test_random_dags(self) -> None:
        for trial in range(600):
            rng = random.Random(trial)
            n = rng.randint(0, 7)
            p = rng.random() * 0.5
            perm = list(range(n))
            rng.shuffle(perm)
            succs: list[list[int]] = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < p:
                        succs[perm[i]].append(perm[j])
            truth = set()
            for q in itertools.permutations(range(n)):
                pos = {x: i for i, x in enumerate(q)}
                if all(pos[x] < pos[y] for x in range(n) for y in succs[x]):
                    truth.add(q)
            self.assertEqual(count_segmented(n, succs), len(truth))
            for f, bound in [(varol_rotem, None), (pruesse_ruskey, 2), (family_tree, 3), (segmented, None)]:
                outs = list(f(n, succs))
                self.assertEqual(len(outs), len(truth), (f.__name__, trial))
                self.assertEqual(set(outs), truth, (f.__name__, trial))
                if bound:
                    for a, b in zip(outs, outs[1:]):
                        self.assertTrue(1 <= kendall(a, b) <= bound, (f.__name__, trial, a, b))


class TestEdgeCases(Base, unittest.TestCase):
    def test_unused_sync_point(self) -> None:
        s = doc([W("a") + W("b"), W("c")], 1)
        self.assertEqual(self.check_setup(s), 15 * 7)  # C(6,2)=15 interleavings x 7 slots
        self.assertEqual(self.check_setup(doc([W("a")], 3)), 5 * 4 * 3)  # 2 nodes + 3 isolated

    def test_only_before_or_after(self) -> None:
        self.check_setup(doc([W("a") + [{"before": 0}] + W("b"), W("c") + [{"before": 0}]], 1))
        self.check_setup(doc([[{"after": 0}] + W("a"), W("b") + [{"after": 0}] + W("c")], 1))
        self.check_setup(doc([W("a") + [{"before": 0}], W("b") + [{"after": 0}] + W("c")], 1))

    def test_full_barrier(self) -> None:
        s = doc([W("a") + [{"at": 0}] + W("b"), W("c") + [{"at": 0}] + W("d"), W("e") + [{"at": 0}] + W("f")], 1)
        cuts, segs = segments(len(s.poset), s.poset.succs)
        self.assertEqual([s.poset.names[c] for c in cuts], ["sync.0"])
        self.assertEqual(self.check_setup(s), 90 * 90)  # 6!/(2!)^3 on each side

    def test_chain_of_barriers(self) -> None:
        th = [W(f"a{t}") + [{"at": 0}] + W(f"b{t}") + [{"at": 1}] + W(f"c{t}") + [{"at": 2}] + W(f"d{t}")
              for t in range(2)]
        s = doc(th, 3)
        self.assertEqual(len(segments(len(s.poset), s.poset.succs)[0]), 3)
        self.assertEqual(self.check_setup(s), 6 ** 4)

    def test_partial_barrier_and_mixed(self) -> None:
        self.check_setup(doc([W("a") + [{"at": 0}] + W("b"), W("c") + [{"at": 0}], W("d") + W("e")], 1))
        self.check_setup(doc([W("a") + [{"at": 0}] + W("b") + [{"before": 1}],
                              W("c") + [{"at": 0}, {"after": 1}] + W("e"), W("d")], 2))

    def test_before_then_after_same_thread(self) -> None:
        self.check_setup(doc([W("a") + [{"before": 0}] + W("b") + [{"after": 0}] + W("c"), W("d") + W("e")], 1))
        self.check_setup(doc([[{"before": 0}, {"after": 0}] + W("a"), W("b") + [{"after": 0}], W("c")], 1))

    def test_event_positions(self) -> None:
        # first step, last step, inside an in-flight action
        self.check_setup(doc([[{"before": 0}] + W("a") + W("b"), W("c") + [{"after": 0}]], 1))
        self.check_setup(doc([[{"at": 0}] + W("a"), W("b") + [{"at": 0}]], 1))
        inflight = [{"write": 0, "id": "a", "data": 1}, {"write": 0, "id": "b", "data": 2}, {"before": 0},
                    {"done": "a"}, {"after": 1}, {"done": "b"}]
        other = [{"read": 0, "id": "r"}, {"after": 0}, {"done": "r"}, {"before": 1}] + W("c")
        self.check_setup(doc([inflight, other], 2))
        self.check_setup(doc([inflight, [{"read": 0, "id": "r"}, {"at": 0}, {"done": "r"}] + W("c")], 2))

    def test_base_k0(self) -> None:
        for th in ([], [[]], [W("a")], [W("a"), W("b")], [W("a") + W("b"), [], W("c")],
                   [W("a") + W("b") + W("c"), W("d") + W("e")]):
            with self.subTest(th=len(th)):
                self.check_setup(doc(th, 0))

    def test_only_sync_nodes(self) -> None:
        self.assertEqual(self.check_setup(doc([], 3)), 6)
        self.assertEqual(self.check_setup(doc([[]], 1)), 1)

    def test_formats_example(self) -> None:
        from harness.formats import load_setup

        s = load_setup(os.path.join(PYROOT, "examples", "formats-example.setup.yaml"))
        self.assertEqual(self.check_setup(s), 45)

    def test_laziness(self) -> None:
        th = [W(f"a{t}") + W(f"b{t}") + [{"before": 0}] + W(f"c{t}") + W(f"d{t}") + [{"after": 1}] + W(f"e{t}")
              for t in range(4)]
        s = doc(th, 2)  # 44 nodes, astronomically many linearizations
        for name in ENUMS:
            it = available("lin-enum")[name]().enumerate(s)
            for _ in range(2000):
                o = next(it)
            self.assertEqual(s.poset.check(s.poset.to_names(o)), [], name)


class TestCLI(unittest.TestCase):
    def run_cli(self, *args: str) -> str:
        env = dict(os.environ, PYTHONPATH=PYROOT)
        r = subprocess.run([sys.executable, "-m", "harness", *args], cwd=PYROOT, env=env,
                           capture_output=True, text=True, timeout=200)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def test_cli_base(self) -> None:
        for name in ENUMS:
            out = self.run_cli("lin", "enum", "examples/base.setup.yaml", "--plugin", "attempts._archive.round1_4.linear_opus55_1.base_sync",
                               "--algo", name, "--count-only")
            self.assertEqual(out, "924", name)

    def test_cli_sync(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "s.yaml")
            self.run_cli("gen", "--set", "sync_points=2", "--set", "events_per_thread=2", "-o", path)
            want = self.run_cli("lin", "count", path)
            n = int(next(l for l in want.splitlines() if l.startswith("linearizations:")).split()[1])
            self.assertLessEqual(n, LIMIT)
            for name in ENUMS:
                out = self.run_cli("lin", "enum", path, "--plugin", "attempts._archive.round1_4.linear_opus55_1.base_sync", "--algo", name,
                                   "--count-only")
                self.assertEqual(int(out), n, name)
            out = self.run_cli("lin", "count", path, "--plugin", "attempts._archive.round1_4.linear_opus55_1.base_sync", "--algo", "opus55-s-segcount")
            self.assertIn(f"linearizations: {n}", out)


if __name__ == "__main__":
    unittest.main()
