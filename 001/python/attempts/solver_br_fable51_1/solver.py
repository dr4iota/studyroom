"""Exact possibility-set solver for cases ``b`` and ``br`` (no sync points, no observations).

Outline (details and provenance in SOURCES.md):

1. *Effect orders.*  With no observations, every linearization is feasible, and the value
   returned by a read/RCW (and every final content) depends only on the order of the
   effect points.  An effect order ``E`` (a total order of the actions) is realizable by
   some linearization and some effect points iff ``E`` is a linear extension of the poset

       ``Q``:   ``b < a``  iff  ``done(b)`` precedes ``start(a)`` in the trace poset,

   i.e. same thread and ``done(b)`` before ``start(a)`` in program order (mode ``all``),
   or ``pos(done(b)) < pos(start(a))`` under the given linearization (mode ``fixed``).
   (Proof sketch: add a node ``pi(a)`` between ``start(a)`` and ``done(a)`` for every
   action; ``E`` is realizable iff that poset plus ``E`` is acyclic, and every cycle
   would have to be a cycle of ``E`` itself.)

2. *Block groups.*  A write's/RCW's content and expected value depend only on reads it
   references (transitively).  Blocks connected by such references are solved together;
   a group's values depend only on the restriction of ``E`` to the group's actions, and
   restrictions of linear extensions of ``Q`` to a subset are exactly the linear
   extensions of the induced sub-poset.

3. *Unreferenced reads* are left out of the search: such a read ``r`` can be inserted
   into an effect order of the other actions anywhere after all its ``Q``-predecessors
   and before all its ``Q``-successors, and it returns the block content at that point.

4. *Memoised search* over states ``(executed set, live block contents, live read values)``
   of the remaining actions of a group; contents of blocks nobody will look at again and
   values of reads nobody will reference again are forgotten, so states merge.

5. *Witnesses.*  Every recorded value remembers the first state/transition that produced
   it; the path back to the root plus a greedy completion gives an effect order, from
   which a linearization is built (or the given one is used in mode ``fixed``).
"""

from __future__ import annotations

from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities
from harness.terms import refs, substitute, to_value


@register
class GroupDownsetSolver(Solver):
    name = "fable51_1-br-groupdp"
    description = "Exact Poss by memoised DP over downsets of the effect-order poset, per dependency-connected block group, with witnesses"
    capabilities = SolverCapabilities(
        rcw=True,
        sync=False,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        return _Engine(setup, linearization).run()


class _Group:
    """Search context of one block group."""

    __slots__ = ("S", "smask", "parent", "rv_by_id")

    def __init__(self, S: list[int], smask: int, rv_by_id: dict[str, int]) -> None:
        self.S = S  # local index -> global action index
        self.smask = smask  # global bitmask of S
        self.parent: dict = {}  # state -> (previous state, local action) or None for the root
        self.rv_by_id = rv_by_id  # read id -> slot in the state's value tuple

    def path(self, st) -> list[int]:
        """Global action indices executed from the root to reach state ``st``."""
        out: list[int] = []
        while True:
            p = self.parent[st]
            if p is None:
                break
            st, k = p
            out.append(self.S[k])
        out.reverse()
        return out


class _Engine:
    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.lin = lin
        self.mode = "all" if lin is None else "fixed"
        acts = list(setup.actions.values())
        self.acts = acts
        n = len(acts)
        self.n = n
        self.gidx = {a.id: i for i, a in enumerate(acts)}
        abid = setup.actions

        # ---- the poset Q of forced effect-order relations (global bitmasks) ----
        pred = [0] * n
        if lin is None:
            for i, a in enumerate(acts):
                m = 0
                for j, b in enumerate(acts):
                    if j != i and b.thread == a.thread and b.done < a.start:
                        m |= 1 << j
                pred[i] = m
        else:
            poset = setup.poset
            pos = poset.positions(lin)
            sp = [pos[poset.start_node[a.id]] for a in acts]
            dp = [pos[poset.done_node[a.id]] for a in acts]
            for i in range(n):
                m = 0
                si = sp[i]
                for j in range(n):
                    if j != i and dp[j] < si:
                        m |= 1 << j
                pred[i] = m
        succ = [0] * n
        for i in range(n):
            pm = pred[i]
            j = 0
            while pm:
                if pm & 1:
                    succ[j] |= 1 << i
                pm >>= 1
                j += 1
        self.pred = pred
        self.succ = succ

        # ---- data dependencies ----
        deps_memo: dict[str, set[str]] = {}

        def deps_expr(expr) -> set[str]:
            out: set[str] = set()
            if expr is None:
                return out
            for x in refs(expr):
                ax = abid[x]
                if ax.kind == "read":
                    out.add(x)
                else:
                    out |= deps_data(x)
            return out

        def deps_data(x: str) -> set[str]:
            r = deps_memo.get(x)
            if r is None:
                r = deps_expr(abid[x].data)
                deps_memo[x] = r
            return r

        self.static_data: dict[str, object] = {}  # writer id -> content, when read-independent
        self.static_expect: dict[str, object] = {}  # rcw id -> expected term, when read-independent
        all_deps: dict[str, set[str]] = {}
        for a in acts:
            if a.kind == "read":
                continue
            dd = deps_data(a.id)
            if not dd:
                self.static_data[a.id] = setup.static_content(a.id)
            de: set[str] = set()
            if a.kind == "rcw":
                de = deps_expr(a.expect)
                if not de:
                    self.static_expect[a.id] = substitute(a.expect, setup.static_content)
            all_deps[a.id] = dd | de

        consumers = [0] * n  # read -> global mask of writers whose data/expect depend on it
        for a in acts:
            if a.kind == "read":
                continue
            for r in all_deps[a.id]:
                consumers[self.gidx[r]] |= 1 << self.gidx[a.id]
        self.consumers = consumers
        self.referenced = {i for i in range(n) if consumers[i]}

        # ---- block groups (union-find) ----
        nb = setup.blocks
        uf = list(range(nb))

        def find(x: int) -> int:
            while uf[x] != x:
                uf[x] = uf[uf[x]]
                x = uf[x]
            return x

        for a in acts:
            if a.kind == "read":
                continue
            for r in all_deps[a.id]:
                x, y = find(a.block), find(abid[r].block)
                if x != y:
                    uf[x] = y
        comps: dict[int, list[int]] = {}
        for b in range(nb):
            comps.setdefault(find(b), []).append(b)
        self.groups = list(comps.values())

        # ---- term interning ----
        self.tid: dict = {}
        self.tlist: list = []

        # ---- records: value id -> first seed ----
        self.res: dict[str, dict] = {a.id: {} for a in acts if a.returns}
        self.fin: dict[int, dict] = {b: {} for b in range(nb)}

    # ------------------------------------------------------------------ helpers

    def _intern(self, t) -> int:
        k = self.tid.get(t)
        if k is None:
            k = len(self.tlist)
            self.tid[t] = k
            self.tlist.append(t)
        return k

    def _rec_result(self, aid: str, tid: int, seed) -> None:
        d = self.res[aid]
        if tid not in d:
            d[tid] = seed

    def _rec_final(self, b: int, tid: int, seed) -> None:
        d = self.fin[b]
        if tid not in d:
            d[tid] = seed

    def _value_fn(self, grp: _Group, vals):
        tl = self.tlist
        sd = self.static_data
        abid = self.setup.actions
        rv = grp.rv_by_id

        def val(x: str):
            t = sd.get(x)
            if t is not None:
                return t
            ax = abid[x]
            if ax.kind == "read":
                return tl[vals[rv[x]]]
            return substitute(ax.data, val)

        return val

    # ------------------------------------------------------------------ search

    def _run_group(self, blocks: list[int]) -> None:
        acts = self.acts
        setup = self.setup
        pred = self.pred
        succ = self.succ
        referenced = self.referenced
        intern = self._intern
        rec_result = self._rec_result
        rec_final = self._rec_final
        static_data = self.static_data
        static_expect = self.static_expect

        bset = set(blocks)
        S = [i for i, a in enumerate(acts) if a.block in bset and (a.kind != "read" or i in referenced)]
        m = len(S)
        smask = 0
        for g in S:
            smask |= 1 << g

        def tolocal(gm: int) -> int:
            x = 0
            for k, g in enumerate(S):
                if gm >> g & 1:
                    x |= 1 << k
            return x

        lpred = [tolocal(pred[g]) for g in S]
        nb = len(blocks)
        bl = {b: k for k, b in enumerate(blocks)}
        lblock = [bl[acts[g].block] for g in S]
        kinds = [acts[g].kind for g in S]
        ids = [acts[g].id for g in S]
        touch = [0] * nb
        writers = [0] * nb
        for k in range(m):
            touch[lblock[k]] |= 1 << k
            if kinds[k] != "read":
                writers[lblock[k]] |= 1 << k
        slot = [-1] * m
        cons: list[int] = []
        rv_by_id: dict[str, int] = {}
        for k, g in enumerate(S):
            if kinds[k] == "read":
                slot[k] = len(cons)
                rv_by_id[ids[k]] = len(cons)
                cons.append(tolocal(self.consumers[g]))
        nslots = len(cons)

        dropped: list[tuple[str, int, int, int]] = []  # (id, local block, lpred, lsucc)
        dropped_on: list[list[tuple[str, int]]] = [[] for _ in range(nb)]
        for i, a in enumerate(acts):
            if a.kind == "read" and a.block in bset and i not in referenced:
                lb = bl[a.block]
                lp = tolocal(pred[i])
                ls = tolocal(succ[i])
                dropped.append((a.id, lb, lp, ls))
                dropped_on[lb].append((a.id, ls))

        grp = _Group(S, smask, rv_by_id)
        parent = grp.parent

        # root state
        init_c = [intern(setup.init[b]) for b in blocks]
        contents0 = list(init_c)
        for k in range(nb):
            if touch[k] == 0:
                contents0[k] = None
        root = (0, tuple(contents0), (None,) * nslots)
        parent[root] = None
        for k, b in enumerate(blocks):
            if writers[k] == 0:
                rec_final(b, init_c[k], (grp, root, None, None))
            if touch[k] == 0:
                for rid, _ls in dropped_on[k]:
                    rec_result(rid, init_c[k], (grp, root, None, rid))

        avail_memo: dict[int, list[int]] = {}
        elig_memo: dict[int, list[tuple[str, int]]] = {}
        dead_memo: dict[int, list[int]] = {}

        def avail(mask: int) -> list[int]:
            r = avail_memo.get(mask)
            if r is None:
                r = [k for k in range(m) if not mask >> k & 1 and lpred[k] & mask == lpred[k]]
                avail_memo[mask] = r
            return r

        def elig(mask: int) -> list[tuple[str, int]]:
            r = elig_memo.get(mask)
            if r is None:
                r = [
                    (rid, lb)
                    for rid, lb, lp, ls in dropped
                    if ls & mask == 0 and (lp & mask == lp or writers[lb] & mask == writers[lb])
                ]
                elig_memo[mask] = r
            return r

        def dead(mask: int) -> list[int]:
            r = dead_memo.get(mask)
            if r is None:
                r = [j for j in range(nslots) if cons[j] & mask == cons[j]]
                dead_memo[mask] = r
            return r

        sd_id: dict[int, int] = {}  # local writer -> interned static content
        se_id: dict[int, int] = {}  # local rcw -> interned static expected value
        for k in range(m):
            if kinds[k] != "read":
                t = static_data.get(ids[k])
                if t is not None:
                    sd_id[k] = intern(t)
                if kinds[k] == "rcw":
                    t = static_expect.get(ids[k])
                    if t is not None:
                        se_id[k] = intern(t)

        def content_of(k: int, vals) -> int:
            c = sd_id.get(k)
            if c is None:
                c = intern(substitute(acts[S[k]].data, self._value_fn(grp, vals)))
            return c

        def expect_of(k: int, vals) -> int:
            c = se_id.get(k)
            if c is None:
                c = intern(substitute(acts[S[k]].expect, self._value_fn(grp, vals)))
            return c

        # root records for insertable unreferenced reads
        for rid, lb in elig(0):
            c = contents0[lb]
            if c is not None:
                rec_result(rid, c, (grp, root, None, rid))

        stack = [root]
        while stack:
            st = stack.pop()
            mask, contents, vals = st
            for k in avail(mask):
                lb = lblock[k]
                kind = kinds[k]
                old = contents[lb]
                nmask = mask | (1 << k)
                nvals = vals
                nc = contents
                if kind == "read":
                    rec_result(ids[k], old, (grp, st, k, None))
                    lst = list(vals)
                    lst[slot[k]] = old
                    nvals = tuple(lst)
                else:
                    if kind == "write":
                        newc = content_of(k, vals)
                    else:
                        rec_result(ids[k], old, (grp, st, k, None))
                        newc = content_of(k, vals) if expect_of(k, vals) == old else old
                    if newc != old:
                        lst = list(contents)
                        lst[lb] = newc
                        nc = tuple(lst)
                    if writers[lb] & nmask == writers[lb]:
                        rec_final(blocks[lb], newc, (grp, st, k, None))
                if touch[lb] & nmask == touch[lb]:
                    # nobody in the search looks at this block any more
                    c = nc[lb]
                    for rid, ls in dropped_on[lb]:
                        if ls & nmask == 0:
                            rec_result(rid, c, (grp, st, k, rid))
                    lst = list(nc)
                    lst[lb] = None
                    nc = tuple(lst)
                dl = dead(nmask)
                if dl:
                    for j in dl:
                        if nvals[j] is not None:
                            lst = list(nvals)
                            for j2 in dl:
                                lst[j2] = None
                            nvals = tuple(lst)
                            break
                nst = (nmask, nc, nvals)
                if nst not in parent:
                    parent[nst] = (st, k)
                    stack.append(nst)
                    for rid, lb2 in elig(nmask):
                        c = nc[lb2]
                        if c is not None:
                            rec_result(rid, c, (grp, st, k, rid))

    # ------------------------------------------------------------------ witnesses

    def _complete(self, F: list[int], smask: int, r: int | None) -> list[int] | None:
        """A linear extension of Q whose restriction to the group starts with ``F``.

        The action ``r`` (an unreferenced read), if given, is placed at the first point
        after ``F`` where all its predecessors are done.
        """
        n = self.n
        pred = self.pred
        executed = 0
        E: list[int] = []
        ptr = 0
        placed = r is None
        while len(E) < n:
            pick = -1
            if ptr < len(F):
                x = F[ptr]
                if pred[x] & executed == pred[x] and not executed >> x & 1:
                    pick = x
                    ptr += 1
                else:
                    for y in range(n):
                        if not executed >> y & 1 and not smask >> y & 1 and y != r and pred[y] & executed == pred[y]:
                            pick = y
                            break
            elif not placed and pred[r] & executed == pred[r]:
                pick = r
            else:
                for y in range(n):
                    if not executed >> y & 1 and (placed or y != r) and pred[y] & executed == pred[y]:
                        pick = y
                        break
            if pick < 0:
                return None
            if pick == r:
                placed = True
            E.append(pick)
            executed |= 1 << pick
        return E

    def _order(self, E: list[int]) -> tuple[int, ...]:
        """A linearization of the trace poset under which ``E`` is an effect order."""
        poset = self.setup.poset
        chains = poset.chains
        chain_of = poset.chain_of
        pos_in_chain = poset.pos_in_chain
        ptr = [0] * len(chains)
        L: list[int] = []
        for g in E:
            sn = poset.start_node[self.acts[g].id]
            ci = chain_of[sn]
            p = pos_in_chain[sn]
            c = chains[ci]
            while ptr[ci] <= p:
                L.append(c[ptr[ci]])
                ptr[ci] += 1
        for ci, c in enumerate(chains):
            while ptr[ci] < len(c):
                L.append(c[ptr[ci]])
                ptr[ci] += 1
        return tuple(L)

    def _execute(self, E: list[int]):
        setup = self.setup
        acts = self.acts
        abid = setup.actions
        sd = self.static_data
        se = self.static_expect
        contents = list(setup.init)
        rvals: dict[str, object] = {}
        results: dict[str, object] = {}

        def val(x: str):
            t = sd.get(x)
            if t is not None:
                return t
            ax = abid[x]
            if ax.kind == "read":
                return rvals[x]
            return substitute(ax.data, val)

        for g in E:
            a = acts[g]
            b = a.block
            old = contents[b]
            if a.kind == "read":
                results[a.id] = old
                rvals[a.id] = old
            elif a.kind == "write":
                contents[b] = val(a.id)
            else:
                results[a.id] = old
                exp = se.get(a.id)
                if exp is None:
                    exp = substitute(a.expect, val)
                if exp == old:
                    contents[b] = val(a.id)
        return results, contents

    def _witness(self, seed, certifies: dict, check) -> Schedule | None:
        grp, st, k, rid = seed
        F = grp.path(st)
        if k is not None:
            F.append(grp.S[k])
        r = None if rid is None else self.gidx[rid]
        E = self._complete(F, grp.smask, r)
        if E is None:
            return None
        results, final = self._execute(E)
        what, key, term = check
        if what == "id":
            if results.get(key) != term:
                return None
        elif final[key] != term:
            return None
        order = tuple(self.lin) if self.lin is not None else self._order(E)
        effects = [self.acts[g].id for g in E]
        return Schedule(order, effects, results, list(final), True, {"certifies": certifies})

    # ------------------------------------------------------------------ driver

    def run(self) -> Outcomes:
        for blocks in self.groups:
            self._run_group(blocks)
        tl = self.tlist
        results = {aid: {tl[t] for t in d} for aid, d in self.res.items()}
        final = {b: {tl[t] for t in d} for b, d in self.fin.items()}
        witnesses: list[Schedule] = []
        for aid, d in self.res.items():
            for t, seed in d.items():
                term = tl[t]
                w = self._witness(seed, {"id": aid, "value": to_value(term)}, ("id", aid, term))
                if w is not None:
                    witnesses.append(w)
        for b, d in self.fin.items():
            for t, seed in d.items():
                term = tl[t]
                w = self._witness(seed, {"block": b, "value": to_value(term)}, ("block", b, term))
                if w is not None:
                    witnesses.append(w)
        return Outcomes(self.mode, True, results, final, witnesses)
