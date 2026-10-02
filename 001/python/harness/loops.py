"""Loop setups: each thread is ``prefix · body^n · suffix`` for one global ``n ≥ 1``.

Document (``format: loop-setup``, version 1)::

    format: loop-setup
    version: 1
    id: "loop-1"
    blocks: 2
    sync_points: 1          # plain sync points, for events in prefixes and suffixes
    loop_sync_points: 1     # per-iteration sync points, for events in bodies
    init: [0, "*"]
    threads:
      - id: t0
        prefix: [ ...steps... ]
        body:   [ ...steps... ]
        suffix: [ ...steps... ]

Steps are the steps of a setup (formats.md §1), with these rules:

- **Actions:** reads and writes only. Every action ends in the segment it starts in.
  Action and event ids must not contain ``__``, which marks unrolled copies.
- **Body data:** a constant or a reference to *one* read. The read must be earlier in
  the same iteration, or in the thread's prefix. No ``"*"`` and no pairs in a body,
  since either would make values grow with ``n``.
- **Prefix and suffix data:** any expression. A suffix may refer to prefix and suffix
  actions only.
- **Events:** in a prefix or suffix, ``k`` names plain sync point ``k``. In a body,
  ``k`` names the per-iteration sync point ``k``: iteration ``i``'s event on ``k`` refers
  to that iteration's own instance, so iteration ``i`` of one thread meets iteration
  ``i`` of the others.

``unroll(n)`` gives the ordinary :class:`~harness.model.Setup` ``P_n``:
- body action and event ids get the suffix ``__i`` (``i = 1..n``);
- plain sync point ``k`` stays ``k``;
- per-iteration sync point ``j`` in iteration ``i`` becomes ``K + (i - 1)·Kb + j``, where
  ``K = sync_points`` and ``Kb = loop_sync_points``.

The answers for a loop setup at ``n`` are ``|Lin(P_n)|``, and the possibility sets of
``P_n``, where a body read's set is the union over its ``n`` instances (``project``).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from . import terms as T
from .model import ACTION_KINDS, EVENT_KINDS, FORMAT_VERSION, MalformedSetup, Setup, Step

SEGMENTS = ("prefix", "body", "suffix")


@dataclass
class LoopThread:
    id: str
    prefix: list[Step]
    body: list[Step]
    suffix: list[Step]

    def segment(self, name: str) -> list[Step]:
        return getattr(self, name)


@dataclass
class LoopAction:
    id: str
    kind: str  # read | write
    block: int
    thread: int
    segment: str  # prefix | body | suffix
    data: T.Expr | None  # writes: the expression; reads: None


@dataclass
class LoopSetup:
    """A parsed, validated loop setup. Construct with :meth:`from_doc`."""

    id: str
    blocks: int
    sync_points: int
    loop_sync_points: int
    init: list[T.Term]
    threads: list[LoopThread]
    actions: dict[str, LoopAction] = field(default_factory=dict)
    doc: dict = field(default_factory=dict, repr=False)

    # ------------------------------------------------------------------ parsing

    @staticmethod
    def from_doc(doc: dict) -> "LoopSetup":
        if not isinstance(doc, dict) or doc.get("format") != "loop-setup" or doc.get("version") != 1:
            raise MalformedSetup("not a loop-setup version 1 document")
        blocks = int(doc["blocks"])
        try:
            init = [T.Init(b) if v == "*" else T.parse_term(v) for b, v in enumerate(doc.get("init", ["*"] * blocks))]
        except T.TermSyntaxError as ex:
            raise MalformedSetup(f"init: {ex}") from None
        threads, actions = [], {}
        for ti, td in enumerate(doc.get("threads") or []):
            segs = {}
            for seg in SEGMENTS:
                segs[seg] = [Step.from_doc(sd, f"thread {td.get('id')} {seg} step {si}")
                             for si, sd in enumerate(td.get(seg) or [])]
            th = LoopThread(td.get("id"), segs["prefix"], segs["body"], segs["suffix"])
            threads.append(th)
            for seg in SEGMENTS:
                for s in segs[seg]:
                    if s.is_start:
                        if s.kind not in ("read", "write"):
                            raise MalformedSetup(f"{s.id}: only reads and writes are allowed in loop setups")
                        actions[s.id] = LoopAction(s.id, s.kind, s.target, ti, seg, s.data)
        ls = LoopSetup(str(doc.get("id", "")), blocks, int(doc.get("sync_points", 0)),
                       int(doc.get("loop_sync_points", 0)), init, threads, actions, copy.deepcopy(doc))
        ls._validate()
        return ls

    def _validate(self) -> None:
        for th in self.threads:
            for seg in SEGMENTS:
                started, ended = set(), set()
                for s in th.segment(seg):
                    for ident in (s.id, s.target if s.kind == "done" else None):
                        if isinstance(ident, str) and "__" in ident:
                            raise MalformedSetup(f"id {ident!r} contains '__'")
                    if s.is_start:
                        started.add(s.id)
                    elif s.kind == "done":
                        if s.target not in started:
                            raise MalformedSetup(f"{s.target}: done in a different segment from its start")
                        ended.add(s.target)
                        if s.data is not None:
                            raise MalformedSetup(f"{s.target}: observed results are not part of loop setups")
                    if seg == "body" and s.kind == "write":
                        d = s.data
                        if d is None or isinstance(d, T.Pair) or not isinstance(d, (T.Const, T.Ref)):
                            raise MalformedSetup(f"{s.id}: body data must be a constant or one read reference")
                        if isinstance(d, T.Ref):
                            src = self.actions.get(d.action)
                            if src is None or src.kind != "read" or src.thread != self.threads.index(th) \
                                    or src.segment not in ("prefix", "body"):
                                raise MalformedSetup(f"{s.id}: body data must refer to a read of this thread's body or prefix")
                    if seg == "suffix" and s.kind == "write" and s.data is not None:
                        for r in T.refs(s.data):
                            if self.actions.get(r) is None or self.actions[r].segment == "body":
                                raise MalformedSetup(f"{s.id}: suffix data may refer to prefix and suffix actions only")
                    if s.is_event:
                        limit = self.loop_sync_points if seg == "body" else self.sync_points
                        if not 0 <= s.target < limit:
                            raise MalformedSetup(f"{seg} event on {s.target}: out of range 0..{limit - 1}")
                if started != ended:
                    raise MalformedSetup(f"thread {th.id} {seg}: actions {sorted(started - ended)} do not end in it")
        for n in (1, 2, 3):  # rule-level checks of the unrolled setup (references, acyclicity)
            self.unroll(n)

    # ------------------------------------------------------------------ unrolling

    def unroll(self, n: int) -> Setup:
        if n < 1:
            raise ValueError("n must be >= 1")
        K, Kb = self.sync_points, self.loop_sync_points
        body_ids = {a for a, x in self.actions.items() if x.segment == "body"}

        def rename_expr(e, i):
            return T.substitute(e, lambda r: T.Ref(f"{r}__{i}" if r in body_ids else r))

        def copy_step(s: Step, i: int | None) -> dict:
            d = s.to_doc()
            if i is None:
                return d
            if s.is_start:
                d["id"] = f"{s.id}__{i}"
                if s.kind == "write":
                    d["data"] = T.to_value(rename_expr(s.data, i))
            elif s.kind == "done":
                d["done"] = f"{s.target}__{i}"
            else:
                d[s.kind] = K + (i - 1) * Kb + s.target
                if s.id is not None:
                    d["id"] = f"{s.id}__{i}"
            return d

        threads = []
        for th in self.threads:
            steps = [copy_step(s, None) for s in th.prefix]
            for i in range(1, n + 1):
                steps += [copy_step(s, i) for s in th.body]
            steps += [copy_step(s, None) for s in th.suffix]
            threads.append({"id": th.id, "steps": steps})
        doc = {"format": "setup", "version": FORMAT_VERSION, "id": f"{self.id}@n={n}", "blocks": self.blocks,
               "sync_points": K + n * Kb, "init": ["*" if t == T.Init(b) else T.to_value(t) for b, t in enumerate(self.init)],
               "threads": threads}
        return Setup.from_doc(doc)

    def to_doc(self) -> dict:
        return copy.deepcopy(self.doc)

    def reads(self) -> list[str]:
        return [a for a, x in self.actions.items() if x.kind == "read"]


def base_id(aid: str) -> str:
    """The loop-setup id of an unrolled action id (``r__3`` → ``r``)."""
    return aid.split("__", 1)[0]


def project(results: dict[str, set]) -> dict[str, set]:
    """Merge unrolled per-instance sets into per-read sets of the loop setup."""
    out: dict[str, set] = {}
    for k, vs in results.items():
        out.setdefault(base_id(k), set()).update(vs)
    return out
