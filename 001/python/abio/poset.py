"""The trace poset ``P`` (premise.md §2.1-2.3) on the quotient by ``at`` events.

Nodes are the steps that appear in a linearization: every start and done endpoint,
every ``before``/``after`` event, and one virtual node ``sync.k`` per sync point.
``at: k`` events are not nodes: they are merged into ``sync.k``.

A **linearization** is represented everywhere in this library as a tuple of node
indices (``Linearization = tuple[int, ...]``) listing every node exactly once; position
in the tuple is the timestamp. ``names``/``from_names`` convert to and from the step
names used in documents.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Sequence

if TYPE_CHECKING:
    from .model import Setup

Linearization = tuple[int, ...]


class TracePoset:
    def __init__(self, setup: "Setup") -> None:
        from .model import MalformedSetup

        self.names: list[str] = []
        self.kind: list[str] = []  # start | done | event | sync
        self.thread: list[int | None] = []  # owning thread; None for sync nodes
        self.action: list[str | None] = []  # action id for endpoints
        self.index: dict[str, int] = {}

        def add(name: str, kind: str, t: int | None, a: str | None) -> int:
            self.index[name] = len(self.names)
            self.names.append(name)
            self.kind.append(kind)
            self.thread.append(t)
            self.action.append(a)
            return self.index[name]

        self.start_node: dict[str, int] = {}
        self.done_node: dict[str, int] = {}
        # Program order of each thread, with at-events replaced by their sync node.
        self.thread_chains: list[list[int]] = []
        pending_sync: list[tuple[int, int, str]] = []  # (node, sync point, before|after)
        for ti, th in enumerate(setup.threads):
            chain: list[int | tuple[str, int]] = []
            for si, s in enumerate(th.steps):
                if s.kind == "at":
                    chain.append(("at", s.target))
                    continue
                name = setup.step_name(ti, si)
                if s.is_start:
                    n = add(name, "start", ti, s.id)
                    self.start_node[s.id] = n
                elif s.kind == "done":
                    n = add(name, "done", ti, s.target)
                    self.done_node[s.target] = n
                else:
                    n = add(name, "event", ti, None)
                    pending_sync.append((n, s.target, s.kind))
                chain.append(n)
            self.thread_chains.append(chain)  # type: ignore[arg-type]
        self.sync_nodes = [add(f"sync.{k}", "sync", None, None) for k in range(setup.sync_points)]
        self.thread_chains = [[self.sync_nodes[x[1]] if isinstance(x, tuple) else x for x in c] for c in self.thread_chains]

        n = len(self.names)
        edges: set[tuple[int, int]] = set()
        for c in self.thread_chains:
            edges.update(zip(c, c[1:]))
        for node, k, rel in pending_sync:
            edges.add((node, self.sync_nodes[k]) if rel == "before" else (self.sync_nodes[k], node))
        self.preds: list[list[int]] = [[] for _ in range(n)]
        self.succs: list[list[int]] = [[] for _ in range(n)]
        for u, v in sorted(edges):
            self.preds[v].append(u)
            self.succs[u].append(v)

        # Chain partition used by the positions DP: each thread's non-virtual nodes,
        # then one singleton chain per sync node (a sync node may sit on several threads).
        self.chains: list[list[int]] = [[x for x in c if self.kind[x] != "sync"] for c in self.thread_chains]
        self.chains += [[s] for s in self.sync_nodes]
        self.chain_of = [0] * n
        self.pos_in_chain = [0] * n
        for ci, c in enumerate(self.chains):
            for j, x in enumerate(c):
                self.chain_of[x], self.pos_in_chain[x] = ci, j

        if len(self.topological_order()) != n:
            raise MalformedSetup("the trace poset has a cycle (check before/after/at events)")

    def __len__(self) -> int:
        return len(self.names)

    def topological_order(self) -> list[int]:
        indeg = [len(p) for p in self.preds]
        ready = [x for x in range(len(self)) if indeg[x] == 0]
        out = []
        while ready:
            x = ready.pop()
            out.append(x)
            for y in self.succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    ready.append(y)
        return out

    def to_names(self, order: Iterable[int]) -> list[str]:
        return [self.names[x] for x in order]

    def from_names(self, names: Iterable[str]) -> Linearization:
        """Convert names to indices without validating (see :meth:`check`)."""
        return tuple(self.index[s] for s in names)

    def positions(self, order: Sequence[int]) -> list[int]:
        """``pos[node]`` = 0-based timestamp of ``node`` in ``order``."""
        pos = [-1] * len(self)
        for i, x in enumerate(order):
            pos[x] = i
        return pos

    def check(self, names: Sequence[str]) -> list[tuple[str, str, str]]:
        """VAL-LIN: errors as ``(code, step, message)``; empty iff a linearization.

        Codes: UNKNOWN-STEP, DUPLICATE, MISSING, BAD-ORDER.
        """
        errs: list[tuple[str, str, str]] = []
        seen: dict[str, int] = {}
        for i, s in enumerate(names):
            if s not in self.index:
                errs.append(("UNKNOWN-STEP", s, "not a step of this setup"))
            elif s in seen:
                errs.append(("DUPLICATE", s, f"listed at {seen[s] + 1} and {i + 1}"))
            else:
                seen[s] = i
        for s in self.names:
            if s not in seen:
                errs.append(("MISSING", s, "step not listed"))
        for v, ps in enumerate(self.preds):
            for u in ps:
                a, b = self.names[u], self.names[v]
                if a in seen and b in seen and seen[a] > seen[b]:
                    errs.append(("BAD-ORDER", b, f"precedes {a}"))
        return errs
