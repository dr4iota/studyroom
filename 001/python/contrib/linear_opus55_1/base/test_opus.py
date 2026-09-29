"""Tests for the opus enumerators. Run from ``python/``:

    python3 -m unittest contrib.linear_opus55_1.base.test_opus -v
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

import contrib.linear_opus55_1.base  # noqa: F401  (registers the algorithms)
from abio.gen import generate
from abio.lin.api import LinEnumerator
from abio.lin.dp import count_linearizations
from abio.model import Setup
from abio.registry import available

ENUMS = ["opus55-b-lex", "opus55-b-coollex", "opus55-b-vr", "opus55-b-neargray"]
LIMIT = 200_000  # never enumerate more than this in a test
HERE = os.path.dirname(os.path.abspath(__file__))
PYROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "abio").is_dir()).__str__()


def manual_setup(actions: list[int], in_flight: bool = False) -> Setup:
    """Threads with the given numbers of writes (0 = empty thread)."""
    threads = []
    for t, a in enumerate(actions):
        steps = []
        for i in range(a):
            aid = f"w{t}_{i}"
            steps.append({"write": 0, "id": aid, "data": i + 1})
            if not in_flight:
                steps.append({"done": aid})
        if in_flight:
            steps += [{"done": f"w{t}_{i}"} for i in reversed(range(a))]
        threads.append({"id": f"t{t}", "steps": steps})
    doc = {"format": "setup", "version": 2, "id": "m", "blocks": 1, "sync_points": 0, "init": [0], "threads": threads}
    return Setup.from_doc(doc)


def one_step_diff(a: tuple, b: tuple) -> bool:
    """True iff b = a after one adjacent swap."""
    d = [i for i in range(len(a)) if a[i] != b[i]]
    return len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]


def near_step_diff(a: tuple, b: tuple) -> bool:
    """True iff b = a after one adjacent swap or one element moving by two (two swaps)."""
    if one_step_diff(a, b):
        return True
    d = [i for i in range(len(a)) if a[i] != b[i]]
    if not d or d[-1] - d[0] != 2:
        return False
    p = d[0]
    x, y, z = a[p : p + 3]
    return b[p : p + 3] in ((y, z, x), (z, x, y))


class Base:
    """Mixin: run every opus enumerator on a setup and check it exhaustively."""

    def check_setup(self, setup: Setup) -> int:
        expected = count_linearizations(setup)
        self.assertLessEqual(expected, LIMIT, "test instance too large")
        P = setup.poset
        algos = available("lin-enum")
        for name in ENUMS:
            algo = algos[name]()
            self.assertIsInstance(algo, LinEnumerator)
            seen: set[tuple] = set()
            prev = None
            for o in algo.enumerate(setup):
                self.assertEqual(P.check(P.to_names(o)), [], (name, o))
                self.assertNotIn(o, seen, name)
                seen.add(o)
                if prev is not None:
                    if algo.gray_code:
                        self.assertTrue(one_step_diff(prev, o), (name, prev, o))
                    if name == "opus55-b-neargray":
                        self.assertTrue(near_step_diff(prev, o), (name, prev, o))
                prev = o
            self.assertEqual(len(seen), expected, name)
            # deterministic
            again = algos[name]().enumerate(setup)
            first = next(iter(algos[name]().enumerate(setup)))
            self.assertEqual(next(again), first)
        c = available("lin-count")["opus55-b-multinomial"]().count(setup)
        self.assertEqual(c.linearizations, expected)
        return expected


class TestGenerated(Base, unittest.TestCase):
    def test_generated(self) -> None:
        n_cases = 0
        for seed in range(12):
            for T, A, F in [(1, 3, 2), (2, 2, 1), (2, 3, 2), (3, 2, 2), (3, 1, 1), (4, 1, 2), (2, 4, 3), (5, 1, 1)]:
                setup, _ = generate({"seed": seed, "threads": T, "blocks": 2, "actions_per_thread": A, "max_in_flight": F})
                if count_linearizations(setup) > LIMIT:
                    continue
                with self.subTest(seed=seed, T=T, A=A, F=F):
                    self.check_setup(setup)
                    n_cases += 1
        self.assertGreater(n_cases, 80)


class TestEdgeCases(Base, unittest.TestCase):
    def test_edge(self) -> None:
        cases = [
            [],
            [0],
            [0, 0, 0],
            [1],
            [5],
            [0, 3],
            [3, 0, 0, 2],
            [1, 1],
            [1, 6],
            [6, 1],
            [7, 1, 1],
            [1, 1, 1, 1, 1],
            [2, 2, 2],
            [4, 4],
            [0, 1, 0, 1, 0],
        ]
        for acts in cases:
            for fl in (False, True):
                with self.subTest(acts=acts, in_flight=fl):
                    self.check_setup(manual_setup(acts, fl))

    def test_empty_count(self) -> None:
        self.assertEqual(self.check_setup(manual_setup([])), 1)
        self.assertEqual(self.check_setup(manual_setup([0, 0])), 1)

    def test_laziness(self) -> None:
        setup = manual_setup([10, 10, 10])  # 60 nodes: about 5e26 linearizations
        for name in ENUMS:
            it = available("lin-enum")[name]().enumerate(setup)
            for _ in range(1000):
                o = next(it)
            self.assertEqual(setup.poset.check(setup.poset.to_names(o)), [])

    def test_refuses_sync(self) -> None:
        doc = {
            "format": "setup", "version": 2, "id": "s", "blocks": 1, "sync_points": 1, "init": [0],
            "threads": [{"id": "a", "steps": [{"write": 0, "id": "w", "data": 1}, {"done": "w"}]}],
        }
        setup = Setup.from_doc(doc)
        for name in ENUMS:
            cls = available("lin-enum")[name]
            self.assertFalse(cls.capabilities.sync)
            with self.assertRaises(ValueError):
                next(cls().enumerate(setup))


class TestCLI(unittest.TestCase):
    def test_cli_count_only(self) -> None:
        env = dict(os.environ, PYTHONPATH=PYROOT)
        for name in ENUMS:
            r = subprocess.run(
                [sys.executable, "-m", "abio", "lin", "enum", "examples/base.setup.yaml",
                 "--plugin", "contrib.linear_opus55_1.base", "--algo", name, "--count-only"],
                cwd=PYROOT, env=env, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), "924", name)


if __name__ == "__main__":
    unittest.main()
