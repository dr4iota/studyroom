"""Tests for the ``fable-*`` linearizers.  Run from ``python/``:

    ulimit -v 2000000; timeout 300 python3 -m unittest contrib.linear_fable51_1.base.test_fable -v

Every enumerator is checked on the shipped base example, on many generated base setups
and on edge cases: each output is a valid linearization, there are no duplicates, and the
number of outputs equals the positions-DP count. Instances are capped at 200 000
linearizations and streamed; nothing large is ever materialized.
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

ROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "abio").is_dir()).__str__()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import abio.lin  # noqa: E402,F401  (register built-ins)
from abio.formats import load_setup  # noqa: E402
from abio.gen import generate  # noqa: E402
from abio.lin.dp import count_linearizations  # noqa: E402
from abio.model import Setup  # noqa: E402

from contrib.linear_fable51_1.base.coollex import FableCoolLex  # noqa: E402
from contrib.linear_fable51_1.base.gray import FableGray, combination_list  # noqa: E402
from contrib.linear_fable51_1.base.lex import FableLex  # noqa: E402
from contrib.linear_fable51_1.base.unrank import FableCount, FableUnrank, rank, unrank  # noqa: E402
from contrib.linear_fable51_1.base.common import multinomial  # noqa: E402

ENUMERATORS = [FableLex, FableCoolLex, FableUnrank, FableGray]
LIMIT = 200_000
EXAMPLE = os.path.join(ROOT, "examples", "base.setup.yaml")


def base_doc(lengths: list[int]) -> dict:
    """A base setup whose thread ``t`` has ``lengths[t]`` actions (``2 * lengths[t]`` nodes)."""
    threads = []
    for t, m in enumerate(lengths):
        steps = []
        for k in range(m):
            steps.append({"write": k % 2, "id": f"w{t}_{k}", "data": k})
            steps.append({"done": f"w{t}_{k}"})
        threads.append({"id": f"t{t}", "steps": steps})
    return {"format": "setup", "version": 2, "id": "fable-edge", "blocks": 2, "sync_points": 0,
            "init": [0, 0], "threads": threads}


def generated(seeds=range(12)):
    """Small generated base setups spanning thread counts and shapes."""
    shapes = [
        {"threads": 2, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 1},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 3},
        {"threads": 4, "actions_per_thread": 1, "max_in_flight": 1},
        {"threads": 5, "actions_per_thread": {"total": {"read": 2, "write": 2}}, "max_in_flight": 2},
        {"threads": 2, "actions_per_thread": {"total": {"read": 5, "write": 2}}, "max_in_flight": 4},
    ]
    for shape in shapes:
        for seed in seeds:
            hp = {"seed": seed, "blocks": 2, **shape}
            setup, _ = generate(hp)
            yield setup


class FableTests(unittest.TestCase):
    def check_enum(self, algo, setup):
        """Validity, uniqueness, count; returns the count."""
        P = setup.poset
        n = count_linearizations(setup)
        self.assertLessEqual(n, LIMIT, "test instance too large")
        seen = set()
        for o in algo.enumerate(setup):
            self.assertEqual(len(o), len(P))
            self.assertEqual(P.check(P.to_names(o)), [], f"{algo.name}: invalid {o}")
            self.assertNotIn(o, seen, f"{algo.name}: duplicate {o}")
            seen.add(o)
        self.assertEqual(len(seen), n, f"{algo.name}: wrong number of outputs")
        return n

    def test_base_example_924(self):
        s = load_setup(EXAMPLE)
        for cls in ENUMERATORS:
            with self.subTest(cls.name):
                self.assertEqual(self.check_enum(cls(), s), 924)
        self.assertEqual(FableCount().count(s).linearizations, 924)

    def test_generated_setups(self):
        for s in generated():
            for cls in ENUMERATORS:
                with self.subTest(algo=cls.name, setup=s.id):
                    self.check_enum(cls(), s)
            self.assertEqual(FableCount().count(s).linearizations, count_linearizations(s))

    def test_edge_cases(self):
        cases = {
            "one thread": base_doc([4]),
            "one thread, one action": base_doc([1]),
            "empty poset": base_doc([0, 0]),
            "empty threads mixed": base_doc([0, 3, 0, 1, 0]),
            "very uneven": base_doc([6, 1]),
            "very uneven 3": base_doc([1, 5, 1]),
            "many singletons": base_doc([1, 1, 1, 1, 1]),
        }
        for name, doc in cases.items():
            s = Setup.from_doc(doc)
            for cls in ENUMERATORS:
                with self.subTest(algo=cls.name, case=name):
                    self.check_enum(cls(), s)
            with self.subTest(algo="fable51-b-count", case=name):
                self.assertEqual(FableCount().count(s).linearizations, count_linearizations(s))

    def test_generated_edge_shapes(self):
        # Generated setups with empty threads (few actions spread over many threads),
        # a single thread, and nothing at all.
        hps = [
            {"seed": 3, "threads": 4, "actions_per_thread": {"total": {"read": 2, "write": 1}}},
            {"seed": 7, "threads": 6, "actions_per_thread": {"total": {"read": 1, "write": 1}}},
            {"seed": 1, "threads": 1, "actions_per_thread": 3},
            {"seed": 1, "threads": 2, "actions_per_thread": {"total": {"read": 0, "write": 0}}},
        ]
        for hp in hps:
            s, _ = generate({"blocks": 2, "max_in_flight": 2, **hp})
            for cls in ENUMERATORS:
                with self.subTest(algo=cls.name, hp=str(hp)):
                    self.check_enum(cls(), s)

    # ---- algorithm-specific properties

    @staticmethod
    def labels(setup, order):
        return tuple(setup.poset.thread[x] for x in order)

    def test_lex_is_sorted_and_unrank_agrees(self):
        for s in list(generated(range(3))) + [load_setup(EXAMPLE)]:
            prev = None
            ranked = FableUnrank().enumerate(s)
            for o in FableLex().enumerate(s):
                lab = self.labels(s, o)
                if prev is not None:
                    self.assertLess(prev, lab, "fable51-b-lex not in increasing label order")
                prev = lab
                self.assertEqual(o, next(ranked), "fable51-b-unrank disagrees with fable51-b-lex")
            self.assertRaises(StopIteration, next, ranked)

    def test_rank_unrank_inverse(self):
        for counts in ([2, 2], [3, 1, 2], [0, 4], [1, 1, 1, 1], [5, 3], [2, 0, 3, 1]):
            m = multinomial(counts)
            seqs = [tuple(unrank(r, counts)) for r in range(m)]
            self.assertEqual(len(set(seqs)), m)
            self.assertEqual(seqs, sorted(seqs))
            for r, seq in enumerate(seqs):
                self.assertEqual(rank(seq, counts), r)

    def test_unrank_options(self):
        s = load_setup(EXAMPLE)
        full = list(FableUnrank().enumerate(s))
        self.assertEqual(list(FableUnrank(start=900).enumerate(s)), full[900:])
        self.assertEqual(list(FableUnrank(start=10, stop=20).enumerate(s)), full[10:20])
        self.assertEqual(list(FableUnrank(step=7).enumerate(s)), full[::7])
        self.assertEqual(list(FableUnrank(start=5, stop=2000, step=100).enumerate(s)), full[5::100])
        self.assertEqual(list(FableUnrank(start=924).enumerate(s)), [])

    def test_coollex_prefix_shifts(self):
        """Consecutive fable51-b-coollex label sequences differ by one prefix shift."""
        for s in list(generated(range(3))) + [load_setup(EXAMPLE)]:
            prev = None
            for o in FableCoolLex().enumerate(s):
                lab = self.labels(s, o)
                if prev is not None and len(lab) > 1:
                    ok = any(lab == (prev[k],) + prev[:k] + prev[k + 1 :] and lab != prev
                             for k in range(1, len(prev)))
                    self.assertTrue(ok, f"not a prefix shift: {prev} -> {lab}")
                prev = lab

    # ---- fable51-b-gray: at most two adjacent transpositions between consecutive outputs

    @staticmethod
    def adjacent_swaps(a):
        for i in range(len(a) - 1):
            b = list(a)
            b[i], b[i + 1] = b[i + 1], b[i]
            yield tuple(b)

    def within_two_adjacent_swaps(self, a, b):
        if a == b:
            return False
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        if len(diff) > 4:
            return False
        for c in self.adjacent_swaps(a):
            if c == b or any(d == b for d in self.adjacent_swaps(c)):
                return True
        return False

    def test_gray_two_adjacent_transpositions(self):
        setups = list(generated(range(4))) + [load_setup(EXAMPLE)]
        setups += [Setup.from_doc(base_doc(x)) for x in ([6, 1], [1, 5, 1], [1, 1, 1, 1, 1], [0, 3, 0, 1, 0], [4], [2, 2, 2])]
        for s in setups:
            prev = None
            steps = 0
            for o in FableGray().enumerate(s):
                if prev is not None:
                    self.assertTrue(self.within_two_adjacent_swaps(prev, o), f"{s.id}: {prev} -> {o}")
                    steps += 1
                prev = o
            self.assertEqual(steps + 1, count_linearizations(s))

    def test_gray_combination_lists(self):
        """C(s,t)/D(s,t): Hamiltonian over (s,t)-strings, near-perfect, documented endpoints."""
        from itertools import combinations
        for s in range(0, 10):
            for t in range(0, 10):
                if s + t > 16:
                    continue
                allc = {tuple(1 if i in c else 0 for i in range(s + t)) for c in combinations(range(s + t), t)}
                for fam in "CD":
                    seq = combination_list(s, t, fam)
                    self.assertEqual(len(seq), len(allc))
                    self.assertEqual(set(seq), allc)
                    for a, b in zip(seq, seq[1:]):
                        self.assertTrue(self.within_two_adjacent_swaps(a, b), (s, t, fam, a, b))
                    if s and t:
                        self.assertEqual(seq[-1], (0,) * s + (1,) * t)
                        if fam == "C":
                            self.assertEqual(seq[0], (1,) + (0,) * s + (1,) * (t - 1))
                        else:
                            self.assertEqual(seq[0], (1, 1) + (0,) * s + (1,) * (t - 2) if t >= 2 else (1,) + (0,) * s)

    def test_gray_flag_is_honest(self):
        """Exactly-one-adjacent-swap Gray codes are impossible in general (parity), so the flag is False."""
        self.assertFalse(FableGray.gray_code)
        s = load_setup(EXAMPLE)
        even = sum(1 for o in FableLex().enumerate(s)
                   if sum(1 for i in range(len(o)) for j in range(i + 1, len(o)) if o[i] > o[j]) % 2 == 0)
        self.assertEqual((even, 924 - even), (472, 452))  # colour classes differ by 20 > 1

    def test_cli_count_only(self):
        for name in ("fable51-b-lex", "fable51-b-coollex", "fable51-b-unrank", "fable51-b-gray"):
            with self.subTest(name):
                out = subprocess.run(
                    [sys.executable, "-m", "abio", "lin", "enum", EXAMPLE, "--plugin", "contrib.linear_fable51_1.base",
                     "--algo", name, "--count-only"],
                    cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertEqual(out.stdout.strip(), "924")
        out = subprocess.run(
            [sys.executable, "-m", "abio", "lin", "count", EXAMPLE, "--plugin", "contrib.linear_fable51_1.base",
             "--algo", "fable51-b-count"], cwd=ROOT, capture_output=True, text=True, timeout=120)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("linearizations: 924", out.stdout)


if __name__ == "__main__":
    unittest.main()
