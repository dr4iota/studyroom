"""Prepare an attempt directory (orchestrator only).

    python -m harness.grade.prepare --task linear_so --model opus55 --model-id claude-opus-5-5 \\
        [--trial 1] [--bundle v1] [--enforcement transcript-audit]

Creates ``attempts/<kind>_<case>_<model>_<trial>/`` with:

- ``PROMPT.md``: the exact prompt, rendered from the bundle's template;
- ``attempt.yaml``: task, model, trial, bundle and spec versions, harness commit, date and
  conditions. The audit and grade results are added later.

It prints the prompt to stdout. It refuses to reuse a directory that already exists, and
refuses to run if the harness working tree has uncommitted changes, since the commit
recorded must be the code the attempt was given.
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import subprocess
import sys

import yaml

STUDY = pathlib.Path(__file__).resolve().parents[3]
REPO = STUDY.parent


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="harness.grade.prepare")
    p.add_argument("--task", required=True, help="e.g. linear_so")
    p.add_argument("--model", required=True, help="short tag with version, e.g. opus55")
    p.add_argument("--model-id", required=True, help="full model id, e.g. claude-opus-5-5")
    p.add_argument("--trial", default="1")
    p.add_argument("--bundle", default="v1")
    p.add_argument("--enforcement", default="transcript-audit", choices=["transcript-audit", "restricted-agent"])
    a = p.parse_args(argv)

    bdir = STUDY / "python" / "tasks" / a.bundle
    bundle = yaml.safe_load((bdir / "bundle.yaml").read_text())
    if a.task not in bundle["tasks"]:
        p.error(f"task {a.task} not in bundle {a.bundle}")
    dirty = _git("status", "--porcelain", "--", str(STUDY / "spec"), str(STUDY / "python" / "harness"), str(bdir))
    if dirty:
        p.error("spec, harness or bundle has uncommitted changes; commit first:\n" + dirty)
    kind, case = a.task.split("_", 1)
    name = f"{a.task}_{a.model}_{a.trial}"
    out = STUDY / "python" / "attempts" / name
    if out.exists():
        p.error(f"{out} exists; use a new trial number")
    prefix = f"{a.model}_{a.trial}-{case}-"
    prompt = (STUDY / bundle["prompt"]).read_text()
    prompt = prompt.format(kind=kind, case=case, dir=name, prefix=prefix, root=str(REPO))
    out.mkdir(parents=True)
    (out / "PROMPT.md").write_text(prompt)
    meta = {
        "format": "attempt", "version": 1, "task": a.task, "kind": kind, "case": case,
        "model": a.model, "model_id": a.model_id, "trial": int(a.trial), "prefix": prefix,
        "bundle": a.bundle, "spec": bundle["spec"], "harness_commit": _git("rev-parse", "HEAD"),
        "prepared": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "conditions": dict(bundle["conditions"], enforcement=a.enforcement),
        "transcript": None, "audit": None, "grade": None,
    }
    (out / "attempt.yaml").write_text(yaml.safe_dump(meta, sort_keys=False))
    sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
