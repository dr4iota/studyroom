"""Tests for deduce.py: hand-checked cases, and the solver against the enumerator."""

import random
import unittest

import deduce as D


def problem(threads, blocks=1, syncs=0, queries=()):
    """threads: {name: (ops, events)}; ops as (kind, block, data_or_obs)."""
    ths = []
    for name, (ops, events) in threads.items():
        out = []
        for k, (kind, b, x) in enumerate(ops):
            oid = f"{name}{k + 1}"
            out.append({"id": oid, "kind": "read", "block": b, "obs": x} if kind == "r"
                       else {"id": oid, "kind": "write", "block": b, "data": x})
        ths.append({"name": name, "ops": out,
                    "events": [{"slot": s, "rel": r, "sync": h} for s, r, h in events]})
    return {"blocks": blocks, "syncs": syncs, "threads": ths, "queries": list(queries)}


def both(p):
    a, _ = D.solve(p, p["queries"])
    b, _ = D.solve_brute(p, p["queries"])
    return a, b


class HandChecked(unittest.TestCase):
    def test_prompt_example(self):
        p = problem({"A": ([("w", 0, 1), ("r", 0, None)], []), "B": ([("w", 0, 2)], [])},
                    queries=[{"read": "A2"}, {"final": 0}])
        a, b = both(p)
        self.assertEqual(a, {(1, 1), (1, 2), (2, 2)})
        self.assertEqual(a, b)

    def test_sync_after_end_orders_effects(self):
        # A1 ends before P, B1 starts after P: B1 must see A1.
        p = problem({"A": ([("w", 0, 1)], [(2, "before", 0)]),
                     "B": ([("r", 0, None)], [(0, "after", 0)])}, syncs=1, queries=[{"read": "B1"}])
        a, b = both(p)
        self.assertEqual(a, {(1,)})
        self.assertEqual(a, b)

    def test_sync_inside_operation_does_not(self):
        # Only A1's start is before P; A1 may take effect after B1.
        p = problem({"A": ([("w", 0, 1)], [(1, "before", 0)]),
                     "B": ([("r", 0, None)], [(0, "after", 0)])}, syncs=1, queries=[{"read": "B1"}])
        a, b = both(p)
        self.assertEqual(a, {(0,), (1,)})
        self.assertEqual(a, b)

    def test_barrier(self):
        p = problem({"A": ([("w", 0, 1), ("r", 0, None)], [(2, "at", 0)]),
                     "B": ([("w", 0, 2), ("r", 0, None)], [(2, "at", 0)])}, syncs=1,
                    queries=[{"read": "A2"}, {"read": "B2"}])
        a, b = both(p)
        # Both writes precede both reads; the reads agree unless... no write between them.
        self.assertEqual(a, {(1, 1), (2, 2)})
        self.assertEqual(a, b)

    def test_copy_and_observation(self):
        p = problem({"A": ([("r", 0, None), ("w", 1, "A1")], []),
                     "B": ([("w", 0, 3), ("r", 1, 3)], [])}, blocks=2, queries=[{"read": "A1"}])
        a, b = both(p)
        self.assertEqual(a, {(3,)})  # B2 saw 3 in y, which only A2 can have copied
        self.assertEqual(a, b)

    def test_cycle_rejected(self):
        p = problem({"A": ([("w", 0, 1)], [(0, "after", 0), (2, "before", 1)]),
                     "B": ([("w", 0, 2)], [(0, "after", 1), (2, "before", 0)])}, syncs=2)
        self.assertIsNone(D.topo_order(D.build_graph(p, effects=False)[0]))


class Traps(unittest.TestCase):
    def test_copy_depth(self):
        p = problem({"A": ([("r", 0, None), ("w", 1, "A1")], []),
                     "B": ([("w", 0, 3), ("r", 1, None)], [])}, blocks=2)
        # B2 reads y: 0 before A2 (the initial 0), or A2's copy of A1 (0 or 3).
        self.assertEqual(D.copy_depths(p, [{"read": "B2"}]), {(0,): 0, (3,): 1})
        self.assertEqual(D.copy_depths(p, [{"final": 1}]), {(0,): 1, (3,): 1})

    def test_interval_trap(self):
        p = problem({"A": ([("w", 0, 1)], [(1, "before", 0)]),
                     "B": ([("r", 0, None)], [(0, "after", 0)])}, syncs=1, queries=[{"read": "B1"}])
        # Treating "before P" as after A1's end hides B1 = 0.
        self.assertEqual(D.traps(p, p["queries"])["interval"], [(0,)])

    def test_refutation_groups(self):
        p = problem({"A": ([("w", 0, 1), ("r", 0, None)], []), "B": ([("w", 0, 2)], [])},
                    queries=[{"read": "A2"}])
        # A2 reads 1 or 2; 0 is plausible, and only A's own order (A1 first) rules it out.
        self.assertEqual(D.solve(p, p["queries"])[0], {(1,), (2,)})
        self.assertEqual(D.refutations(p, p["queries"], {(0,)}), {(0,): ["order:A"]})

    def test_relaxations_are_supersets(self):
        rng = random.Random(9)
        for seed in range(120):
            params = {"threads": 3, "ops": rng.randint(2, 4), "blocks": 2, "p_obs": rng.choice([0, 0.4]),
                      "p_copy": 0.8, "min_answers": 1, "max_answers": 10**6}
            p = D.generate(params, seed)
            if p is None:
                continue
            t = D.solve(p, p["queries"])[0]
            poss = D.copy_sources(p)
            for kw in [{"drop_obs": True}, {"free": 0}, {"free": 2}, {"decouple": poss}]:
                self.assertTrue(t <= D.solve_relaxed(p, p["queries"], **kw), (seed, kw))

    def test_depths_cover_answers(self):
        rng = random.Random(3)
        for seed in range(150):
            params = {"threads": rng.randint(2, 3), "ops": rng.randint(2, 4), "blocks": rng.randint(1, 2),
                      "syncs": rng.randint(0, 2), "p_obs": rng.choice([0, 0.3]), "p_copy": rng.choice([0.5, 1]),
                      "min_answers": 1, "max_answers": 10**6}
            p = D.generate(params, seed)
            if p is None:
                continue
            self.assertEqual(set(D.copy_depths(p, p["queries"])), D.solve(p, p["queries"])[0], seed)

    def test_adversarial_selection(self):
        params = {"threads": 2, "ops": 4, "blocks": 2, "p_copy": 0.8, "adversarial": 1, "min_answers": 4}
        found = [p for p in (D.generate(params, s) for s in range(40)) if p]
        self.assertTrue(found)
        for p in found:
            self.assertGreater(D.traps(p, p["queries"])["score"], 0)


class Conditional(unittest.TestCase):
    def test_final_value_given(self):
        p = problem({"A": ([("w", 0, 1), ("r", 0, None)], []), "B": ([("w", 0, 2)], [])},
                    queries=[{"read": "A2"}])
        p["given_final"] = [{"block": 0, "value": 1}]
        # x ends as 1, so B1 came before A1, and A2 read 1.
        a, b = both(p)
        self.assertEqual(a, {(1,)})
        self.assertEqual(a, b)
        self.assertIn("At the end: x = 1.", D.render(p))

    def test_conditional_selection(self):
        params = {"threads": 3, "ops": 4, "blocks": 2, "values": 3, "p_copy": 0.8, "adversarial": 4,
                  "max_queries": 1, "min_answers": 1, "max_answers": 4}
        found = [p for p in (D.generate(params, s) for s in range(60)) if p]
        self.assertTrue(found)
        for p in found:
            a, b = both(p)
            self.assertEqual(a, b)
            self.assertNotIn(tuple(p["trap"]), a)
            self.assertEqual(p["prompt"], "v2")


class StaleAndSeparable(unittest.TestCase):
    def test_stale_copy(self):
        # A1 reads x early (0); B1 then writes 5; A2 copies A1's 0 into y after that: stale.
        p = problem({"A": ([("r", 0, None), ("w", 1, "A1")], []), "B": ([("w", 0, 5)], [])},
                    blocks=2, queries=[{"final": 1}])
        self.assertEqual(D.solve(p, p["queries"])[0], {(0,), (5,)})
        # Without stale copies, a read of 0 must be copied before B1 writes 5... which is
        # still possible (A1, A2, B1), so 0 is not stale-only; 5 needs no stale copy either.
        self.assertEqual(D.traps(p, p["queries"])["stale"], [])
        q = problem({"A": ([("r", 0, None), ("w", 1, "A1")], []), "B": ([("w", 0, 5), ("w", 1, 3)], [])},
                    blocks=2, queries=[{"read": "A1"}, {"final": 1}])
        # y ends as 0 only if A2 comes after B2, hence after B1; with A1 = 0, A1 came before
        # B1, so A2 copies a 0 that x no longer holds: (0, 0) needs a stale copy.
        self.assertEqual(D.solve(q, q["queries"])[0], {(0, 0), (0, 3), (5, 3), (5, 5)})
        self.assertEqual(D.traps(q, q["queries"])["stale"], [(0, 0)])

    def test_stale_rows_are_true_rows(self):
        rng = random.Random(4)
        for seed in range(100):
            params = {"threads": 2, "ops": rng.randint(3, 5), "blocks": 2, "p_copy": 0.8,
                      "min_answers": 1, "max_answers": 10**6}
            p = D.generate(params, seed)
            if p is None:
                continue
            self.assertTrue(D.stale_rows(p, p["queries"]) <= D.solve(p, p["queries"])[0])

    def test_separable(self):
        self.assertTrue(D.separable({(5, 4), (5, 6)}, 2))
        self.assertTrue(D.separable({(1, 4), (1, 6), (2, 4), (2, 6)}, 2))
        self.assertFalse(D.separable({(1, 4), (2, 6)}, 2))
        self.assertTrue(D.separable({(1, 4, 0), (2, 6, 0)}, 3))
        self.assertFalse(D.separable({(1, 4, 0), (2, 6, 0), (1, 6, 1)}, 3))


class SolverVsBrute(unittest.TestCase):
    def test_random(self):
        rng = random.Random(7)
        checked = 0
        for seed in range(400):
            params = {
                "threads": rng.randint(2, 3), "ops": rng.randint(1, 3), "blocks": rng.randint(1, 2),
                "values": rng.randint(1, 3), "syncs": rng.randint(0, 2), "p_obs": rng.choice([0, 0.3, 1]),
                "p_copy": rng.choice([0, 0.6]), "min_answers": 1, "max_answers": 10**6,
            }
            p = D.generate(params, seed)
            if p is None:
                continue
            for k in range(3):
                cands = [{"read": op["id"]} for op in D.flat_ops(p) if op["kind"] == "read"]
                cands += [{"final": b} for b in range(p["blocks"])]
                qs = rng.sample(cands, min(len(cands), rng.randint(1, 3)))
                a, _ = D.solve(p, qs)
                b, _ = D.solve_brute(p, qs)
                self.assertEqual(a, b, (seed, qs))
                self.assertTrue(a)  # generated problems always have an execution
                checked += 1
        self.assertGreater(checked, 500)


class Parsing(unittest.TestCase):
    def test_parse(self):
        text = "reasoning\nBEGIN\n1 2\n\n3 4\nEND\nnoise\n```\nBEGIN\n5 6\n7, 8\n9\nEND\n```"
        rows, bad = D.parse_answer(text, 2)
        self.assertEqual(rows, {(5, 6), (7, 8)})
        self.assertEqual(bad, ["9"])
        self.assertEqual(D.parse_answer("no block", 2), (None, []))


if __name__ == "__main__":
    unittest.main()
