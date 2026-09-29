import random
import unittest

from helpers import example, small_setups

from abio import terms as T
from abio.formats import load_setup
from abio.lin.random_topo import random_linearization
from abio.semantics import execute
from abio.solve.brute import BruteForce


def as_str(sets):
    return {k: sorted(T.format_term(v) for v in vs) for k, vs in sets.items()}


class SolveTests(unittest.TestCase):
    def test_formats_example(self):
        s = load_setup(example("formats-example.setup.yaml"))
        o = BruteForce().solve(s)
        self.assertTrue(o.consistent)
        self.assertEqual(as_str(o.results), {"r1": ["init.1"], "r2": ["1"], "c1": ["1"]})
        self.assertEqual(as_str(o.final), {0: ["2"], 1: ["9", "init.1~7"]})

    def test_witnesses_are_sound(self):
        s = load_setup(example("formats-example.setup.yaml"))
        o = BruteForce().solve(s)
        self.assertEqual(len(o.witnesses), sum(map(len, o.results.values())) + sum(map(len, o.final.values())))
        for w in o.witnesses:
            again = execute(s, w.order, w.effects)
            self.assertTrue(again.consistent)
            c = w.meta["certifies"]
            got = again.results[c["id"]] if "id" in c else again.final[c["block"]]
            self.assertEqual(T.to_value(got), c["value"])

    def test_fixed_union_equals_all(self):
        # Poss over all L must be the union of Poss_L (read-dependent data included).
        from abio.lin.backtrack import linear_extensions
        dep = {"content": {"classes": {"const": 0.3, "copy": 0.4, "combine": 0.3}, "value_pool": 2},
               "knowledge": {"p_w": 0.7, "init_known": 0.5}, "max_in_flight": 1, "actions_per_thread": 3}
        for s, _ in small_setups(8, **dep):
            with self.subTest(s.id):
                allmode = BruteForce(witnesses=False).solve(s)
                res, fin = {}, {}
                for L in linear_extensions(s):
                    o = BruteForce(witnesses=False).solve(s, L)
                    for k, v in o.results.items():
                        res.setdefault(k, set()).update(v)
                    for k, v in o.final.items():
                        fin.setdefault(k, set()).update(v)
                self.assertEqual((allmode.results, allmode.final), (res, fin))

    def test_fixed_is_subset_of_all(self):
        rng = random.Random(0)
        for s, _ in small_setups(6, actions_per_thread=3, max_in_flight=3):
            allmode = BruteForce(witnesses=False).solve(s)
            for _ in range(3):
                o = BruteForce(witnesses=False).solve(s, random_linearization(s, rng))
                for k, v in o.results.items():
                    self.assertLessEqual(v, allmode.results[k])

    def test_generated_observations_are_realizable(self):
        full = {"threads": 2, "sync_points": 1, "events_per_thread": 1, "kind_mix": {"read": 0.5, "write": 0.3, "rcw": 0.2},
                "content": {"classes": {"const": 0.5, "copy": 0.3, "combine": 0.2}, "value_pool": 3},
                "knowledge": {"p_w": 0.8, "p_r": 0.7, "init_known": 0.5}}
        for s, truth in small_setups(10, **full):
            with self.subTest(s.id):
                o = BruteForce(witnesses=False).solve(s)
                self.assertTrue(o.consistent)
                for aid, v in truth.results.items():
                    self.assertIn(v, o.results[aid])  # the hidden run is one feasible schedule
                for b, v in enumerate(truth.final):
                    self.assertIn(v, o.final[b])

    def test_inconsistent(self):
        from abio.model import Setup
        doc = {"format": "setup", "version": 2, "id": "x", "blocks": 1, "sync_points": 0, "init": [0], "threads": [
            {"id": "t0", "steps": [{"read": 0, "id": "r"}, {"done": "r", "data": 5}]}]}
        o = BruteForce().solve(Setup.from_doc(doc))
        self.assertFalse(o.consistent)
        self.assertEqual(o.results, {})


if __name__ == "__main__":
    unittest.main()
