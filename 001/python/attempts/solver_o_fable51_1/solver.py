"""Exact possibility-set solver for setups without sync points, observed reads allowed.

Method (own derivation; see SOURCES.md).

1. Realizable effect orders.  With ``K = 0`` the trace poset is the disjoint union of
   the threads' program orders.  A total order ``sigma`` of the actions is the effect
   order of some full schedule ``(L, pi)`` iff ``sigma`` extends

       R = {(a, b) : same thread, done(a) precedes start(b) in program order}.

   Necessity is immediate.  Sufficiency: the constraint graph
   "P plus start(a) -> done(b) for every a <sigma b" is acyclic (a cycle would give a
   strictly increasing cycle in ``sigma``), any of its linear extensions is an ``L`` in
   which ``start(a) <_L done(b)`` for all ``a <sigma b``, and then
   ``pi(a_i) = max(start(a_1..a_i)) + i*eps`` are distinct effect points inside the
   intervals.  For a fixed ``L`` the same holds with
   ``R_L = {(a, b) : done(a) <_L start(b)}``.

   So ``Poss`` over all feasible full schedules equals ``Poss`` over the feasible linear
   extensions of ``R`` (resp. ``R_L``), executed under atomic block semantics.

2. Search.  Depth-first search over the order ideals of ``R`` (sets of actions already
   in effect).  The state is memoized on ``(ideal, block contents, values of the reads
   that some pending write still depends on)``; everything else about the history is
   irrelevant to the future.  Observed reads are checked at their effect, so every
   visited state has a feasible prefix.  A state is *good* if some feasible completion
   exists.  ``Poss(r)`` collects the value returned by ``r`` on every transition into a
   good state; ``Poss(b)`` collects block contents at terminal states.  The setup is
   consistent iff the initial state is good.

3. Witnesses.  Parent pointers give a feasible prefix to each state, completion pointers
   a feasible suffix from each good state.  The concatenation is re-executed and, in
   mode ``all``, turned into a linearization by emitting each action's start (preceded
   by its not yet emitted program-order predecessors) in effect order and the remaining
   ends afterwards.  In mode ``fixed`` the given linearization is used.
"""

from __future__ import annotations

import sys
from typing import Any

from harness import terms as T
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities

_MISSING = object()


@register
class IdealSolver(Solver):
    name = "fable51_1-o-ideals"
    description = (
        "Exact DFS over the order ideals of the realizable effect-order poset, memoized on "
        "(ideal, contents, live read values); modes all and fixed; witnesses."
    )
    capabilities = SolverCapabilities(
        rcw=False,
        sync=False,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        return _Search(setup, linearization).run()


class _Search:
    """One solve call: precomputed tables, the DFS, and witness reconstruction."""

    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.lin = None if lin is None else tuple(lin)
        self.mode = "all" if lin is None else "fixed"
        acts = list(setup.actions.values())
        self.acts = acts
        n = len(acts)
        self.n = n
        self.idx = {a.id: i for i, a in enumerate(acts)}

        # Term interning: block contents and read values are handled as small ints.
        self.term_ids: dict[Any, int] = {}
        self.terms: list[Any] = []

        self.is_read = [a.kind == "read" for a in acts]
        self.block = [a.block for a in acts]
        self.obs = [
            self.intern(a.observed) if (a.kind == "read" and a.observed is not None and not isinstance(a.observed, str)) else -1
            for a in acts
        ]

        # pred[j]: bitmask of the actions that must take effect before j.
        pred = [0] * n
        if self.lin is None:
            for i, a in enumerate(acts):
                for j, b in enumerate(acts):
                    if i != j and a.thread == b.thread and a.done < b.start:
                        pred[j] |= 1 << i
        else:
            poset = setup.poset
            pos = poset.positions(self.lin)
            sp = [pos[poset.start_node[a.id]] for a in acts]
            dp = [pos[poset.done_node[a.id]] for a in acts]
            for i in range(n):
                di = dp[i]
                for j in range(n):
                    if i != j and di < sp[j]:
                        pred[j] |= 1 << i
        self.pred = pred
        self.succ = [[j for j in range(n) if (pred[j] >> i) & 1] for i in range(n)]

        # Read dependencies of writes (transitively through referenced writes).
        self.deps = [[] if self.is_read[i] else self._dep_reads(i) for i in range(n)]
        users = [0] * n
        for w in range(n):
            for r in self.deps[w]:
                users[r] |= 1 << w
        used = [i for i in range(n) if users[i]]
        self.rpos = [-1] * n
        for p, i in enumerate(used):
            self.rpos[i] = p
        self.used_masks = [users[i] for i in used]
        self.rv0 = (-1,) * len(used)

        self.static_id = [-1] * n
        for i, a in enumerate(acts):
            if not self.is_read[i] and not self.deps[i]:
                self.static_id[i] = self.intern(setup.static_content(a.id))
        self.ccache: dict[Any, int] = {}
        self.init_ids = tuple(self.intern(t) for t in setup.init)

    # ------------------------------------------------------------------ helpers

    def intern(self, t: Any) -> int:
        k = self.term_ids.get(t)
        if k is None:
            k = len(self.terms)
            self.term_ids[t] = k
            self.terms.append(t)
        return k

    def _dep_reads(self, i: int) -> list[int]:
        acts = self.acts
        seen: set[str] = set()
        out: list[int] = []
        stack = [] if acts[i].data is None else [acts[i].data]
        while stack:
            e = stack.pop()
            for x in T.refs(e):
                if x in seen:
                    continue
                seen.add(x)
                j = self.idx[x]
                if self.is_read[j]:
                    out.append(j)
                elif acts[j].data is not None:
                    stack.append(acts[j].data)
        out.sort()
        return out

    def content_id(self, i: int, rv: tuple) -> int:
        """Interned content of write ``i`` given the live read values ``rv``."""
        s = self.static_id[i]
        if s >= 0:
            return s
        rpos = self.rpos
        ck = (i, tuple([rv[rpos[j]] for j in self.deps[i]]))
        c = self.ccache.get(ck)
        if c is None:
            c = self.intern(self._write_term(i, rv))
            self.ccache[ck] = c
        return c

    def _write_term(self, i: int, rv: tuple) -> Any:
        a = self.acts[i]
        if a.data is None:
            return T.Unk(a.id)
        terms = self.terms
        idx = self.idx
        is_read = self.is_read
        rpos = self.rpos

        def lookup(x: str) -> Any:
            j = idx[x]
            if is_read[j]:
                return terms[rv[rpos[j]]]
            return terms[self.content_id(j, rv)]

        return T.substitute(a.data, lookup)

    # ------------------------------------------------------------------ search

    def run(self) -> Outcomes:
        n = self.n
        full = (1 << n) - 1
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 2000))
        pred, succ = self.pred, self.succ
        is_read, block, obs, rpos = self.is_read, self.block, self.obs, self.rpos
        used_masks = self.used_masks
        has_used = bool(used_masks)
        content_id = self.content_id
        memo: dict[Any, Any] = {}
        parent: dict[Any, tuple] = {}
        compl: dict[Any, Any] = {}
        res: list[set[int]] = [set() for _ in range(n)]
        fin: list[set[int]] = [set() for _ in range(self.setup.blocks)]
        wit_read: dict[tuple[int, int], tuple] = {}
        wit_final: dict[tuple[int, int], Any] = {}

        def key_of(done: int, contents: tuple, rv: tuple):
            if has_used:
                nd = ~done
                return (done, contents, tuple([v if (um & nd) else -1 for v, um in zip(rv, used_masks)]))
            return (done, contents)

        def explore(done: int, avail: int, contents: tuple, rv: tuple, pkey: Any, pact: Any):
            """Return this state's key if a feasible completion exists, else None."""
            key = key_of(done, contents, rv)
            r = memo.get(key, _MISSING)
            if r is not _MISSING:
                return r
            parent[key] = (pkey, pact)
            if done == full:
                for b, c in enumerate(contents):
                    s = fin[b]
                    if c not in s:
                        s.add(c)
                        wit_final[(b, c)] = key
                memo[key] = key
                compl[key] = None
                return key
            good = False
            m = avail
            while m:
                low = m & -m
                m ^= low
                i = low.bit_length() - 1
                ndone = done | low
                nav = avail ^ low
                for j in succ[i]:
                    pj = pred[j]
                    if (pj & ndone) == pj:
                        nav |= 1 << j
                if is_read[i]:
                    v = contents[block[i]]
                    o = obs[i]
                    if o >= 0 and v != o:
                        continue
                    p = rpos[i]
                    nrv = rv if p < 0 else rv[:p] + (v,) + rv[p + 1:]
                    ck = explore(ndone, nav, contents, nrv, key, i)
                    if ck is not None:
                        s = res[i]
                        if v not in s:
                            s.add(v)
                            wit_read[(i, v)] = (key, ck)
                        if not good:
                            good = True
                            compl[key] = (i, ck)
                else:
                    c = content_id(i, rv)
                    b = block[i]
                    nc = contents if contents[b] == c else contents[:b] + (c,) + contents[b + 1:]
                    ck = explore(ndone, nav, nc, rv, key, i)
                    if ck is not None and not good:
                        good = True
                        compl[key] = (i, ck)
            r = key if good else None
            memo[key] = r
            return r

        avail0 = 0
        for i in range(n):
            if pred[i] == 0:
                avail0 |= 1 << i
        root = explore(0, avail0, self.init_ids, self.rv0, None, None)
        meta = {"states": len(memo)}
        if root is None:
            return Outcomes(self.mode, False, {}, {}, [], meta)

        terms = self.terms
        results = {self.acts[i].id: {terms[v] for v in res[i]} for i in range(n) if is_read[i]}
        final = {b: {terms[c] for c in fin[b]} for b in range(self.setup.blocks)}

        # ---------------------------------------------------------- witnesses
        def path_to(key: Any) -> list[int]:
            out: list[int] = []
            while True:
                pkey, pact = parent[key]
                if pact is None:
                    break
                out.append(pact)
                key = pkey
            out.reverse()
            return out

        def completion(key: Any) -> list[int]:
            out: list[int] = []
            while True:
                c = compl[key]
                if c is None:
                    break
                out.append(c[0])
                key = c[1]
            return out

        witnesses: list[Schedule] = []
        for (i, v), (skey, ck) in wit_read.items():
            sigma = path_to(skey) + [i] + completion(ck)
            cert = {"id": self.acts[i].id, "value": T.to_value(terms[v])}
            sch = self._schedule(sigma, cert)
            if sch is not None:
                witnesses.append(sch)
        for (b, c), tkey in wit_final.items():
            sigma = path_to(tkey)
            cert = {"block": b, "value": T.to_value(terms[c])}
            sch = self._schedule(sigma, cert)
            if sch is not None:
                witnesses.append(sch)

        return Outcomes(self.mode, True, results, final, witnesses, meta)

    # ------------------------------------------------------------------ witnesses

    def _schedule(self, sigma: list[int], cert: dict) -> Schedule | None:
        """Re-execute effect order ``sigma`` and package it as a Schedule; None if it fails."""
        setup = self.setup
        acts = self.acts
        if len(sigma) != self.n or len(set(sigma)) != self.n:
            return None
        vals: dict[str, Any] = {}
        contents = list(setup.init)
        results: dict[str, Any] = {}

        def content_of(aid: str) -> Any:
            a = setup.actions[aid]
            if a.data is None:
                return T.Unk(aid)
            return T.substitute(a.data, lookup)

        def lookup(x: str) -> Any:
            v = vals.get(x)
            return v if v is not None else content_of(x)

        for i in sigma:
            a = acts[i]
            if a.kind == "read":
                v = contents[a.block]
                if a.observed is not None and v != a.observed:
                    return None
                results[a.id] = v
                vals[a.id] = v
            else:
                c = content_of(a.id)
                vals[a.id] = c
                contents[a.block] = c
        if "id" in cert:
            got = results.get(cert["id"])
        else:
            got = contents[cert["block"]]
        if got is None or T.to_value(got) != cert["value"]:
            return None
        order = self.lin if self.lin is not None else self._order_for(sigma)
        if order is None:
            return None
        return Schedule(order, [acts[i].id for i in sigma], results, contents, True, {"certifies": cert})

    def _order_for(self, sigma: list[int]) -> tuple[int, ...] | None:
        """A linearization realizing effect order ``sigma`` (mode ``all``, K = 0)."""
        poset = self.setup.poset
        chains = poset.chains
        chain_of = poset.chain_of
        pos_in_chain = poset.pos_in_chain
        ptr = [0] * len(chains)
        order: list[int] = []
        for i in sigma:
            target = poset.start_node[self.acts[i].id]
            ci = chain_of[target]
            pi = pos_in_chain[target]
            if pi < ptr[ci]:
                continue  # already emitted as a predecessor of an earlier start
            order.extend(chains[ci][ptr[ci]:pi + 1])
            ptr[ci] = pi + 1
        for ci, ch in enumerate(chains):
            order.extend(ch[ptr[ci]:])
        if len(order) != len(poset) or len(set(order)) != len(poset):
            return None
        return tuple(order)
