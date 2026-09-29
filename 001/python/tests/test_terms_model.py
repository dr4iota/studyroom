import unittest

from helpers import example

from harness import terms as T
from harness.formats import load_setup, to_string, load_documents
from harness.model import MalformedSetup, Setup


class TermTests(unittest.TestCase):
    def test_canonical(self):
        for src, want in [("init.1~7", "init.1~7"), ("1~w4~init.0", "1~w4~init.0"), ("r1~(r2~7)", "r1~(r2~7)"),
                          ("(a~b)~c", "a~b~c"), (" ( 5 ) ", "5"), (17, "17")]:
            self.assertEqual(T.format_term(T.parse_term(src)), want)

    def test_non_commutative(self):
        self.assertNotEqual(T.parse_term("a~b"), T.parse_term("b~a"))
        self.assertNotEqual(T.parse_term("a~(b~c)"), T.parse_term("a~b~c"))
        self.assertEqual(T.parse_term("17"), T.parse_term(17))

    def test_sort_order(self):
        ts = [T.parse_term(x) for x in ("init.1~7", "17", "9")]
        self.assertEqual([T.format_term(t) for t in T.sorted_terms(ts)], ["9", "17", "init.1~7"])

    def test_expr_substitute(self):
        e = T.parse_expr("r1~7")
        self.assertEqual(T.refs(e), {"r1"})
        v = T.substitute(e, {"r1": T.parse_term("a~b")}.__getitem__)
        self.assertEqual(T.format_term(v), "a~b~7")

    def test_syntax_errors(self):
        for bad in ("", "~", "1~", "(1", "a.b", "init.1~"):
            with self.assertRaises(T.TermSyntaxError):
                T.parse_term(bad)
        with self.assertRaises(T.TermSyntaxError):
            T.parse_expr("init.0")


def _doc(threads, blocks=1, k=0):
    return {"format": "setup", "version": 2, "id": "x", "blocks": blocks, "sync_points": k,
            "init": [0] * blocks, "threads": threads}


class ModelTests(unittest.TestCase):
    def test_example_roundtrip(self):
        s = load_setup(example("formats-example.setup.yaml"))
        self.assertEqual(len(s.actions), 6)
        f = s.features()
        self.assertTrue(f.rcw and f.sync and f.observed_reads and s.has_data_from_reads())
        again = Setup.from_doc(load_documents_from_string(to_string([s.to_doc()])))
        self.assertEqual(again.to_doc(), s.to_doc())
        self.assertEqual(Setup.from_doc(load_documents_from_string(to_string([s.to_doc()], "json"))).to_doc(), s.to_doc())

    def test_base_features(self):
        s = load_setup(example("base.setup.yaml"))
        self.assertEqual(s.features().names(), [])

    def test_poset_names(self):
        s = load_setup(example("formats-example.setup.yaml"))
        self.assertIn("sync.0", s.poset.names)
        self.assertIn("t0.before.0", s.poset.names)
        self.assertIn("c1.done", s.poset.names)
        self.assertEqual(len(s.poset), 15)

    def test_malformed(self):
        cases = {
            "done before start": [{"id": "t0", "steps": [{"done": "r1"}, {"read": 0, "id": "r1"}]}],
            "no done": [{"id": "t0", "steps": [{"read": 0, "id": "r1"}]}],
            "dup id": [{"id": "t0", "steps": [{"read": 0, "id": "a"}, {"done": "a"}, {"read": 0, "id": "a"}, {"done": "a"}]}],
            "dotted id": [{"id": "t0", "steps": [{"read": 0, "id": "a.b"}, {"done": "a.b"}]}],
            "bad block": [{"id": "t0", "steps": [{"read": 3, "id": "a"}, {"done": "a"}]}],
            "write done data": [{"id": "t0", "steps": [{"write": 0, "id": "w", "data": 1}, {"done": "w", "data": 1}]}],
            "ref to incomplete read": [{"id": "t0", "steps": [{"read": 0, "id": "r"}, {"write": 0, "id": "w", "data": "r~1"},
                                                              {"done": "r"}, {"done": "w"}]}],
            "ref to other thread": [{"id": "t0", "steps": [{"read": 0, "id": "r"}, {"done": "r"}]},
                                    {"id": "t1", "steps": [{"write": 0, "id": "w", "data": "r"}, {"done": "w"}]}],
        }
        for name, threads in cases.items():
            with self.subTest(name), self.assertRaises(MalformedSetup):
                Setup.from_doc(_doc(threads))

    def test_sync_cycles(self):
        after_before = [{"id": "t0", "steps": [{"after": 0}, {"before": 0}]}]
        with self.assertRaises(MalformedSetup):
            Setup.from_doc(_doc(after_before, k=1))
        cross = [{"id": "t0", "steps": [{"after": 0}, {"before": 1}]},
                 {"id": "t1", "steps": [{"after": 1}, {"before": 0}]}]
        with self.assertRaises(MalformedSetup):
            Setup.from_doc(_doc(cross, k=2))


def load_documents_from_string(text):
    import tempfile, os
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write(text)
    try:
        return load_documents(fh.name)[0]
    finally:
        os.unlink(fh.name)


if __name__ == "__main__":
    unittest.main()
