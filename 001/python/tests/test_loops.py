"""Loop setups: unrolling, rules, oracles, large-n formulas, and that grading catches bugs."""

import copy
import unittest

from helpers import ROOT  # noqa: F401

from harness import terms as T
from harness.capabilities import Capabilities
from harness.gen.loops import generate_loop
from harness.grade import loops as G
from harness.loop.api import LoopCounter, LoopOutcomes, LoopSolver
from harness.loop.reference import oracle_count, oracle_solve
from harness.loops import LoopSetup
from harness.model import MalformedSetup

CHAIN = {"format": "loop-setup", "version": 1, "id": "chain", "blocks": 2, "sync_points": 0, "loop_sync_points": 1,
         "init": [1, 2], "threads": [
             {"id": "t0", "prefix": [], "body": [{"read": 0, "id": "a"}, {"done": "a"},
                                                 {"write": 1, "id": "wa", "data": "a"}, {"done": "wa"}, {"at": 0}], "suffix": []},
             {"id": "t1", "prefix": [{"write": 0, "id": "p", "data": 5}, {"done": "p"}],
              "body": [{"read": 1, "id": "b"}, {"done": "b"}, {"write": 0, "id": "wb", "data": "b"}, {"done": "wb"}, {"at": 0}],
              "suffix": [{"read": 0, "id": "z"}, {"done": "z"}]}]}


class LoopModel(unittest.TestCase):
    def test_unroll_shape(self):
        L = LoopSetup.from_doc(CHAIN)
        s = L.unroll(3)
        self.assertEqual(len(s.actions), 2 * 2 * 3 + 2)
        self.assertIn("a__3", s.actions)
        self.assertEqual(s.sync_points, 3)  # one per iteration
        self.assertEqual(s.actions["wa__2"].data, T.Ref("a__2"))  # body refs stay within the iteration

    def test_rules(self):
        for path, value in [(("threads", 0, "body", 2, "data"), "a~1"),  # pair in body
                            (("threads", 0, "body", 2, "data"), "*")]:   # unknown in body
            d = copy.deepcopy(CHAIN)
            node = d
            for k in path[:-1]:
                node = node[k]
            node[path[-1]] = value
            with self.subTest(value=value), self.assertRaises(MalformedSetup):
                LoopSetup.from_doc(d)

    def test_counter_formulas_match_oracle(self):
        for seed in range(15):
            L = generate_loop(seed, sync=False)
            f = G._multinomial_count(L)
            for n in (1, 2, 3):
                self.assertEqual(f(n), oracle_count(L, n))

    def test_relay_is_n_dependent_and_stable(self):
        L = G._relay(3, False)
        z = [frozenset(map(T.format_term, oracle_solve(L, n).results["z"])) for n in range(1, 7)]
        self.assertEqual(z[0], {"0"})          # value not there yet
        self.assertEqual(z[2], {"0", "9"})     # can arrive at n = 3
        self.assertEqual(z[4], {"9"})          # forced from n = 5 on
        self.assertEqual(z[4], z[5])


class _OneIterationCounter(LoopCounter):
    name = "bad-loop-count"
    capabilities = Capabilities(sync=True)

    def count(self, setup, n):
        return oracle_count(setup, 1)  # ignores n


class _TwoIterationSolver(LoopSolver):
    name = "bad-loop-solve"
    capabilities = Capabilities(sync=True)

    def solve(self, setup, n):
        return oracle_solve(setup, min(n, 2))  # assumes the answer is settled by n = 2


class GradingCatchesBugs(unittest.TestCase):
    def test_counter_ignoring_n(self):
        insts = G.loop_instances("loop-count", ["b"], "small")
        errs = [e for i in insts for e in G.check_loop_count(_OneIterationCounter(), i, 20)]
        self.assertTrue(any(e["code"] == "COUNT" for e in errs))

    def test_solver_truncating_n(self):
        insts = [i for i in G.loop_instances("loop-solver", ["s"], "small") if i.id.startswith("relay")]
        errs = [e for i in insts for e in G.check_loop_solve(_TwoIterationSolver(), i, 20)]
        self.assertTrue({"UNDER", "OVER"} & {e["code"] for e in errs})

    def test_reference_passes_small_n(self):
        for inst in G.loop_instances("loop-solver", ["b", "s"], "small")[:10]:
            want = oracle_solve(inst.setup, 2)
            got = LoopOutcomes(want.results, want.final)
            self.assertEqual(got.results, oracle_solve(inst.setup, 2).results)


if __name__ == "__main__":
    unittest.main()
