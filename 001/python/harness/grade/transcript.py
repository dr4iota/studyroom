"""Audit an attempting agent's transcript (Claude Code subagent JSONL) against the protocol.

    python -m harness.grade.transcript TRANSCRIPT.jsonl attempts.<dir>

Checks, as report errors:

TOOL        a tool other than the file tools was used (shell, web, agents, ...)
TOOL-MINOR  a shell call that only inspected the attempt's own directory, read-only
            (``ls``, ``cat``, ``head``, ``tail``, ``wc``, ``stat``, ``file``, ``pwd``, ``find``
            without actions); it leaks nothing about the problem, so it is recorded but
            does not discard the attempt
READ    a file outside the task's allowed list was read
SEARCH  Grep/Glob searched outside the allowed files and the attempt directory
WRITE   a file outside the attempt directory was written or edited

Any TOOL, READ, SEARCH or WRITE error means the attempt did not follow the protocol and is
discarded. TOOL-MINOR is recorded but does not discard. Paths are resolved against the study root (``001/``).
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

from .tasks import parse

FILE_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep"}
NEUTRAL_TOOLS = {"SubagentHandback", "TodoWrite"}  # bookkeeping, no access to files or the world
STUDY = pathlib.Path(__file__).resolve().parents[3]  # .../001


def bundle_reads(bundle: str, kind: str, task: str) -> list[str]:
    """Allowed reads for a task, from ``python/tasks/<bundle>/bundle.yaml``."""
    import yaml
    b = yaml.safe_load((STUDY / "python" / "tasks" / bundle / "bundle.yaml").read_text())
    return [f.format(task=task) for f in b["reads"]["all"] + b["reads"][kind]]


INSPECT = {"ls", "cat", "head", "tail", "wc", "stat", "file", "pwd", "find"}
MINOR = {"TOOL-MINOR"}


def minor_shell(command: str, own: pathlib.Path) -> bool:
    """Is ``command`` read-only inspection of paths inside ``own`` only?"""
    import re
    import shlex
    if re.search(r"[`$<>]|\\", command):  # substitutions, redirections, escapes: not simple
        return False
    for part in re.split(r"&&|\|\||;|\|", command):
        try:
            words = shlex.split(part)
        except ValueError:
            return False
        if not words:
            continue
        if words[0] not in INSPECT:
            return False
        if words[0] == "find" and any(w in ("-exec", "-execdir", "-delete", "-ok", "-fprint") for w in words):
            return False
        for w in words[1:]:
            if w.startswith("-"):
                continue
            q = pathlib.Path(w)
            q = (q if q.is_absolute() else own / q).resolve()
            if not (q == own or own in q.parents):
                return False
        if words[0] == "pwd":
            continue
        if len([w for w in words[1:] if not w.startswith("-")]) == 0 and words[0] != "pwd":
            return False  # no explicit path: would act on an unknown working directory
    return True


def tool_calls(path: str):
    for line in open(path, encoding="utf-8"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = d.get("message")
        content = msg.get("content") if isinstance(msg, dict) else None
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    yield c.get("name"), c.get("input") or {}


def _resolve(p: str | None) -> pathlib.Path | None:
    if not p:
        return None
    q = pathlib.Path(p)
    return (q if q.is_absolute() else STUDY / q).resolve()


def audit(transcript: str, module: str) -> tuple[list[dict], dict]:
    task = parse(module)
    if task is None:
        raise ValueError(f"not an attempt module name: {module}")
    own = (STUDY / "python" / pathlib.Path(*module.split("."))).resolve()
    meta = own / "attempt.yaml"
    import yaml
    bundle = yaml.safe_load(meta.read_text())["bundle"] if meta.is_file() else "v1"
    allowed = {(STUDY / f).resolve() for f in bundle_reads(bundle, task.kind, f"{task.kind}_{task.case}")}
    protected = {own / "attempt.yaml", own / "PROMPT.md"}

    def inside(p: pathlib.Path) -> bool:
        return p == own or own in p.parents

    errs, tools = [], Counter()
    for name, inp in tool_calls(transcript):
        tools[name] += 1
        if name in NEUTRAL_TOOLS:
            continue
        if name == "ToolSearch":  # loading deferred tools: neutral only if it loads file tools
            q = str(inp.get("query", ""))
            wanted = {t.strip() for t in q[len("select:"):].split(",")} if q.startswith("select:") else None
            if wanted and wanted <= FILE_TOOLS:
                continue
        if name not in FILE_TOOLS:
            detail = inp.get("command") or inp.get("query") or inp.get("url") or ""
            code = "TOOL-MINOR" if name == "Bash" and minor_shell(str(detail), own) else "TOOL"
            errs.append({"code": code, "where": {"tool": name}, "message": str(detail)[:200]})
            continue
        p = _resolve(inp.get("file_path") or inp.get("path"))
        if name == "Read":
            if p is None or not (p in allowed or inside(p)):
                errs.append({"code": "READ", "where": {"file": str(p)}, "message": "not on the allowed list"})
        elif name in ("Write", "Edit"):
            if p is None or not inside(p) or p in protected:
                errs.append({"code": "WRITE", "where": {"file": str(p)},
                             "message": "outside the attempt directory, or an orchestrator file"})
        else:  # Glob / Grep
            base = p or STUDY  # no path: searches the working directory
            if not (base in allowed or inside(base)):
                errs.append({"code": "SEARCH", "where": {"tool": name, "path": str(base)},
                             "message": f"pattern {str(inp.get('pattern'))[:80]!r} outside allowed files"})
    return errs, {"tools": dict(tools)}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    errs, stats = audit(*argv)
    print(json.dumps({"ok": not errs, "errors": errs, "stats": stats}, indent=1))
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
