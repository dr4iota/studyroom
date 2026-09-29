"""RCW semantics: the brute oracle against answers derived by hand.

RCW(b, expect, data) at its effect point: result := current content; if the content
equals ``expect``, the content becomes ``data``. Every answer below is worked out in the
comment above its case, independently of the code.
"""

import unittest

from helpers import ROOT  # noqa: F401

from harness import terms as T
from harness.model import Setup
from harness.solve.brute import BruteForce


def R(i, b, obs=None):
    return [{"read": b, "id": i}, {"done": i} if obs is None else {"done": i, "data": obs}]


def W(i, b, data):
    return [{"write": b, "id": i, "data": data}, {"done": i}]


def C(i, b, expect, data, obs=None):
    return [{"rcw": b, "id": i, "expect": expect, "data": data}, {"done": i} if obs is None else {"done": i, "data": obs}]


def setup(threads, blocks=1, init=None):
    return Setup.from_doc({"format": "setup", "version": 2, "id": "rcw", "blocks": blocks, "sync_points": 0,
                           "init": init or [0] * blocks, "threads": [{"id": f"t{i}", "steps": st} for i, st in enumerate(threads)]})


def solve(s):
    o = BruteForce(witnesses=False).solve(s)
    return o.consistent, {k: sorted(map(T.format_term, v)) for k, v in o.results.items()}, \
        {b: sorted(map(T.format_term, v)) for b, v in o.final.items()}


class RcwOracle(unittest.TestCase):
    def test_sequential(self):
        # one thread: write 1, then RCW(expect 1 -> 2), then read. Everything is forced.
        ok, res, fin = solve(setup([W("w1", 0, 1) + C("c1", 0, 1, 2) + R("r1", 0)]))
        self.assertEqual((ok, res, fin), (True, {"c1": ["1"], "r1": ["2"]}, {0: ["2"]}))

    def test_fails_after_intervening_write(self):
        # c1 expects the initial 0; w1 = 1 is concurrent. c1 first: sees 0, writes 5, then w1 -> 1.
        # w1 first: c1 sees 1 and fails. Either way the block ends at 1.
        ok, res, fin = solve(setup([C("c1", 0, 0, 5), W("w1", 0, 1)]))
        self.assertEqual((res, fin), ({"c1": ["0", "1"]}, {0: ["1"]}))

    def test_mutual_exclusion(self):
        # two concurrent CAS 0->1 and 0->2: exactly one succeeds; the loser sees the winner's value.
        ok, res, fin = solve(setup([C("c1", 0, 0, 1), C("c2", 0, 0, 2)]))
        self.assertEqual((res, fin), ({"c1": ["0", "2"], "c2": ["0", "1"]}, {0: ["1", "2"]}))

    def test_aba(self):
        # t0 writes 1 then 0 (in order); t1 does CAS 0->9, then reads.
        # c1 before w1: succeeds, then w1, w2 -> final 0; r1 sees 9, 1 or 0.
        # c1 between w1 and w2: sees 1, fails -> final 0.  c1 after w2: sees 0, succeeds -> final 9.
        ok, res, fin = solve(setup([W("w1", 0, 1) + W("w2", 0, 0), C("c1", 0, 0, 9) + R("r1", 0)]))
        self.assertEqual(res["c1"], ["0", "1"])
        self.assertEqual(res["r1"], ["0", "1", "9"])
        self.assertEqual(fin, {0: ["0", "9"]})

    def test_observed_result_forces_order(self):
        # mutual exclusion, but c1 is observed to have found 2: so c2 went first and succeeded.
        ok, res, fin = solve(setup([C("c1", 0, 0, 1, obs=2), C("c2", 0, 0, 2)]))
        self.assertEqual((ok, res, fin), (True, {"c1": ["2"], "c2": ["0"]}, {0: ["2"]}))

    def test_observed_result_impossible(self):
        # a lone CAS cannot find a value nobody writes
        ok, _, _ = solve(setup([C("c1", 0, 0, 1, obs=7)]))
        self.assertFalse(ok)

    def test_data_from_read(self):
        # c1 writes r1~1, where r1 reads block 1 (0, or 4 from w1). c1 always finds 0 and succeeds.
        ok, res, fin = solve(setup([R("r1", 1) + C("c1", 0, 0, "r1~1"), W("w1", 1, 4)], blocks=2))
        self.assertEqual(res["c1"], ["0"])
        self.assertEqual(fin[0], ["0~1", "4~1"])

    def test_expect_from_read(self):
        # c1 expects what r1 read from block 0 itself; w1 = 3 is concurrent. c1's result is the
        # OLD content it finds: 0 (w1 not yet in) or 3 (w1 in), never the 8 it writes.
        # r1 = 0 and nothing in between: success -> 8. r1 = 0 but w1 lands in between: fail, stays 3.
        # r1 = 3 (w1 already done): c1 sees 3 = expect -> 8.  w1 after c1's effect: final 3.
        ok, res, fin = solve(setup([R("r1", 0) + C("c1", 0, "r1", 8), W("w1", 0, 3)]))
        self.assertEqual(res["c1"], ["0", "3"])
        self.assertEqual(fin, {0: ["3", "8"]})


if __name__ == "__main__":
    unittest.main()
