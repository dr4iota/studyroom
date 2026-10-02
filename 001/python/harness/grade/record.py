"""Audit, grade and record one attempt (orchestrator only).

    python -m harness.grade.record attempts.<dir> --transcript AGENT.jsonl [--budget small]

1. Audits the transcript against the protocol (``transcript.py``) → ``audit.yaml``.
2. Grades the attempt in a separate process (``harness grade``) → ``grade.yaml``.
3. Fills ``transcript``, ``audit`` and ``grade`` in ``attempt.yaml``.

An attempt that fails the audit is still graded, for information, but is marked
``discarded: true``.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
import sys
from collections import Counter

import yaml

from .transcript import MINOR, audit

PYROOT = pathlib.Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="harness.grade.record")
    p.add_argument("module")
    p.add_argument("--transcript", required=True)
    p.add_argument("--budget", default="small", choices=["small", "full"])
    p.add_argument("--audit-only", action="store_true", help="re-audit; keep the existing grade")
    a = p.parse_args(argv)
    own = PYROOT / pathlib.Path(*a.module.split("."))
    meta_path = own / "attempt.yaml"
    meta = yaml.safe_load(meta_path.read_text())

    errs, stats = audit(a.transcript, a.module)
    (own / "audit.yaml").write_text(yaml.safe_dump(
        {"ok": not [e for e in errs if e["code"] not in MINOR], "errors": errs, **stats}, sort_keys=False))

    if a.audit_only:
        major = [e for e in errs if e["code"] not in MINOR]
        meta["audit"] = {"ok": not major, "errors": dict(Counter(e["code"] for e in errs)), "tools": stats["tools"]}
        meta["discarded"] = bool(major)
        meta_path.write_text(yaml.safe_dump(meta, sort_keys=False))
        print(yaml.safe_dump({"audit": meta["audit"], "discarded": meta["discarded"]}, sort_keys=False), end="")
        return 0
    (own / "grade.yaml").unlink(missing_ok=True)  # never read a stale report
    r = subprocess.run([sys.executable, "-m", "harness", "grade", "--plugin", a.module, "--budget", a.budget,
                        "-o", str(own / "grade.yaml")], cwd=PYROOT, capture_output=True, text=True)
    try:
        grade = yaml.safe_load((own / "grade.yaml").read_text())
    except (OSError, yaml.YAMLError):
        grade = {"ok": False, "errors": [{"code": "GRADER", "message": (r.stderr or r.stdout)[-500:]}], "stats": {}}
        (own / "grade.yaml").write_text(yaml.safe_dump(grade, sort_keys=False))
    codes = Counter(e["code"] for e in grade.get("errors") or [])
    per_algo = {n: {"cases": s.get("cases"), "passed": s.get("instances", 0) - s.get("failed", 0),
                    "instances": s.get("instances"), "throughput": s.get("throughput")}
                for n, s in (grade.get("stats") or {}).items()}

    meta["transcript"] = {"file": pathlib.Path(a.transcript).name,
                          "sha256": hashlib.sha256(pathlib.Path(a.transcript).read_bytes()).hexdigest()}
    major = [e for e in errs if e["code"] not in MINOR]
    meta["audit"] = {"ok": not major, "errors": dict(Counter(e["code"] for e in errs)), "tools": stats["tools"]}
    grader = subprocess.run(["git", "rev-parse", "HEAD"], cwd=PYROOT, capture_output=True, text=True).stdout.strip()
    for n, st in (grade.get("stats") or {}).items():
        if "scaling" in st:
            per_algo.setdefault(n, {})["scale"] = {c: v.get("max_shape", v.get("max_n")) for c, v in st["scaling"].items()}
    meta["grade"] = {"ok": bool(grade.get("ok")), "budget": a.budget, "grader_commit": grader,
                     "errors": dict(codes), "algorithms": per_algo}
    meta["discarded"] = bool(major)
    meta_path.write_text(yaml.safe_dump(meta, sort_keys=False))
    print(yaml.safe_dump({"audit": meta["audit"], "grade": meta["grade"], "discarded": meta["discarded"]},
                         sort_keys=False), end="")
    print(r.stderr.strip(), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
