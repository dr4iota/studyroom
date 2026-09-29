import contextlib
import io
import os
import sys
import unittest

from helpers import ROOT  # noqa: F401  (sets sys.path)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from harness.cli import main  # noqa: E402
from harness.formats import loads  # noqa: E402


def grade(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(["grade", "--no-throughput", "--no-scaling", "--mem-mb", "3000", *argv])
    return code, loads(out.getvalue(), "report")


class GradeTests(unittest.TestCase):
    def test_reference_algorithms_pass(self):
        code, rep = grade("--algo", "backtrack", "--algo", "dp-positions")
        self.assertEqual(code, 0, rep["errors"][:3])
        self.assertTrue(rep["ok"])

    def test_planted_bugs_are_caught(self):
        code, rep = grade("--plugin", "fixtures.bad_attempt")
        self.assertEqual(code, 1)
        by_algo = {}
        for e in rep["errors"]:
            by_algo.setdefault(e["where"].get("algo"), set()).add(e["code"])
        self.assertIn("MISSING", by_algo["bad-drops-last"])
        self.assertIn("EXTRA", by_algo["bad-ignores-obs"])
        self.assertIn("CRASH", by_algo["bad-crashes"])
        self.assertIn("COUNT", by_algo["bad-off-by-one"])
        self.assertTrue({"UNDER", "OVER"} & by_algo["bad-init-only"])
        self.assertIn("IMPORT-POLICY", by_algo[None])  # the forbidden import of reference code


if __name__ == "__main__":
    unittest.main()
