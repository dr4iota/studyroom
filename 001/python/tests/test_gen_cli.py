import contextlib
import io
import os
import tempfile
import unittest

from helpers import example, small_setups

from abio import terms as T
from abio.cli import main
from abio.formats import load_document, to_string
from abio.gen import generate
from abio.gen.exprgen import combine_expr, copy_expr, random_expr


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class GenTests(unittest.TestCase):
    def test_reproducible(self):
        a, _ = generate({"seed": 5, "threads": 3, "sync_points": 1, "events_per_thread": 2})
        b, _ = generate({"seed": 5, "threads": 3, "sync_points": 1, "events_per_thread": 2})
        self.assertEqual(to_string([a.to_doc()]), to_string([b.to_doc()]))

    def test_defaults_are_base(self):
        for s, _ in small_setups(10, actions_per_thread=4):
            self.assertEqual(s.features().names(), [])

    def test_synchronous_io(self):
        for s, _ in small_setups(5, max_in_flight=1, actions_per_thread=4):
            for th in s.threads:
                kinds = [st.kind == "done" for st in th.steps]
                self.assertEqual(kinds, [False, True] * 4)

    def test_writers_cap(self):
        for s, _ in small_setups(10, threads=4, blocks=2, kind_mix={"write": 1.0}, writers_per_block=1):
            for b in range(s.blocks):
                self.assertLessEqual(len({w.thread for w in s.writers(b)}), 1)

    def test_exprgen(self):
        import random
        rng = random.Random(0)
        self.assertEqual(T.refs(copy_expr(rng, ["r1"], 4)), {"r1"})
        for _ in range(50):
            e = combine_expr(rng, ["r1", "r2", "r3"], 4, 3)
            self.assertGreaterEqual(len(T.refs(e)), 2)
        self.assertIsInstance(random_expr(rng, [], {"copy": 1.0}, 4, 2), T.Const)  # falls back without reads


class CLITests(unittest.TestCase):
    def test_pipeline(self):
        with tempfile.TemporaryDirectory() as d:
            setup = os.path.join(d, "s.yaml")
            self.assertEqual(run("gen", example("base.hyperparams.yaml"), "-o", setup, "--truth", os.path.join(d, "t.yaml"))[0], 0)
            code, out, _ = run("lin", "count", setup)
            n = load_document_from(out)["linearizations"]
            lin = os.path.join(d, "l.yaml")
            self.assertEqual(run("lin", "enum", setup, "-o", lin)[0], 0)
            self.assertEqual(run("validate", "lin", setup, lin)[0], 0)
            self.assertEqual(run("lin", "enum", setup, "--count-only")[1].strip(), str(n))
            outc = os.path.join(d, "o.yaml")
            self.assertEqual(run("solve", "run", setup, "--algo", "brute", "-o", outc)[0], 0)
            self.assertEqual(run("validate", "solve", setup, outc)[0], 0)
            self.assertEqual(run("solve", "run", setup, "--algo", "brute", "--lin", lin, "--index", "3", "-o", outc)[0], 0)
            self.assertEqual(load_document(outc)["mode"], "fixed")
            self.assertEqual(run("validate", "solve", setup, outc, "--lin", lin, "--index", "3")[0], 0)

    def test_capability_refusal(self):
        code, _, err = run("lin", "count", example("formats-example.setup.yaml"))
        self.assertEqual(code, 2)
        self.assertIn("--ignore-observed", err)
        self.assertEqual(run("lin", "count", example("formats-example.setup.yaml"), "--ignore-observed")[0], 0)

    def test_plugin_spec(self):
        code, out, _ = run("lin", "count", example("base.setup.yaml"), "--algo", "abio.lin.feasible:EnumerationCounter")
        self.assertEqual(code, 0)
        self.assertEqual(load_document_from(out)["linearizations"], 924)


def load_document_from(text):
    import yaml
    return yaml.safe_load(text)


if __name__ == "__main__":
    unittest.main()
