"""Enumerator and counter of ``LinFeas(P)`` for case ``or`` (K = 0, observed read and
RCW results, RCW actions).

Method (own derivation; see SOURCES.md)
---------------------------------------
With no sync points the trace poset is a disjoint union of thread chains, so a
linearization ``L`` is an interleaving of those chains.  ``L`` gives every action ``a``
the closed interval ``[pos(start a), pos(end a)]``.  A full schedule ``(L, pi)`` with
distinct effect points is, up to the choice of the real numbers, the same thing as a
total *execution order* ``T`` of the actions that extends the interval order of ``L``
(``a`` before ``b`` whenever ``end(a)`` precedes ``start(b)`` in ``L``); any such ``T``
is realised by effect points, and any effect points give such a ``T``.  Hence ``L`` is
feasible iff some ``T`` extending its interval order, executed with the atomic block
semantics, returns every observed result.

Equivalently, ``T`` can be produced while ``L`` is built node by node: an action may be
executed at any moment after its start has been placed and before its end is placed.
So we build ``L`` by depth-first search over the interleavings and carry along the set
of *states* compatible with the prefix.  A state is

    (E, contents, rv)

where ``E`` is the set of started-but-not-ended actions that have already executed,
``contents`` is the tuple of block contents, and ``rv`` holds the values returned by
the unobserved reads that some not-yet-executed expression still needs.  Placing a
start makes the action executable, and the state set is closed under executing any
executable action whose observed result (if it has one) matches.  Placing an end keeps
the states in which that action has executed (and drops it from ``E``).  The prefix is
dead when the set becomes empty; a complete ``L`` with a non-empty set is feasible.

Unobserved reads that no expression references never influence anything, so they are
not tracked at all.  Once every observed action has ended, every completion of the
prefix is feasible, so tracking stops (and the counter uses a multinomial coefficient).
The counter memoises on (chain positions, state set).
"""

from __future__ import annotations

from math import comb
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.terms import Unk, refs, substitute

CAPS = Capabilities(rcw=True, sync=False, observed_reads=True)


def _multinomial(ks) -> int:
    total = sum(ks)
    r = 1
    for k in ks:
        r *= comb(total, k)
        total -= k
    return r


class _Problem:
    """Static data of one setup plus the state-set transitions."""

    def __init__(self, setup: Setup) -> None:
        poset = setup.poset
        self.n_nodes = len(poset)
        self.chains: list[list[int]] = [list(c) for c in poset.chains if c]
        self.ids: list[str] = list(setup.actions.keys())
        self.index: dict[str, int] = {aid: i for i, aid in enumerate(self.ids)}
        acts = [setup.actions[aid] for aid in self.ids]
        n = len(acts)
        self.n_actions = n
        self.kind = [a.kind for a in acts]
        self.block = [a.block for a in acts]
        self.data = [a.data for a in acts]
        self.expect = [a.expect for a in acts]
        self.observed = [a.observed for a in acts]  # Term, "ok"/"fail", or None
        self.init = tuple(setup.init)
        self.n_observed = sum(1 for o in self.observed if o is not None)

        referenced: set[str] = set()
        for a in acts:
            for e in (a.data, a.expect):
                if e is not None:
                    referenced |= refs(e)
        # An action matters for feasibility if it can change a block, has an observed
        # result, or is a read whose value some expression uses.
        self.relevant = [
            a.kind != "read" or a.observed is not None or a.id in referenced for a in acts
        ]

        # needs_content[j] / needs_expect[j]: the unobserved reads whose returned value
        # is needed (transitively) to evaluate j's content / expected value.
        self.needs_content: list[set[int] | None] = [None] * n
        self.needs_expect: list[set[int]] = [set() for _ in range(n)]

        def needs_of(expr) -> set[int]:
            out: set[int] = set()
            if expr is None:
                return out
            for r in refs(expr):
                k = self.index[r]
                if self.kind[k] == "read":
                    if self.observed[k] is None:
                        out.add(k)
                else:
                    out |= content_needs(k)
            return out

        def content_needs(k: int) -> set[int]:
            if self.needs_content[k] is None:
                self.needs_content[k] = set()  # guard (references are acyclic anyway)
                self.needs_content[k] = needs_of(self.data[k])
            return self.needs_content[k]

        for j in range(n):
            content_needs(j)
            if self.kind[j] == "rcw":
                self.needs_expect[j] = needs_of(self.expect[j])
        self.needs: list[tuple[int, ...]] = [
            tuple(sorted(self.needs_content[j] | self.needs_expect[j])) for j in range(n)  # type: ignore[operator]
        ]
        users: list[list[int]] = [[] for _ in range(n)]
        for j in range(n):
            for r in self.needs[j]:
                users[r].append(j)
        self.users: list[tuple[int, ...]] = [tuple(u) for u in users]

        # Contents / expected values that do not depend on unobserved reads are cached.
        self.static_content: list = [None] * n
        self.static_expect: list = [None] * n

        # Node tables.
        self.node_action: list[int] = [self.index[a] if a is not None else -1 for a in poset.action]
        self.node_is_start: list[bool] = [k == "start" for k in poset.kind]

    # ------------------------------------------------------------------ evaluation

    def _value(self, j: int, rv: dict):
        """Value of a reference to action ``j``: a read's result or a writer's content."""
        if self.kind[j] == "read":
            o = self.observed[j]
            return o if o is not None else rv[j]
        return self._content(j, rv)

    def _content(self, j: int, rv: dict):
        c = self.static_content[j]
        if c is not None:
            return c
        d = self.data[j]
        if d is None:
            c = Unk(self.ids[j])
        else:
            c = substitute(d, lambda x: self._value(self.index[x], rv))
        if not self.needs_content[j]:
            self.static_content[j] = c
        return c

    def _expected(self, j: int, rv: dict):
        c = self.static_expect[j]
        if c is not None:
            return c
        c = substitute(self.expect[j], lambda x: self._value(self.index[x], rv))
        if not self.needs_expect[j]:
            self.static_expect[j] = c
        return c

    # ------------------------------------------------------------------ transitions

    def initial(self) -> set:
        return {(frozenset(), self.init, frozenset())}

    def _execute(self, j: int, st: tuple, ended: list[bool]):
        """Execute action ``j`` in state ``st``; None if an observed result mismatches."""
        E, contents, rv = st
        b = self.block[j]
        cur = contents[b]
        kind = self.kind[j]
        new_rv = rv
        if kind == "read":
            obs = self.observed[j]
            if obs is not None:
                if cur != obs:
                    return None
            else:
                new_rv = rv | {(j, cur)}
        else:
            rvd = dict(rv) if rv else {}
            if kind == "rcw":
                ok = cur == self._expected(j, rvd)
                obs = self.observed[j]
                if obs is not None:
                    if isinstance(obs, str):
                        if ok != (obs == "ok"):
                            return None
                    elif cur != obs:
                        return None
                if ok:
                    contents = contents[:b] + (self._content(j, rvd),) + contents[b + 1:]
            else:
                contents = contents[:b] + (self._content(j, rvd),) + contents[b + 1:]
        new_E = E | {j}
        needs = self.needs[j]
        if needs and new_rv:
            drop = set()
            for r in needs:
                if all(u in new_E or ended[u] for u in self.users[r]):
                    drop.add(r)
            if drop:
                new_rv = frozenset(p for p in new_rv if p[0] not in drop)
        return (new_E, contents, new_rv)

    def _closure(self, base: set, seeds: list, open_actions: tuple, ended: list[bool]) -> set:
        result = set(base)
        work = []
        for st in seeds:
            if st not in result:
                result.add(st)
                work.append(st)
        while work:
            st = work.pop()
            E = st[0]
            for j in open_actions:
                if j in E:
                    continue
                ns = self._execute(j, st, ended)
                if ns is not None and ns not in result:
                    result.add(ns)
                    work.append(ns)
        return result

    def step_start(self, S: set, open_actions: tuple, j: int, ended: list[bool]):
        nop = open_actions + (j,)
        seeds = []
        for st in S:
            ns = self._execute(j, st, ended)
            if ns is not None:
                seeds.append(ns)
        return self._closure(S, seeds, nop, ended), nop

    def step_done(self, S: set, open_actions: tuple, j: int):
        nS = set()
        for st in S:
            E = st[0]
            if j in E:
                nS.add((E - {j}, st[1], st[2]))
        nop = tuple(x for x in open_actions if x != j)
        return nS, nop


class _Walker:
    """Mutable prefix of a linearization under construction, with undo."""

    def __init__(self, P: _Problem) -> None:
        self.P = P
        self.chains = P.chains
        self.nch = len(self.chains)
        self.lens = [len(c) for c in self.chains]
        self.pos = [0] * self.nch
        self.order: list[int] = []
        self.taken: list[int] = []
        self.ended = [False] * P.n_actions
        self.rem_obs = P.n_observed
        self.states: list[set] = [P.initial()]
        self.opens: list[tuple] = [()]

    def try_step(self, ci: int):
        """(state set, open actions) after placing the head of chain ``ci``."""
        P = self.P
        node = self.chains[ci][self.pos[ci]]
        j = P.node_action[node]
        S = self.states[-1]
        op = self.opens[-1]
        if self.rem_obs == 0 or not P.relevant[j]:
            return S, op
        if P.node_is_start[node]:
            return P.step_start(S, op, j, self.ended)
        return P.step_done(S, op, j)

    def commit(self, ci: int, S: set, op: tuple) -> None:
        P = self.P
        node = self.chains[ci][self.pos[ci]]
        self.pos[ci] += 1
        self.order.append(node)
        self.taken.append(ci)
        self.states.append(S)
        self.opens.append(op)
        if not P.node_is_start[node]:
            j = P.node_action[node]
            self.ended[j] = True
            if P.observed[j] is not None:
                self.rem_obs -= 1

    def undo(self) -> int:
        """Remove the last placed node; returns the chain it came from."""
        P = self.P
        self.order.pop()
        self.states.pop()
        self.opens.pop()
        ci = self.taken.pop()
        self.pos[ci] -= 1
        node = self.chains[ci][self.pos[ci]]
        if not P.node_is_start[node]:
            j = P.node_action[node]
            self.ended[j] = False
            if P.observed[j] is not None:
                self.rem_obs += 1
        return ci

    def remaining(self) -> list[int]:
        return [ln - p for ln, p in zip(self.lens, self.pos)]


@register
class FeasEnumerator(LinEnumerator):
    name = "fable51_1-or-enum"
    description = "DFS over chain interleavings carrying the set of partial executions compatible with the prefix"
    capabilities = CAPS
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        P = _Problem(setup)
        n = P.n_nodes
        if n == 0:
            yield ()
            return
        W = _Walker(P)
        nch, pos, lens = W.nch, W.pos, W.lens
        choice = [0]  # choice[d]: next chain to try at depth d
        while True:
            d = len(W.order)
            if d == n:
                yield tuple(W.order)
                ci = nch
            else:
                ci = choice[d]
                while ci < nch and pos[ci] == lens[ci]:
                    ci += 1
            if ci >= nch:
                if d == 0:
                    return
                choice.pop()
                c = W.undo()
                choice[-1] = c + 1
                continue
            S, op = W.try_step(ci)
            if not S:
                choice[d] = ci + 1
                continue
            W.commit(ci, S, op)
            choice.append(0)


@register
class FeasCounter(LinCounter):
    name = "fable51_1-or-count"
    description = "Counts feasible linearizations by memoised DFS on (chain positions, compatible execution states)"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        P = _Problem(setup)
        total = _multinomial([len(c) for c in P.chains])
        if P.n_observed == 0:
            return CountResult(linearizations=total, feasible=total, method="multinomial")
        feasible = self._count_feasible(P)
        return CountResult(linearizations=total, feasible=feasible, method="memo-dfs")

    @staticmethod
    def _count_feasible(P: _Problem) -> int:
        n = P.n_nodes
        if n == 0:
            return 1
        W = _Walker(P)
        nch, pos, lens = W.nch, W.pos, W.lens
        memo: dict = {}
        # frame: [memo key, accumulated count, next chain to try]
        frames = [[(tuple(pos), frozenset(W.states[-1])), 0, 0]]
        while True:
            fr = frames[-1]
            d = len(W.order)
            if d == n:
                value = 1
            elif W.rem_obs == 0:
                value = _multinomial(W.remaining())
            else:
                ci = fr[2]
                while ci < nch and pos[ci] == lens[ci]:
                    ci += 1
                if ci >= nch:
                    value = fr[1]
                else:
                    fr[2] = ci + 1
                    S, op = W.try_step(ci)
                    if not S:
                        continue
                    W.commit(ci, S, op)
                    key = (tuple(pos), frozenset(S))
                    hit = memo.get(key)
                    if hit is not None:
                        fr[1] += hit
                        W.undo()
                        continue
                    frames.append([key, 0, 0])
                    continue
            memo[fr[0]] = value
            frames.pop()
            if not frames:
                return value
            W.undo()
            frames[-1][1] += value
