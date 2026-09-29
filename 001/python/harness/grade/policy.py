"""Import policy for attempts: what model-written code may use from the harness.

An attempt receives parsed objects through the API; it must not call the harness's
reference algorithms or oracles, or read files. This module checks that statically, by
parsing every ``.py`` file of the attempt package (tests are not exempt, since attempts
do not ship tests).

Allowed:
- the Python standard library, except modules that execute or reach outside
  (``subprocess``, ``socket``, network clients, ``ctypes``, ...);
- the attempt's own package;
- the harness modules in ``ALLOWED`` (data model and APIs), and the names in
  ``ALLOWED_NAMES`` from modules that also hold reference code.

Everything else from ``harness`` is a violation, as is any import of another attempt.
"""

from __future__ import annotations

import ast
import pathlib
import sys

ALLOWED = {
    "harness", "harness.model", "harness.poset", "harness.terms", "harness.capabilities",
    "harness.registry", "harness.lin", "harness.lin.api", "harness.solve", "harness.solve.api",
}
# from-imports allowed from these packages/modules: only these names
ALLOWED_NAMES = {
    "harness": {"model", "poset", "terms", "capabilities", "registry"},
    "harness.lin": {"api", "LinEnumerator", "LinCounter", "LinSampler", "CountResult"},
    "harness.solve": {"api", "Solver", "SolverCapabilities", "Outcomes"},
    "harness.semantics": {"Schedule"},
}
FORBIDDEN_STDLIB = {
    "subprocess", "socket", "ssl", "http", "urllib", "ftplib", "smtplib", "telnetlib",
    "ctypes", "multiprocessing", "webbrowser", "xmlrpc", "asyncio",
}


def _stdlib(name: str) -> bool:
    return name.split(".")[0] in sys.stdlib_module_names


def check_package(package: str, root: pathlib.Path) -> list[dict]:
    """Violations as report errors (code IMPORT-POLICY), one per offending import."""
    own = package.split(".")[0:2]  # e.g. attempts.linear_opus55_b_1
    errors = []
    for f in sorted(root.rglob("*.py")):
        if "__pycache__" in f.parts:
            continue
        try:
            tree = ast.parse(f.read_text(), str(f))
        except SyntaxError as ex:
            errors.append({"code": "SYNTAX", "where": {"file": str(f)}, "message": str(ex)})
            continue
        for node in ast.walk(tree):
            mods: list[tuple[str, list[str]]] = []
            if isinstance(node, ast.Import):
                mods = [(a.name, []) for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:  # relative import inside the attempt: fine
                    continue
                mods = [(node.module or "", [a.name for a in node.names])]
            elif isinstance(node, ast.Call) and getattr(node.func, "id", None) in ("__import__", "exec", "eval", "open"):
                errors.append({"code": "IMPORT-POLICY", "where": {"file": str(f), "line": node.lineno},
                               "message": f"call to {node.func.id}() is not allowed"})
                continue
            for mod, names in mods:
                msg = _judge(mod, names, own)
                if msg:
                    errors.append({"code": "IMPORT-POLICY", "where": {"file": str(f), "line": node.lineno}, "message": msg})
    return errors


def _judge(mod: str, names: list[str], own: list[str]) -> str | None:
    top = mod.split(".")[0]
    if mod.split(".")[:2] == own:
        return None
    if top == "attempts":
        return f"imports another attempt: {mod}"
    if top == "harness":
        if mod in ALLOWED_NAMES:
            bad = [n for n in names if n not in ALLOWED_NAMES[mod]] if names else ["(whole module)"]
            if mod in ALLOWED and not names:
                return None
            return f"from {mod} import {', '.join(bad)} is not allowed" if bad else None
        if mod in ALLOWED:
            return None
        return f"harness module {mod} is not allowed (reference code or I/O)"
    if top in FORBIDDEN_STDLIB:
        return f"module {mod} is not allowed"
    if not _stdlib(mod):
        return f"third-party module {mod} is not allowed"
    return None
