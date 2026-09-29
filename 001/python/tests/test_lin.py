import random
import unittest
from collections import Counter

from helpers import example, small_setups

from abio.formats import load_setup
from abio.lin.backtrack import Backtrack
from abio.lin.dp import PositionsDPCounter, PositionsDPSampler
from abio.lin.feasible import EnumerationCounter, FeasibleBacktrack, RejectionSampler
from abio.lin.random_topo import RandomTopo
from abio.semantics import is_feasible

# Keep instances tiny: |Lin(P)| is exponential (3 threads x 6 steps is ~17M orders).
SYNC = {"sync_points": 2, "events_per_thread": 2, "threads": 2}


class LinTests(unittest.TestCase):
    def check_enum(self, setup, limit=200_000):
        n = PositionsDPCounter().count(setup).linearizations
        self.assertLessEqual(n, limit, "test instance too large")
        seen = set()
        for o in Backtrack().enumerate(setup):
            self.assertNotIn(o, seen, "duplicate")
            seen.add(o)
            self.assertEqual(setup.poset.check(setup.poset.to_names(o)), [])
        self.assertEqual(len(seen), n)
        return n

    def test_base_multinomial(self):
        s = load_setup(example("base.setup.yaml"))
        self.assertEqual(self.check_enum(s), 924)  # C(12, 6)

    def test_enum_equals_count(self):
        for s, _ in small_setups(15):
            self.check_enum(s)

    def test_enum_equals_count_sync(self):
        for s, _ in small_setups(15, **SYNC):
            with self.subTest(s.id):
                self.check_enum(s)

    def test_samplers_valid(self):
        rng = random.Random(1)
        for s, _ in small_setups(5, **SYNC):
            for algo in (RandomTopo(), PositionsDPSampler()):
                for o in algo.samples(s, rng, 20):
                    self.assertEqual(s.poset.check(s.poset.to_names(o)), [])

    def test_dp_uniform(self):
        s, _ = next(small_setups(1, actions_per_thread=1))  # 2 chains of 2 -> 6 linearizations
        n = PositionsDPCounter().count(s).linearizations
        c = Counter(PositionsDPSampler().samples(s, random.Random(0), 600 * n))
        self.assertEqual(len(c), n)
        self.assertLess(max(c.values()) / min(c.values()), 1.3)

    def test_feasible_reduces(self):
        s = load_setup(example("formats-example.setup.yaml"))
        c = EnumerationCounter().count(s)
        feas = list(FeasibleBacktrack().enumerate(s))
        self.assertEqual(c.feasible, len(feas))
        self.assertLessEqual(c.feasible, c.linearizations)
        o = next(RejectionSampler().samples(s, random.Random(0), 1))
        self.assertTrue(is_feasible(s, o))

    def test_observations_reduce_linearizations(self):
        # t1 reads 1 only if it sees t0's write: forces w.start < r.done.
        from abio.model import Setup
        doc = {"format": "setup", "version": 2, "id": "x", "blocks": 1, "sync_points": 0, "init": [0], "threads": [
            {"id": "t0", "steps": [{"write": 0, "id": "w", "data": 1}, {"done": "w"}]},
            {"id": "t1", "steps": [{"read": 0, "id": "r"}, {"done": "r", "data": 1}]}]}
        s = Setup.from_doc(doc)
        c = EnumerationCounter().count(s)
        self.assertEqual((c.linearizations, c.feasible), (6, 5))  # only r, r.done, w, w.done is infeasible


if __name__ == "__main__":
    unittest.main()
