"""Readers and writers for the on-disk documents of formats.md (v2).

YAML is the default syntax; JSON is accepted everywhere. Streams (linearizations,
schedules) are YAML documents separated by ``---``, or JSON Lines. The path ``-`` means
stdin/stdout. No other module parses or prints documents by hand.
"""

from __future__ import annotations

import io
import json
import sys
from typing import Any, Iterable, TextIO

import yaml

from . import terms as T
from .model import FORMAT_VERSION, Setup
from .poset import Linearization
from .semantics import Schedule, check_effects, observed_value_doc


class FormatError(ValueError):
    pass


# --------------------------------------------------------------------------- raw documents


def _read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def loads_all(text: str, json_syntax: bool | None = None) -> list[dict]:
    """All documents in a string (YAML stream, JSON document or JSON Lines)."""
    if json_syntax is None:
        json_syntax = text.lstrip().startswith(("{", "["))
    if json_syntax:
        try:
            return [json.loads(text)]
        except json.JSONDecodeError:
            return [json.loads(line) for line in text.splitlines() if line.strip()]
    return [d for d in yaml.safe_load_all(text) if d is not None]


def loads(text: str, fmt: str | None = None) -> dict:
    """Exactly one document from a string (e.g. captured CLI output); checks ``fmt``."""
    docs = loads_all(text)
    if len(docs) != 1:
        raise FormatError(f"expected one document, found {len(docs)}")
    if fmt is not None:
        expect(docs[0], fmt)
    return docs[0]


def load_documents(path: str) -> list[dict]:
    """All documents in a file (one for plain documents, many for streams)."""
    return loads_all(_read_text(path), True if path.endswith((".json", ".jsonl")) else None)


def load_document(path: str, fmt: str | None = None) -> dict:
    docs = load_documents(path)
    if len(docs) != 1:
        raise FormatError(f"{path}: expected one document, found {len(docs)}")
    if fmt is not None:
        expect(docs[0], fmt)
    return docs[0]


def expect(doc: Any, fmt: str) -> None:
    if not isinstance(doc, dict) or doc.get("format") != fmt:
        raise FormatError(f"expected a '{fmt}' document, got {doc.get('format') if isinstance(doc, dict) else type(doc).__name__}")
    if doc.get("version") != FORMAT_VERSION:
        raise FormatError(f"unsupported {fmt} version {doc.get('version')!r}")


def dumps(doc: dict, syntax: str = "yaml") -> str:
    if syntax == "json":
        return json.dumps(doc, separators=(", ", ": "))
    return yaml.safe_dump(doc, sort_keys=False, default_flow_style=None, width=100, allow_unicode=True)


class Output:
    """A document sink (file path or ``-``) that writes single documents or streams."""

    def __init__(self, path: str = "-", syntax: str | None = None, fh: TextIO | None = None) -> None:
        self.path = path
        self.syntax = syntax or ("json" if path.endswith((".json", ".jsonl")) else "yaml")
        self.count = 0
        self.owned = fh is None and path != "-"
        self.fh: TextIO = fh or (open(path, "w", encoding="utf-8") if self.owned else sys.stdout)

    def write(self, doc: dict) -> None:
        if self.syntax == "json":
            self.fh.write(dumps(doc, "json") + "\n")
        else:
            if self.count:
                self.fh.write("---\n")
            self.fh.write(dumps(doc))
        self.count += 1

    def close(self) -> None:
        if self.owned:
            self.fh.close()
        else:
            self.fh.flush()

    def __enter__(self) -> "Output":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


def write_document(doc: dict, path: str = "-", syntax: str | None = None) -> None:
    with Output(path, syntax) as out:
        out.write(doc)


def to_string(docs: Iterable[dict], syntax: str = "yaml") -> str:
    buf = io.StringIO()
    out = Output("", syntax, fh=buf)
    for d in docs:
        out.write(d)
    return buf.getvalue()


def _head(fmt: str, setup_id: str, meta: dict | None = None) -> dict:
    d: dict[str, Any] = {"format": fmt, "version": FORMAT_VERSION, "setup_id": setup_id}
    if meta:
        d["meta"] = meta
    return d


def _check_binding(setup: Setup, doc: dict) -> None:
    if doc.get("setup_id") != setup.id:
        raise FormatError(f"setup_id {doc.get('setup_id')!r} does not match setup {setup.id!r}")


# --------------------------------------------------------------------------- setup


def load_setup(path: str) -> Setup:
    return Setup.from_doc(load_document(path, "setup"))


# --------------------------------------------------------------------------- linearization


def linearization_doc(setup: Setup, order: Linearization, meta: dict | None = None) -> dict:
    d = _head("linearization", setup.id, meta)
    d["order"] = setup.poset.to_names(order)
    return d


def parse_linearization(setup: Setup, doc: dict) -> Linearization:
    """Validate (VAL-LIN) and convert a linearization document."""
    expect(doc, "linearization")
    _check_binding(setup, doc)
    errs = setup.poset.check(doc.get("order") or [])
    if errs:
        raise FormatError("invalid linearization: " + "; ".join(f"{c} {s}: {m}" for c, s, m in errs[:5]))
    return setup.poset.from_names(doc["order"])


# --------------------------------------------------------------------------- schedule


def schedule_doc(setup: Setup, s: Schedule) -> dict:
    d = _head("schedule", setup.id, s.meta)
    d["order"] = setup.poset.to_names(s.order)
    d["effects"] = list(s.effects)
    d["results"] = [{"id": a.id, "value": T.to_value(s.results[a.id])} for a in setup.returning() if a.id in s.results]
    d["final"] = [{"block": b, "value": T.to_value(v)} for b, v in enumerate(s.final)]
    d["consistent"] = s.consistent
    return d


def parse_schedule(setup: Setup, doc: dict) -> Schedule:
    """Parse a schedule; recorded results are *not* trusted (validators recompute them)."""
    expect(doc, "schedule")
    order = parse_linearization(setup, {**doc, "format": "linearization"})
    effects = tuple(doc.get("effects") or [])
    errs = check_effects(setup, order, effects)
    if errs:
        raise FormatError("; ".join(errs))
    results = {r["id"]: T.parse_term(r["value"]) for r in doc.get("results") or []}
    final = [T.parse_term(f["value"]) for f in sorted(doc.get("final") or [], key=lambda f: f["block"])]
    return Schedule(order, effects, results, final, bool(doc.get("consistent")), dict(doc.get("meta") or {}))


# --------------------------------------------------------------------------- outcomes


def outcomes_doc(setup: Setup, o: Any, *, linearization: Any = None, witnesses: str | None = None) -> dict:
    """``o`` is an :class:`abio.solve.api.Outcomes`."""
    d = _head("outcomes", setup.id, o.meta)
    d["mode"] = o.mode
    d["linearization"] = linearization
    d["consistent"] = o.consistent
    if o.consistent:
        d["results"] = [{"id": a.id, "values": [T.to_value(v) for v in T.sorted_terms(o.results.get(a.id, ()))]}
                        for a in setup.returning()]
        d["final"] = [{"block": b, "values": [T.to_value(v) for v in T.sorted_terms(o.final.get(b, ()))]}
                      for b in range(setup.blocks)]
    if witnesses:
        d["witnesses"] = witnesses
    return d


def parse_outcomes(setup: Setup, doc: dict) -> tuple[bool, dict[str, set[T.Term]], dict[int, set[T.Term]]]:
    expect(doc, "outcomes")
    _check_binding(setup, doc)
    res = {r["id"]: {T.parse_term(v) for v in r["values"]} for r in doc.get("results") or []}
    fin = {f["block"]: {T.parse_term(v) for v in f["values"]} for f in doc.get("final") or []}
    return bool(doc.get("consistent")), res, fin


# --------------------------------------------------------------------------- count, report


def count_doc(setup: Setup, c: Any, meta: dict | None = None) -> dict:
    """``c`` is an :class:`abio.lin.api.CountResult`."""
    d = _head("count", setup.id, meta)
    d.update(linearizations=c.linearizations, feasible=c.feasible, method=c.method, error=c.error)
    return d


def report_doc(setup_id: str, subject: str, errors: list[dict], stats: dict | None = None) -> dict:
    d = _head("report", setup_id)
    d.update(subject=subject, ok=not errors, errors=errors, stats=stats or {})
    return d


__all__ = [
    "FormatError", "Output", "count_doc", "dumps", "expect", "linearization_doc", "load_document",
    "load_documents", "load_setup", "loads", "loads_all", "observed_value_doc", "outcomes_doc", "parse_linearization",
    "parse_outcomes", "parse_schedule", "report_doc", "schedule_doc", "to_string", "write_document",
]
