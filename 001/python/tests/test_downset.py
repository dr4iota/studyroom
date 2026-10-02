"""The down-set reference solver against the brute-force oracle, on every case."""

import random
import unittest

from helpers import small_setups

from harness.grade.instances import suite
from harness.lin.random_topo import random_linearization
from harness.solve.brute import BruteForce
from harness.solve.downset import solve_downset

CASES = {
    "b": {},
    "s": {"sync_points": 2, "events_per_thread": 2},
    "o": {"knowledge": {"p_r": 0.7}},
    "so": {"sync_points": 1, "events_per_thread": 1, "knowledge": {"p_r": 0.7}},
    "r": {"kind_mix": {"read": 0.4, "write": 0.3, "rcw": 0.3}, "knowledge": {"p_r": 0.5}},
}
MIX = {"content": {"classes": {"const": 0.3, "copy": 0.4, "combine": 0.3}, "value_pool": 2},
       "max_in_flight": 2, "actions_per_thread": 3}


def same(a, b):
    return (a.consistent, a.results if a.consistent else {}, a.final if a.consistent else {}) == \
           (b.consistent, b.results if b.consistent else {}, b.final if b.consistent else {})


class DownsetVsBrute(unittest.TestCase):
    def test_generated_all_mode(self):
        for case, hp in CASES.items():
            for s, _ in small_setups(10, **MIX, **hp):
                with self.subTest(case=case, setup=s.id):
                    self.assertTrue(same(solve_downset(s), BruteForce(witnesses=False).solve(s)))

    def test_generated_fixed_mode(self):
        rng = random.Random(1)
        for case, hp in CASES.items():
            for s, _ in small_setups(4, **MIX, **hp):
                for _ in range(3):
                    L = random_linearization(s, rng)
                    with self.subTest(case=case, setup=s.id):
                        self.assertTrue(same(solve_downset(s, L), BruteForce(witnesses=False).solve(s, L)))

    def test_adversarial_suite(self):
        for inst in suite():
            with self.subTest(inst.id):
                self.assertTrue(same(solve_downset(inst.setup), BruteForce(witnesses=False).solve(inst.setup)))


if __name__ == "__main__":
    unittest.main()
