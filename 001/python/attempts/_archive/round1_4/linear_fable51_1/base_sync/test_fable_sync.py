"""Tests for the ``fable51-s-*`` linearizers (base problem plus sync).  Run from ``python/``:

    ulimit -v 2000000; timeout 600 python3 -m unittest attempts._archive.round1_4.linear_fable51_1.base_sync.test_fable_sync -v

Every enumerator is checked on the shipped examples, on many generated setups with sync
(every subset of the relations ``before``/``after``/``at``), on generated base setups
(``K = 0``) and on hand-built edge cases: each output is a valid linearization
(``poset.check``), there are no duplicates, and the number of outputs equals the
positions-DP count. ``fable51-s-pr`` is checked for its delay-2 property (every
consecutive pair differs by exactly one or two adjacent transpositions). Instances are
capped at 200 000 linearizations and streamed; nothing large is ever materialised.
"""

from __future__ import annotations

import itertools
import os
import subprocess
import sys
import unittest

ROOT = next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "harness").is_dir()).__str__()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import harness.lin  # noqa: E402,F401  (register built-ins)
from harness.formats import load_setup  # noqa: E402
from harness.gen import generate  # noqa: E402
from harness.lin.backtrack import linear_extensions as backtrack  # noqa: E402
from harness.lin.dp import count_linearizations  # noqa: E402
from harness.model import Setup  # noqa: E402

from attempts._archive.round1_4.linear_fable51_1.base_sync.common import cut_segments  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.base_sync.cut import FableSyncCut  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.base_sync.dp import FableSyncCount, FableSyncDP  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.base_sync.pr import FableSyncPR  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.base_sync.tree import FableSyncTree  # noqa: E402
from attempts._archive.round1_4.linear_fable51_1.base_sync.vr import FableSyncVR  # noqa: E402

ENUMERATORS = [FableSyncPR, FableSyncVR, FableSyncTree, FableSyncDP, FableSyncCut]
LIMIT = 200_000  # absolute cap on |Lin(P)| for any enumerated instance
GEN_LIMIT = 20_000  # cap for the bulk generated sweep (hundreds of instances)
EXAMPLES = os.path.join(ROOT, "examples")
BASE_EXAMPLE = os.path.join(EXAMPLES, "base.setup.yaml")
FORMATS_EXAMPLE = os.path.join(EXAMPLES, "formats-example.setup.yaml")
RELATION_SETS = [list(r) for k in (1, 2, 3) for r in itertools.combinations(["before", "after", "at"], k)]


def doc(threads: list[list[dict]], sync_points: int, id: str = "fable-sync-edge") -> dict:
    return {"format": "setup", "version": 2, "id": id, "blocks": 2, "sync_points": sync_points,
            "init": [0, 0], "threads": [{"id": f"t{t}", "steps": s} for t, s in enumerate(threads)]}


_ids = itertools.count()


def rw(t: int, k: int) -> list[dict]:
    """One write action (start + done) with a fresh unique id."""
    a = f"w{t}_{next(_ids)}"
    return [{"write": k % 2, "id": a, "data": k}, {"done": a}]


def actions(t: int, m: int) -> list[dict]:
    return [s for k in range(m) for s in rw(t, k)]


def edge_cases() -> dict[str, dict]:
    cases: dict[str, dict] = {}
    # an unused sync point (isolated node), also with K = 2 and one used
    cases["unused sync"] = doc([actions(0, 2), actions(1, 2)], 1)
    cases["two unused sync"] = doc([actions(0, 2), actions(1, 1)], 2)
    cases["one used one unused"] = doc([actions(0, 2) + [{"before": 1}], [{"after": 1}] + actions(1, 2)], 2)
    # only before / only after
    cases["only before"] = doc([actions(0, 1) + [{"before": 0}] + actions(0, 1), actions(1, 1) + [{"before": 0}]], 1)
    cases["only after"] = doc([[{"after": 0}] + actions(0, 2), actions(1, 1) + [{"after": 0}] + actions(1, 1)], 1)
    # full at barrier across all threads; chain of barriers
    cases["full barrier"] = doc([actions(0, 1) + [{"at": 0}] + actions(0, 1), actions(1, 2) + [{"at": 0}],
                                 [{"at": 0}] + actions(2, 1)], 1)
    cases["chain of barriers"] = doc([actions(0, 1) + [{"at": 0}] + actions(0, 1) + [{"at": 1}] + actions(0, 1),
                                      actions(1, 1) + [{"at": 0}] + [{"at": 1}] + actions(1, 1)], 2)
    cases["three barriers three threads"] = doc(
        [actions(0, 1) + [{"at": 0}] + [{"at": 1}] + actions(0, 1) + [{"at": 2}],
         [{"at": 0}] + actions(1, 1) + [{"at": 1}] + [{"at": 2}] + actions(1, 1),
         actions(2, 1) + [{"at": 0}] + actions(2, 1) + [{"at": 1}] + actions(2, 1) + [{"at": 2}]], 3)
    # partial barrier plus before/after from the third thread
    cases["partial barrier"] = doc([actions(0, 1) + [{"at": 0}] + actions(0, 1), [{"at": 0}] + actions(1, 2),
                                    actions(2, 1) + [{"before": 0}] + actions(2, 1) + [{"after": 0}]], 1)
    # one thread with before: k then after: k
    cases["before then after"] = doc([actions(0, 1) + [{"before": 0}] + actions(0, 1) + [{"after": 0}] + actions(0, 1),
                                      actions(1, 1) + [{"at": 0}] + actions(1, 1)], 1)
    cases["before then after alone"] = doc([[{"before": 0}] + actions(0, 2) + [{"after": 0}], actions(1, 2)], 1)
    # event as first / last step, inside an in-flight action
    cases["event first"] = doc([[{"before": 0}] + actions(0, 2), [{"after": 0}] + actions(1, 2)], 1)
    cases["event last"] = doc([actions(0, 2) + [{"before": 0}], actions(1, 2) + [{"after": 0}]], 1)
    cases["event in flight"] = doc(
        [[{"write": 0, "id": "a", "data": 1}, {"write": 1, "id": "b", "data": 2}, {"before": 0}, {"done": "a"},
          {"at": 1}, {"done": "b"}],
         [{"read": 0, "id": "r"}, {"after": 0}, {"at": 1}, {"done": "r"}]], 2)
    # sync point with at on one thread and before/after on others
    cases["at plus before after"] = doc([actions(0, 1) + [{"at": 0}] + actions(0, 1), actions(1, 1) + [{"before": 0}],
                                         [{"after": 0}] + actions(2, 1)], 1)
    # K = 0 base setups
    cases["base"] = doc([actions(0, 3), actions(1, 2)], 0)
    cases["base one thread"] = doc([actions(0, 3)], 0)
    cases["base empty"] = doc([[], []], 0)
    cases["base one action"] = doc([actions(0, 1)], 0)
    # degenerate sync-only setups
    cases["only sync nodes"] = doc([[], []], 2)
    cases["single event thread"] = doc([[{"before": 0}]], 1)
    cases["single at thread"] = doc([[{"at": 0}]], 1)
    cases["one thread two events"] = doc([[{"before": 0}, {"after": 1}]], 2)
    cases["total order"] = doc([[{"at": 0}] + actions(0, 1) + [{"at": 1}], [{"at": 0}, {"at": 1}]], 2)
    return cases


def generated_sync(seeds=range(3)):
    shapes = [
        {"threads": 2, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 1},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 3},
        {"threads": 4, "actions_per_thread": 1, "max_in_flight": 1},
        {"threads": 2, "actions_per_thread": {"total": {"read": 3, "write": 2}}, "max_in_flight": 3},
    ]
    for seed in seeds:
        for shape in shapes:
            for K in (1, 2, 3):
                for R in RELATION_SETS:
                    for E in range(1, min(K * len(R), 3) + 1):
                        hp = {"seed": seed, "blocks": 2, "sync_points": K, "events_per_thread": E, "relations": R, **shape}
                        try:
                            setup, _ = generate(hp)
                        except RuntimeError:
                            continue  # the generator found no acyclic placement for these hyperparameters
                        yield hp, setup


def generated_base(seeds=range(4)):
    shapes = [
        {"threads": 2, "actions_per_thread": 3, "max_in_flight": 2},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 1},
        {"threads": 4, "actions_per_thread": 1, "max_in_flight": 1},
        {"threads": 3, "actions_per_thread": 2, "max_in_flight": 3},
    ]
    for seed in seeds:
        for shape in shapes:
            setup, _ = generate({"seed": seed, "blocks": 2, **shape})
            yield setup


def adjacent_swaps(a):
    for i in range(len(a) - 1):
        b = list(a)
        b[i], b[i + 1] = b[i + 1], b[i]
        yield tuple(b)


def within_two_adjacent_swaps(a, b) -> bool:
    """True iff ``b`` is obtained from ``a`` by exactly one or two adjacent transpositions."""
    if a == b:
        return False
    if sum(1 for i in range(len(a)) if a[i] != b[i]) > 4:
        return False
    for c in adjacent_swaps(a):
        if c == b or any(d == b for d in adjacent_swaps(c)):
            return True
    return False


class FableSyncTests(unittest.TestCase):
    def check_enum(self, algo, setup, gray=False):
        """Validity, uniqueness, count (and the delay-2 property when ``gray``); returns the count."""
        P = setup.poset
        n = count_linearizations(setup)
        self.assertLessEqual(n, LIMIT, "test instance too large")
        seen = set()
        prev = None
        for o in algo.enumerate(setup):
            self.assertEqual(len(o), len(P))
            self.assertEqual(P.check(P.to_names(o)), [], f"{algo.name}: invalid {o}")
            self.assertNotIn(o, seen, f"{algo.name}: duplicate {o}")
            seen.add(o)
            if gray and prev is not None:
                self.assertTrue(within_two_adjacent_swaps(prev, o), f"{algo.name}: {prev} -> {o}")
            prev = o
        self.assertEqual(len(seen), n, f"{algo.name}: wrong number of outputs")
        return n

    def check_all(self, setup, tag, cap=LIMIT):
        if count_linearizations(setup) > cap:
            return  # generated instance too large to enumerate safely
        for cls in ENUMERATORS:
            with self.subTest(algo=cls.name, setup=tag):
                self.check_enum(cls(), setup, gray=cls is FableSyncPR)
        with self.subTest(algo="fable51-s-count", setup=tag):
            self.assertEqual(FableSyncCount().count(setup).linearizations, count_linearizations(setup))

    # ---- examples

    def test_base_example_924(self):
        s = load_setup(BASE_EXAMPLE)
        for cls in ENUMERATORS:
            with self.subTest(cls.name):
                self.assertEqual(self.check_enum(cls(), s, gray=cls is FableSyncPR), 924)
        self.assertEqual(FableSyncCount().count(s).linearizations, 924)

    def test_formats_example_45(self):
        # Uses RCW and an observed read; for a linearizer an RCW is just an action.
        s = load_setup(FORMATS_EXAMPLE)
        for cls in ENUMERATORS:
            with self.subTest(cls.name):
                self.assertEqual(self.check_enum(cls(), s, gray=cls is FableSyncPR), 45)
        self.assertEqual(FableSyncCount().count(s).linearizations, 45)

    # ---- generated

    def test_generated_sync(self):
        n = 0
        for hp, s in generated_sync():
            self.check_all(s, str(hp), cap=GEN_LIMIT)  # many instances: keep each one small
            n += 1
        self.assertGreater(n, 100)

    def test_generated_base(self):
        for s in generated_base():
            self.check_all(s, s.id)

    def test_generated_bigger_sync(self):
        # A few larger instances (still under the cap), including ones without at-barriers.
        hps = [
            {"seed": 1, "threads": 3, "actions_per_thread": 3, "max_in_flight": 2, "sync_points": 2, "events_per_thread": 2, "relations": ["before", "after"]},
            {"seed": 2, "threads": 2, "actions_per_thread": 5, "max_in_flight": 3, "sync_points": 2, "events_per_thread": 2, "relations": ["before", "after", "at"]},
            {"seed": 5, "threads": 4, "actions_per_thread": 2, "max_in_flight": 2, "sync_points": 3, "events_per_thread": 2, "relations": ["at"]},
            {"seed": 8, "threads": 3, "actions_per_thread": 2, "max_in_flight": 2, "sync_points": 3, "events_per_thread": 1, "relations": ["before"]},
        ]
        for hp in hps:
            s, _ = generate({"blocks": 2, **hp})
            if count_linearizations(s) <= LIMIT:
                self.check_all(s, str(hp))

    # ---- hand-built edge cases

    def test_edge_cases(self):
        for name, d in edge_cases().items():
            self.check_all(Setup.from_doc(d), name)

    def test_edge_case_counts_by_hand(self):
        c = edge_cases()
        # unused sync: 4 + 4 nodes interleaved (C(8,4) = 70) times 9 slots for the isolated node
        self.assertEqual(count_linearizations(Setup.from_doc(c["unused sync"])), 70 * 9)
        # only sync nodes: two isolated nodes
        self.assertEqual(count_linearizations(Setup.from_doc(c["only sync nodes"])), 2)
        self.assertEqual(count_linearizations(Setup.from_doc(c["total order"])), 1)
        self.assertEqual(count_linearizations(Setup.from_doc(c["base empty"])), 1)
        # full barrier: segment before (2 + 4 + 0 nodes, C(6,2)=15), sync, segment after (2 + 0 + 2, C(4,2)=6)
        self.assertEqual(count_linearizations(Setup.from_doc(c["full barrier"])), 15 * 6)

    def test_cut_segments(self):
        c = edge_cases()
        s = Setup.from_doc(c["full barrier"])
        segs = cut_segments(s.poset)
        self.assertEqual([len(x) for x in segs], [6, 1, 4])
        self.assertEqual(s.poset.names[segs[1][0]], "sync.0")
        s = Setup.from_doc(c["chain of barriers"])
        # between the barriers thread 0 alone has one action: its two endpoints are cut nodes too
        self.assertEqual([len(x) for x in cut_segments(s.poset)], [4, 1, 1, 1, 1, 4])
        s = Setup.from_doc(c["total order"])
        self.assertEqual([len(x) for x in cut_segments(s.poset)], [1, 1, 1, 1])
        s = Setup.from_doc(c["base"])
        self.assertEqual([len(x) for x in cut_segments(s.poset)], [10])
        s = Setup.from_doc(c["base one thread"])
        self.assertEqual([len(x) for x in cut_segments(s.poset)], [1] * 6)

    # ---- algorithm-specific properties

    def test_pr_delay_two_on_all_edge_cases(self):
        # (also checked inside check_enum; here for the base example with a counted number of 2-steps)
        s = load_setup(BASE_EXAMPLE)
        prev = None
        ones = twos = 0
        for o in FableSyncPR().enumerate(s):
            if prev is not None:
                if o in set(adjacent_swaps(prev)):
                    ones += 1
                else:
                    self.assertTrue(within_two_adjacent_swaps(prev, o))
                    twos += 1
            prev = o
        self.assertEqual(ones + twos, 923)
        self.assertGreater(twos, 0)  # a pure one-transposition Gray code does not exist here (472 vs 452)

    def test_tree_parent_child_one_swap(self):
        # Each output of fable51-s-tree is one adjacent swap away from some earlier output (its parent).
        s = load_setup(FORMATS_EXAMPLE)
        seen = set()
        for i, o in enumerate(FableSyncTree().enumerate(s)):
            if i > 0:
                self.assertTrue(any(p in seen for p in adjacent_swaps(o)), o)
            seen.add(o)

    def test_dp_lexicographic_and_rank_options(self):
        for hp, s in list(generated_sync(range(1)))[:12] + [(None, load_setup(FORMATS_EXAMPLE))]:
            P = s.poset
            full = list(FableSyncDP().enumerate(s))
            labels = [tuple(P.chain_of[x] for x in o) for o in full]
            self.assertEqual(labels, sorted(labels))
            n = len(full)
            self.assertEqual(list(FableSyncDP(start=n // 2).enumerate(s)), full[n // 2:])
            self.assertEqual(list(FableSyncDP(start=3, stop=9).enumerate(s)), full[3:9])
            self.assertEqual(list(FableSyncDP(step=5).enumerate(s)), full[::5])
            self.assertEqual(list(FableSyncDP(start=2, stop=n + 50, step=7).enumerate(s)), full[2::7])
            self.assertEqual(list(FableSyncDP(start=n).enumerate(s)), [])

    def test_cut_equals_pr_without_cuts_and_small_cache(self):
        s = load_setup(BASE_EXAMPLE)
        self.assertEqual(list(FableSyncCut().enumerate(s)), list(FableSyncPR().enumerate(s)))
        c = Setup.from_doc(edge_cases()["chain of barriers"])
        self.assertEqual(self.check_enum(FableSyncCut(cache=0), c), count_linearizations(c))

    def test_agree_with_backtrack_as_sets(self):
        for hp, s in list(generated_sync(range(1)))[::9]:
            if count_linearizations(s) > 20_000:
                continue
            ref = set(backtrack(s))
            for cls in ENUMERATORS:
                self.assertEqual(set(cls().enumerate(s)), ref, cls.name)

    def test_lazy(self):
        s, _ = generate({"seed": 1, "threads": 4, "actions_per_thread": 4, "max_in_flight": 2, "sync_points": 2,
                         "events_per_thread": 1, "relations": ["before", "after"]})
        self.assertGreater(count_linearizations(s), 10**7)
        for cls in ENUMERATORS:
            it = cls().enumerate(s)
            first = [next(it) for _ in range(50)]
            self.assertEqual(len(set(first)), 50)

    # ---- CLI

    def test_cli(self):
        env = dict(os.environ, PYTHONPATH=ROOT)
        for cls in ENUMERATORS:
            out = subprocess.run(
                [sys.executable, "-m", "harness", "lin", "enum", BASE_EXAMPLE, "--plugin", "attempts._archive.round1_4.linear_fable51_1.base_sync",
                 "--algo", cls.name, "--count-only"], cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertEqual(out.stdout.strip(), "924", cls.name)
        # A generated sync setup: the enumerators' --count-only must match `lin count` (dp-positions).
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "sync.setup.yaml")
            out = subprocess.run(
                [sys.executable, "-m", "harness", "gen", "--set", "sync_points=2", "--set", "events_per_thread=2", "-o", f],
                cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            ref = subprocess.run([sys.executable, "-m", "harness", "lin", "count", f], cwd=ROOT, env=env,
                                 capture_output=True, text=True)
            self.assertEqual(ref.returncode, 0, ref.stderr)
            expected = [l for l in ref.stdout.splitlines() if l.startswith("linearizations:")]
            self.assertEqual(len(expected), 1, ref.stdout)
            n = int(expected[0].split(":")[1])
            self.assertLessEqual(n, LIMIT)
            for cls in ENUMERATORS:
                out = subprocess.run(
                    [sys.executable, "-m", "harness", "lin", "enum", f, "--plugin", "attempts._archive.round1_4.linear_fable51_1.base_sync", "--algo", cls.name,
                     "--count-only"], cwd=ROOT, env=env, capture_output=True, text=True)
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertEqual(out.stdout.strip(), str(n), cls.name)
            out = subprocess.run(
                [sys.executable, "-m", "harness", "lin", "count", f, "--plugin", "attempts._archive.round1_4.linear_fable51_1.base_sync", "--algo", "fable51-s-count"],
                cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn(f"linearizations: {n}", out.stdout)


if __name__ == "__main__":
    unittest.main()
