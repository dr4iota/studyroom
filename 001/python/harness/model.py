"""The setup: threads, their steps, and the derived action table (formats.md §1).

``Setup.from_doc`` parses and validates a ``setup`` document; ``Setup.to_doc`` writes
one back. Construction always validates (rules 1-5 of formats.md §1), so an existing
``Setup`` object is well-formed. Unknown document keys are kept in ``extra`` and written
back unchanged.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any

from . import terms as T
from .capabilities import Features

if TYPE_CHECKING:
    from .poset import TracePoset

ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
ACTION_KINDS = ("read", "write", "rcw")
EVENT_KINDS = ("before", "after", "at")
KIND_KEYS = ACTION_KINDS + ("done",) + EVENT_KINDS
REL_RANK = {"before": 0, "at": 1, "after": 2}  # required program order of events on one sync point
FORMAT_VERSION = 2


class MalformedSetup(ValueError):
    pass


@dataclass
class Step:
    """One program step.

    kind    one of ``read write rcw done before after at``
    target  the block (``read``/``write``/``rcw``), the action id (``done``), or the sync
            point (events)
    id      action id for start steps; optional id for events; None for ``done``
    data    start of write/rcw: ``Expr``, or None for ``"*"`` (unknown content);
            ``done`` of read/rcw: the observed result (a ``Term``, or ``"ok"``/``"fail"``
            under ``rcw_result: flag``), or None when unobserved
    expect  start of rcw: ``Expr``
    """

    kind: str
    target: int | str
    id: str | None = None
    data: Any = None
    expect: T.Expr | None = None
    extra: dict = field(default_factory=dict)

    @property
    def is_start(self) -> bool:
        return self.kind in ACTION_KINDS

    @property
    def is_event(self) -> bool:
        return self.kind in EVENT_KINDS

    @staticmethod
    def from_doc(d: dict, where: str) -> "Step":
        if not isinstance(d, dict):
            raise MalformedSetup(f"{where}: a step must be a map")
        kinds = [k for k in KIND_KEYS if k in d]
        if len(kinds) != 1:
            raise MalformedSetup(f"{where}: a step needs exactly one of {KIND_KEYS}, got {kinds}")
        kind = kinds[0]
        known = {kind, "id", "data", "expect"}
        extra = {k: v for k, v in d.items() if k not in known}
        target = d[kind]
        sid = d.get("id")
        try:
            if kind in ACTION_KINDS:
                if "data" not in d and kind != "read":
                    raise MalformedSetup(f"{where}: {kind} needs 'data'")
                if kind == "read" and ("data" in d or "expect" in d):
                    raise MalformedSetup(f"{where}: a read start takes no data (put it on 'done')")
                data = None if kind == "read" or d["data"] == "*" else T.parse_expr(d["data"])
                expect = None
                if kind == "rcw":
                    if "expect" not in d or d["expect"] == "*":
                        raise MalformedSetup(f"{where}: rcw needs a known 'expect'")
                    expect = T.parse_expr(d["expect"])
                elif "expect" in d:
                    raise MalformedSetup(f"{where}: only rcw takes 'expect'")
                return Step(kind, target, sid, data, expect, extra)
            if kind == "done":
                v = d.get("data")
                if v is None or v == "?":
                    obs = None
                elif v in ("ok", "fail"):
                    obs = v
                else:
                    obs = T.parse_term(v)
                return Step(kind, target, None, obs, None, extra)
            return Step(kind, target, sid, None, None, extra)
        except T.TermSyntaxError as ex:
            raise MalformedSetup(f"{where}: {ex}") from None

    def to_doc(self) -> dict:
        d: dict[str, Any] = {self.kind: self.target}
        if self.kind in ACTION_KINDS:
            d["id"] = self.id
            if self.kind == "rcw":
                d["expect"] = T.to_value(self.expect)
            if self.kind != "read":
                d["data"] = "*" if self.data is None else T.to_value(self.data)
        elif self.kind == "done":
            if self.data is not None:
                d["data"] = self.data if isinstance(self.data, str) else T.to_value(self.data)
        elif self.id is not None:
            d["id"] = self.id
        d.update(self.extra)
        return d


@dataclass
class Thread:
    id: str
    steps: list[Step]
    extra: dict = field(default_factory=dict)


@dataclass
class Semantics:
    register: str = "atomic"  # atomic | regular | safe (only atomic is implemented)
    rcw_result: str = "old"  # old | flag
    distinct_effects: bool = True

    def is_default(self) -> bool:
        return self.register == "atomic" and self.distinct_effects


@dataclass
class Action:
    """Derived view of one action (read, write or rcw); built by ``Setup``."""

    id: str
    kind: str  # read | write | rcw
    block: int
    thread: int  # thread index
    start: int  # step index of the start step in the thread
    done: int  # step index of the done step
    data: T.Expr | None  # write/rcw: expression, None = "*"; read: None
    expect: T.Expr | None  # rcw only
    observed: Any  # done data: Term, "ok"/"fail", or None

    @property
    def writes(self) -> bool:
        """True for actions that can change the block (write, rcw)."""
        return self.kind != "read"

    @property
    def returns(self) -> bool:
        """True for actions that have a result (read, rcw)."""
        return self.kind != "write"


@dataclass
class Setup:
    id: str
    blocks: int
    sync_points: int
    init: list[T.Term]
    threads: list[Thread]
    semantics: Semantics = field(default_factory=Semantics)
    meta: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate()

    # ------------------------------------------------------------------ derived data

    @cached_property
    def poset(self) -> "TracePoset":
        from .poset import TracePoset

        return TracePoset(self)

    @property
    def n_threads(self) -> int:
        return len(self.threads)

    def returning(self) -> list[Action]:
        """Reads and RCWs, in action order: the ids that get a ``Poss`` set."""
        return [a for a in self.actions.values() if a.returns]

    def writers(self, block: int | None = None) -> list[Action]:
        return [a for a in self.actions.values() if a.writes and (block is None or a.block == block)]

    def step_name(self, t: int, i: int) -> str | None:
        """Global name of step ``i`` of thread ``t`` (formats.md §1.1); None for ``at``."""
        s = self.threads[t].steps[i]
        if s.is_start:
            return s.id
        if s.kind == "done":
            return f"{s.target}.done"
        if s.kind == "at":
            return None
        return s.id if s.id is not None else f"{self.threads[t].id}.{s.kind}.{s.target}"

    def depends_on_reads(self, aid: str) -> bool:
        """Does the content (or expect) of write/rcw ``aid`` depend, transitively, on a read?"""
        a = self.actions[aid]
        todo = [e for e in (a.data, a.expect) if e is not None]
        seen: set[str] = set()
        while todo:
            for r in T.refs(todo.pop()):
                if r in seen:
                    continue
                seen.add(r)
                b = self.actions[r]
                if b.kind == "read":
                    return True
                if b.data is not None:
                    todo.append(b.data)
        return False

    def static_content(self, aid: str) -> T.Term:
        """Content written by write/rcw ``aid`` when it does not depend on any read."""
        a = self.actions[aid]
        if a.data is None:
            return T.Unk(aid)
        return T.substitute(a.data, self.static_content)

    def has_data_from_reads(self) -> bool:
        """Descriptive only (part of the base problem): does some write depend on a read?"""
        return any(a.writes and self.depends_on_reads(a.id) for a in self.actions.values())

    def features(self) -> Features:
        acts = self.actions.values()
        return Features(
            rcw=any(a.kind == "rcw" for a in acts),
            sync=self.sync_points > 0,
            observed_reads=any(a.observed is not None for a in acts),
        )

    def without_observations(self) -> "Setup":
        doc = self.to_doc()
        for th in doc["threads"]:
            for s in th["steps"]:
                if "done" in s:
                    s.pop("data", None)
        return Setup.from_doc(doc)

    # ------------------------------------------------------------------ documents

    @staticmethod
    def from_doc(doc: dict) -> "Setup":
        if not isinstance(doc, dict) or doc.get("format") != "setup":
            raise MalformedSetup("not a setup document")
        if doc.get("version") != FORMAT_VERSION:
            raise MalformedSetup(f"unsupported setup version {doc.get('version')!r}")
        known = {"format", "version", "id", "meta", "blocks", "sync_points", "init", "semantics", "threads"}
        try:
            blocks = int(doc["blocks"])
            init_doc = doc.get("init", ["*"] * blocks)
            init = [T.Init(b) if v == "*" else T.parse_term(v) for b, v in enumerate(init_doc)]
        except (KeyError, T.TermSyntaxError) as ex:
            raise MalformedSetup(f"setup: {ex}") from None
        sem_doc = dict(doc.get("semantics") or {})
        sem = Semantics(
            register=sem_doc.pop("register", "atomic"),
            rcw_result=sem_doc.pop("rcw_result", "old"),
            distinct_effects=sem_doc.pop("distinct_effects", True),
        )
        threads = []
        for ti, td in enumerate(doc.get("threads") or []):
            steps = [Step.from_doc(sd, f"thread {td.get('id', ti)} step {si}") for si, sd in enumerate(td.get("steps") or [])]
            threads.append(Thread(td.get("id"), steps, {k: v for k, v in td.items() if k not in ("id", "steps")}))
        return Setup(
            id=str(doc.get("id", "")),
            blocks=blocks,
            sync_points=int(doc.get("sync_points", 0)),
            init=init,
            threads=threads,
            semantics=sem,
            meta=dict(doc.get("meta") or {}),
            extra={k: v for k, v in doc.items() if k not in known},
        )

    def to_doc(self) -> dict:
        d: dict[str, Any] = {"format": "setup", "version": FORMAT_VERSION, "id": self.id}
        if self.meta:
            d["meta"] = copy.deepcopy(self.meta)
        d["blocks"] = self.blocks
        d["sync_points"] = self.sync_points
        d["init"] = ["*" if t == T.Init(b) else T.to_value(t) for b, t in enumerate(self.init)]
        if self.semantics != Semantics():
            d["semantics"] = {
                "register": self.semantics.register,
                "rcw_result": self.semantics.rcw_result,
                "distinct_effects": self.semantics.distinct_effects,
            }
        d["threads"] = [{"id": th.id, **th.extra, "steps": [s.to_doc() for s in th.steps]} for th in self.threads]
        d.update(copy.deepcopy(self.extra))
        return d

    # ------------------------------------------------------------------ validation

    def _validate(self) -> None:
        def bad(msg: str) -> None:
            raise MalformedSetup(msg)

        if self.blocks < 0 or self.sync_points < 0:
            bad("blocks and sync_points must be >= 0")
        if len(self.init) != self.blocks:
            bad(f"init has {len(self.init)} entries, expected {self.blocks}")
        for t in self.init:
            if T.refs(t) or any(isinstance(x, T.Unk) for x in _leaves(t)):
                bad(f"init term {t} may only use constants and init.k")
        if self.semantics.rcw_result not in ("old", "flag"):
            bad(f"unknown rcw_result {self.semantics.rcw_result!r}")

        names: set[str] = set()
        thread_ids: set[str] = set()
        actions: dict[str, Action] = {}
        for ti, th in enumerate(self.threads):
            if not isinstance(th.id, str) or not ID_RE.match(th.id):
                bad(f"thread {ti}: bad id {th.id!r}")
            if th.id in thread_ids:
                bad(f"duplicate thread id {th.id}")
            thread_ids.add(th.id)
            rels: dict[int, list[str]] = {}
            for si, s in enumerate(th.steps):
                where = f"thread {th.id} step {si}"
                if s.is_start or (s.is_event and s.id is not None):
                    if not isinstance(s.id, str) or not ID_RE.match(s.id):
                        bad(f"{where}: bad or missing id {s.id!r}")
                    if s.id in names:
                        bad(f"{where}: duplicate id {s.id}")
                    names.add(s.id)
                if s.is_start:
                    if not _is_int(s.target) or not 0 <= s.target < self.blocks:
                        bad(f"{where}: block {s.target!r} out of range 0..{self.blocks - 1}")
                    actions[s.id] = Action(s.id, s.kind, s.target, ti, si, -1, s.data, s.expect, None)
                elif s.kind == "done":
                    a = actions.get(s.target) if isinstance(s.target, str) else None
                    if a is None or a.thread != ti:
                        bad(f"{where}: done of unknown action {s.target!r} (must be started earlier in this thread)")
                    if a.done != -1:
                        bad(f"{where}: second done for {a.id}")
                    a.done = si
                    if s.data is not None:
                        if a.kind == "write":
                            bad(f"{where}: done of a write carries no data")
                        if isinstance(s.data, str) and (a.kind != "rcw" or self.semantics.rcw_result != "flag"):
                            bad(f"{where}: 'ok'/'fail' only for rcw under rcw_result: flag")
                        if not isinstance(s.data, str) and a.kind == "rcw" and self.semantics.rcw_result == "flag":
                            bad(f"{where}: rcw result must be 'ok' or 'fail' under rcw_result: flag")
                        a.observed = s.data
                else:  # event
                    if not _is_int(s.target) or not 0 <= s.target < self.sync_points:
                        bad(f"{where}: sync point {s.target!r} out of range 0..{self.sync_points - 1}")
                    seen = rels.setdefault(s.target, [])
                    if s.kind in seen:
                        bad(f"{where}: second '{s.kind}: {s.target}' in thread {th.id}")
                    if seen and REL_RANK[seen[-1]] > REL_RANK[s.kind]:
                        bad(f"{where}: '{s.kind}: {s.target}' after '{seen[-1]}: {s.target}' is a cycle")
                    seen.append(s.kind)
        for a in actions.values():
            if a.done == -1:
                bad(f"action {a.id} has no done step")
        self.actions = actions

        # expression references (formats.md §2.2)
        for a in actions.values():
            for e in (a.data, a.expect):
                if e is None:
                    continue
                for r in T.refs(e):
                    b = actions.get(r)
                    if b is None or b.thread != a.thread or b.id == a.id:
                        bad(f"{a.id}: expression refers to {r!r}, not an earlier action of the same thread")
                    if b.kind == "read" and not b.done < a.start:
                        bad(f"{a.id}: refers to read {r} whose done does not precede it")
                    if b.kind != "read" and not b.start < a.start:
                        bad(f"{a.id}: refers to {r} which does not start before it")

        self.__dict__.pop("poset", None)
        self.poset  # builds the poset; raises MalformedSetup on a cycle (rule 4)


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _leaves(t: T.Node):
    if isinstance(t, T.Pair):
        yield from _leaves(t.left)
        yield from _leaves(t.right)
    else:
        yield t
