"""Tasks for attempts, machine-readable; the prose is in ``python/tasks/<bundle>/<kind>_<case>.md``.

An attempt package is ``attempts.<kind>_<case>_<model><version>_<trial>``. The grader
derives the task from that name and checks that the attempt delivers what the task asks
(error code TASK):

- ``linear``: exactly one ``lin-enum``, at most one ``lin-count``, nothing else;
- ``solver``: exactly one ``solver``, with ``"all"`` among its modes;
- every algorithm declares exactly the case's capabilities (``rcw`` False);
- every name starts with ``<model><version>_<trial>-<case>-``;
- the directory has an ``__init__.py`` and a ``SOURCES.md``.
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass

NAME_RE = re.compile(r"^attempts\.(linear|solver)_(b|s|o|so)_([a-z]+[0-9]+)_([0-9]+)$")
CASE_CAPS = {"b": (False, False), "s": (True, False), "o": (False, True), "so": (True, True)}
ALLOWED_CATS = {"linear": {"lin-enum": (1, 1), "lin-count": (0, 1)}, "solver": {"solver": (1, 1)}}


@dataclass(frozen=True)
class Task:
    kind: str
    case: str
    model: str
    trial: str

    @property
    def prefix(self) -> str:
        return f"{self.model}_{self.trial}-{self.case}-"

    @property
    def name(self) -> str:
        return f"{self.kind}_{self.case}"


def parse(module: str) -> Task | None:
    m = NAME_RE.match(module)
    return Task(*m.groups()) if m else None


def conformance(task: Task, root: pathlib.Path, algos: list[tuple[str, str, type]]) -> list[dict]:
    """``algos``: (category, name, class) registered by the attempt."""
    errs = []

    def e(msg: str, **where) -> None:
        errs.append({"code": "TASK", "where": {"task": f"{task.kind}_{task.case}", **where}, "message": msg})

    for f in ("__init__.py", "SOURCES.md", "PROMPT.md", "attempt.yaml"):
        if not (root / f).is_file():
            e(f"missing {f}")
    want = ALLOWED_CATS[task.kind]
    counts = {c: 0 for c in want}
    sync, obs = CASE_CAPS[task.case]
    for cat, name, cls in algos:
        if cat not in want:
            e(f"registers a {cat}, which task {task.kind} does not ask for", algo=name)
            continue
        counts[cat] += 1
        if not name.startswith(task.prefix):
            e(f"name must start with {task.prefix!r}", algo=name)
        caps = cls.capabilities
        if (caps.rcw, caps.sync, caps.observed_reads) != (False, sync, obs):
            e(f"capabilities rcw={caps.rcw} sync={caps.sync} observed_reads={caps.observed_reads}; "
              f"task wants rcw=False sync={sync} observed_reads={obs}", algo=name)
        if cat == "solver" and "all" not in getattr(caps, "modes", ()):
            e("solver modes must include 'all'", algo=name)
    for cat, (lo, hi) in want.items():
        if not lo <= counts[cat] <= hi:
            e(f"registers {counts[cat]} {cat}, task wants {lo}..{hi}")
    return errs
