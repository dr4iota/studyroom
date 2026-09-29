"""Exact possibility-set solver for case ``so`` (sync points and observed reads allowed).

Method (own derivation; see SOURCES.md):

1. The values a full schedule ``(L, pi)`` produces depend only on its *effect order*
   ``sigma`` (the actions sorted by ``pi``).  ``sigma`` is realisable by some
   ``L in Lin(P)`` iff it is a linear extension of the *effect poset* ``Q`` on actions,
   ``a <_Q b  iff  done(a) <_P start(b)``.
   For a fixed ``L`` the same holds with ``Q_L``: ``a < b`` iff
   ``pos_L(done(a)) < pos_L(start(b))``.
2. Reads that are neither observed nor referenced (transitively) by any write are
   *passive*: they change no block and no feasibility check, so they are left out of the
   dynamic programme and their ``Poss`` is read off the surviving states afterwards.
3. The remaining (*active*) actions are handled by a dynamic programme over the
   down-sets of ``Q``.  A forward pass collects, per down-set, the reachable execution
   states (block contents plus the values of reads still needed by writes that have not
   taken effect), enforcing observations on the transitions.  A backward pass keeps the
   states from which a full feasible schedule can still be completed.  ``Poss`` sets are
   read off the transitions between surviving states; witnesses are rebuilt from parent
   and successor pointers, re-executed, and turned into a linearization by a
   topological sort of ``P`` extended with the effect chain.
"""

from __future__ import annotations

from typing import Any, Callable

import harness.terms as T
from harness.model import Action, Setup
from harness.poset import Linearization
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities

# An execution state: (block contents, pending read values).  ``pending`` has one slot
# per read that some write depends on; a slot is ``None`` before the read takes effect
# and again once every write that needs it has taken effect.
State = tuple[tuple, tuple]


def _bits(m: int):
    i = 0
    while m:
        if m & 1:
            yield i
        m >>= 1
        i += 1


def _popcount(m: int) -> int:
    return bin(m).count("1")


class _Engine:
    """One solve: builds ``Q``, runs the two passes, and can rebuild witnesses."""

    def __init__(self, setup: Setup, linearization: Linearization | None) -> None:
        self.setup = setup
        self.lin = linearization
        self.poset = setup.poset
        self.acts: list[Action] = list(setup.actions.values())
        self.n = len(self.acts)
        self.idx: dict[str, int] = {a.id: i for i, a in enumerate(self.acts)}
        self.is_read = [a.kind == "read" for a in self.acts]
        self.M = setup.blocks
        self._build_effect_poset()
        self._build_dependencies()
        self._enabled_cache: dict[int, list[int]] = {}
        # filled by run()
        self.reached: dict[int, dict[State, Any]] = {}
        self.good: dict[int, dict[State, Any]] = {}
        self.read_poss: dict[int, set] = {}
        self.final_poss: dict[int, set] = {}
        self.wit_read: dict[tuple, tuple] = {}
        self.wit_pass: dict[tuple, tuple] = {}
        self.wit_final: dict[tuple, State] = {}

    # ------------------------------------------------------------------ structure

    def _build_effect_poset(self) -> None:
        """``pred[j]``: bitmask of actions that must take effect before action ``j``."""
        n = self.n
        poset = self.poset
        pred = [0] * n
        if self.lin is None:
            # reach[u] = bitmask of nodes strictly reachable from u in P
            N = len(poset)
            reach = [0] * N
            for u in reversed(poset.topological_order()):
                m = 0
                for v in poset.succs[u]:
                    m |= (1 << v) | reach[v]
                reach[u] = m
            done_reach = [reach[poset.done_node[a.id]] for a in self.acts]
            for j, b in enumerate(self.acts):
                sb = poset.start_node[b.id]
                m = 0
                for i in range(n):
                    if i != j and (done_reach[i] >> sb) & 1:
                        m |= 1 << i
                pred[j] = m
        else:
            pos = poset.positions(self.lin)
            done_pos = [pos[poset.done_node[a.id]] for a in self.acts]
            for j, b in enumerate(self.acts):
                sb = pos[poset.start_node[b.id]]
                m = 0
                for i in range(n):
                    if i != j and done_pos[i] < sb:
                        m |= 1 << i
                pred[j] = m
        self.pred = pred
        succ = [0] * n
        for j in range(n):
            for i in _bits(pred[j]):
                succ[i] |= 1 << j
        self.succ = succ

    def _build_dependencies(self) -> None:
        n = self.n
        memo: dict[int, set[int]] = {}

        def deps(i: int) -> set[int]:
            """Reads that the content of write ``i`` depends on, transitively."""
            if i in memo:
                return memo[i]
            s: set[int] = set()
            data = self.acts[i].data
            if data is not None:
                for x in T.refs(data):
                    k = self.idx[x]
                    if self.is_read[k]:
                        s.add(k)
                    else:
                        s |= deps(k)
            memo[i] = s
            return s

        writers_mask = [0] * n
        self.static: list[Any] = [None] * n
        for i, a in enumerate(self.acts):
            if self.is_read[i]:
                continue
            d = deps(i)
            for r in d:
                writers_mask[r] |= 1 << i
            if not d:
                self.static[i] = self.setup.static_content(a.id)
        self.read_slot: dict[int, int] = {}
        self.slot_writers: list[int] = []
        for i in range(n):
            if self.is_read[i] and writers_mask[i]:
                self.read_slot[i] = len(self.slot_writers)
                self.slot_writers.append(writers_mask[i])
        self.write_prunes: list[list[int]] = [[] for _ in range(n)]
        for slot, wm in enumerate(self.slot_writers):
            for w in _bits(wm):
                self.write_prunes[w].append(slot)
        active = 0
        for i, a in enumerate(self.acts):
            if not self.is_read[i] or a.observed is not None or i in self.read_slot:
                active |= 1 << i
        self.active_mask = active
        self.active = [i for i in range(n) if (active >> i) & 1]
        self.passive = [i for i in range(n) if not (active >> i) & 1]
        self.pred_active = [self.pred[i] & active for i in range(n)]
        self.succ_active = [self.succ[i] & active for i in range(n)]

    # ------------------------------------------------------------------ semantics

    def _content(self, a: int, getread: Callable[[int], Any]) -> Any:
        """Content of write ``a``; ``getread(i)`` gives the value returned by read ``i``."""
        st = self.static[a]
        if st is not None:
            return st
        act = self.acts[a]
        if act.data is None:
            return T.Unk(act.id)

        def lookup(x: str) -> Any:
            i = self.idx[x]
            if self.is_read[i]:
                return getread(i)
            return self._content(i, getread)

        return T.substitute(act.data, lookup)

    def _step(self, S: int, st: State, a: int):
        """Fire action ``a`` from state ``st`` at down-set ``S``.

        Returns ``(S2, st2, value)`` (``value`` is the read result, or None for a write),
        or None when an observed read would not return its observed term.
        """
        contents, pending = st
        act = self.acts[a]
        S2 = S | (1 << a)
        if self.is_read[a]:
            v = contents[act.block]
            if act.observed is not None and v != act.observed:
                return None
            slot = self.read_slot.get(a)
            if slot is not None:
                pending = pending[:slot] + (v,) + pending[slot + 1:]
            return S2, (contents, pending), v
        c = self._content(a, lambda i: pending[self.read_slot[i]])
        b = act.block
        contents = contents[:b] + (c,) + contents[b + 1:]
        prunes = self.write_prunes[a]
        if prunes:
            newp = list(pending)
            changed = False
            for slot in prunes:
                if newp[slot] is not None and (self.slot_writers[slot] & ~S2) == 0:
                    newp[slot] = None
                    changed = True
            if changed:
                pending = tuple(newp)
        return S2, (contents, pending), None

    def _enabled(self, S: int) -> list[int]:
        en = self._enabled_cache.get(S)
        if en is None:
            en = [a for a in self.active if not (S >> a) & 1 and (self.pred_active[a] & ~S) == 0]
            self._enabled_cache[S] = en
        return en

    # ------------------------------------------------------------------ the two passes

    def run(self) -> bool:
        """Compute the possibility sets; returns False when the setup is inconsistent."""
        full = self.active_mask
        init_state: State = (tuple(self.setup.init), (None,) * len(self.slot_writers))
        reached: dict[int, dict[State, Any]] = {0: {init_state: None}}
        frontier = [0]
        while frontier:
            nxt: dict[int, None] = {}
            for S in frontier:
                en = self._enabled(S)
                for st in reached[S]:
                    for a in en:
                        res = self._step(S, st, a)
                        if res is None:
                            continue
                        S2, st2, _ = res
                        d = reached.get(S2)
                        if d is None:
                            d = reached[S2] = {}
                            nxt[S2] = None
                        if st2 not in d:
                            d[st2] = (S, st, a)
            frontier = list(nxt)
        self.reached = reached
        if not reached.get(full):
            return False

        read_poss: dict[int, set] = {i: set() for i in range(self.n) if self.is_read[i]}
        good: dict[int, dict[State, Any]] = {}
        for S in sorted(reached, key=_popcount, reverse=True):
            g: dict[State, Any] = {}
            if S == full:
                for st in reached[S]:
                    g[st] = None
                good[S] = g
                continue
            en = self._enabled(S)
            for st in reached[S]:
                first = None
                for a in en:
                    res = self._step(S, st, a)
                    if res is None:
                        continue
                    S2, st2, v = res
                    g2 = good.get(S2)
                    if g2 is None or st2 not in g2:
                        continue
                    if first is None:
                        first = (a, S2, st2)
                    if self.is_read[a]:
                        ps = read_poss[a]
                        if v not in ps:
                            ps.add(v)
                            self.wit_read[(a, v)] = (S, st, a, S2, st2)
                if first is not None:
                    g[st] = first
            good[S] = g
        self.good = good

        # passive reads: any surviving state where they could take effect
        if self.passive:
            for S, g in good.items():
                if not g:
                    continue
                for r in self.passive:
                    if (self.pred_active[r] & ~S) or (self.succ_active[r] & S):
                        continue
                    b = self.acts[r].block
                    ps = read_poss[r]
                    for st in g:
                        v = st[0][b]
                        if v not in ps:
                            ps.add(v)
                            self.wit_pass[(r, v)] = (S, st)
        self.read_poss = read_poss

        final_poss: dict[int, set] = {b: set() for b in range(self.M)}
        for st in reached[full]:
            for b in range(self.M):
                v = st[0][b]
                if v not in final_poss[b]:
                    final_poss[b].add(v)
                    self.wit_final[(b, v)] = st
        self.final_poss = final_poss
        return True

    # ------------------------------------------------------------------ witnesses

    def _prefix(self, S: int, st: State) -> list[int]:
        out: list[int] = []
        while True:
            p = self.reached[S][st]
            if p is None:
                break
            S, st, a = p
            out.append(a)
        out.reverse()
        return out

    def _suffix(self, S: int, st: State) -> list[int]:
        out: list[int] = []
        full = self.active_mask
        while S != full:
            a, S, st = self.good[S][st]
            out.append(a)
        return out

    def _complete(self, sigma: list[int], skip: int | None) -> list[int]:
        """Insert the passive reads (except ``skip``) at positions compatible with Q."""
        order = sorted((r for r in self.passive if r != skip), key=lambda r: _popcount(self.pred[r]))
        for r in order:
            pm = self.pred[r]
            pos = 0
            for k, a in enumerate(sigma):
                if (pm >> a) & 1:
                    pos = k + 1
            sigma.insert(pos, r)
        return sigma

    def _execute(self, sigma: list[int]):
        contents = list(self.setup.init)
        vals: dict[int, Any] = {}
        results: dict[str, Any] = {}
        for a in sigma:
            act = self.acts[a]
            if self.is_read[a]:
                v = contents[act.block]
                if act.observed is not None and v != act.observed:
                    return None
                vals[a] = v
                results[act.id] = v
            else:
                contents[act.block] = self._content(a, vals.__getitem__)
        return results, contents

    def _order_for(self, sigma: list[int]) -> Linearization | None:
        """A linearization of P in which ``sigma`` is a valid effect order."""
        if self.lin is not None:
            return tuple(self.lin)
        poset = self.poset
        N = len(poset)
        total = N + self.n
        succs = [list(s) for s in poset.succs] + [[] for _ in range(self.n)]
        indeg = [len(p) for p in poset.preds] + [0] * self.n
        for i, a in enumerate(self.acts):
            e = N + i
            s, d = poset.start_node[a.id], poset.done_node[a.id]
            succs[s].append(e)
            indeg[e] += 1
            succs[e].append(d)
            indeg[d] += 1
        for x, y in zip(sigma, sigma[1:]):
            succs[N + x].append(N + y)
            indeg[N + y] += 1
        ready = [x for x in range(total) if indeg[x] == 0]
        out: list[int] = []
        while ready:
            x = ready.pop()
            out.append(x)
            for y in succs[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    ready.append(y)
        if len(out) != total:
            return None
        return tuple(x for x in out if x < N)

    def _valid_order(self, order: Linearization, sigma: list[int]) -> bool:
        poset = self.poset
        N = len(poset)
        if len(order) != N or len(set(order)) != N:
            return False
        pos = poset.positions(order)
        for v in range(N):
            for u in poset.preds[v]:
                if pos[u] > pos[v]:
                    return False
        # sigma must extend the interval order of ``order``
        start_pos = [pos[poset.start_node[a.id]] for a in self.acts]
        done_pos = [pos[poset.done_node[a.id]] for a in self.acts]
        max_start = -1
        for a in sigma:
            if done_pos[a] < max_start:
                return False
            if start_pos[a] > max_start:
                max_start = start_pos[a]
        return True

    def _schedule(self, sigma: list[int], skip: int | None, cert: tuple) -> Schedule | None:
        sigma = self._complete(list(sigma), skip)
        if len(sigma) != self.n or len(set(sigma)) != self.n:
            return None
        ex = self._execute(sigma)
        if ex is None:
            return None
        results, contents = ex
        kind, key, v = cert
        if kind == "id":
            if results.get(self.acts[key].id) != v:
                return None
            certifies = {"id": self.acts[key].id, "value": T.to_value(v)}
        else:
            if contents[key] != v:
                return None
            certifies = {"block": key, "value": T.to_value(v)}
        order = self._order_for(sigma)
        if order is None or not self._valid_order(order, sigma):
            return None
        effects = [self.acts[a].id for a in sigma]
        return Schedule(order, effects, results, list(contents), True, {"certifies": certifies})

    def witnesses(self) -> list[Schedule]:
        out: list[Schedule] = []
        full = self.active_mask
        for (r, v), (S, st, a, S2, st2) in self.wit_read.items():
            sigma = self._prefix(S, st) + [a] + self._suffix(S2, st2)
            s = self._schedule(sigma, None, ("id", r, v))
            if s is not None:
                out.append(s)
        for (r, v), (S, st) in self.wit_pass.items():
            sigma = self._prefix(S, st) + [r] + self._suffix(S, st)
            s = self._schedule(sigma, r, ("id", r, v))
            if s is not None:
                out.append(s)
        for (b, v), st in self.wit_final.items():
            sigma = self._prefix(full, st)
            s = self._schedule(sigma, None, ("block", b, v))
            if s is not None:
                out.append(s)
        return out


@register
class DownsetDPSolver(Solver):
    name = "fable51_1-so-downset-dp"
    description = "Exact Poss sets by a forward/backward DP over down-sets of the effect poset (sync, observed reads; modes all+fixed; witnesses)."
    capabilities = SolverCapabilities(
        rcw=False,
        sync=True,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        eng = _Engine(setup, linearization)
        if not eng.run():
            return Outcomes(mode=mode, consistent=False)
        results = {eng.acts[i].id: set(vals) for i, vals in eng.read_poss.items()}
        final = {b: set(vals) for b, vals in eng.final_poss.items()}
        try:
            witnesses = eng.witnesses()
        except Exception:  # never let witness building sink the answer
            witnesses = []
        return Outcomes(mode=mode, consistent=True, results=results, final=final, witnesses=witnesses)
