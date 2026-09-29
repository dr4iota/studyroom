"""Exact possibility-set solver for case ``sor`` (spec v2), modes ``all`` and ``fixed``.

Reduction (own derivation, see SOURCES.md).  Let ``Q`` be the *effect poset* on actions:

    a <Q b   iff   end(a) precedes start(b)

in the trace poset ``P`` (mode ``all``) or in the given linearization ``L`` (mode
``fixed``).  Then the effect orders realised by full schedules are exactly the linear
extensions of ``Q``:

* a full schedule ``(L, pi)`` has ``pi(a) <= pos(end(a)) < pos(start(b)) <= pi(b)``
  whenever ``end(a)`` precedes ``start(b)`` in ``L`` (and ``P``'s order is contained in
  ``L``'s), so its effect order extends ``Q``;
* conversely, for a linear extension ``sigma`` of ``Q``, the poset ``P`` plus one effect
  node ``eff(a)`` per action (``start(a) < eff(a) < end(a)``) plus the chain
  ``eff(sigma_1) < eff(sigma_2) < ...`` is acyclic (any path between effect nodes that
  avoids chain edges goes ``eff(a) -> end(a) -> ... -> start(b) -> eff(b)``, i.e.
  ``a <Q b``, so it follows ``sigma`` too), and any topological order of it yields a
  linearization ``L`` of ``P`` with effect points inside the intervals, in the order
  ``sigma``.

So ``Poss`` over all full schedules is ``Poss`` over all linear extensions of ``Q``, and
these are enumerated by a memoised depth-first search over the downsets of ``Q`` (the
sets of actions already effected).  The search state also carries the block contents
and the results of reads that a not-yet-effected write/RCW still references.  A
transition whose read/RCW result contradicts its observation is dropped; a read value
or final content is recorded only when the transition leads to a state from which the
run can be completed.  Witnesses are built from the DFS path plus a memoised
completion of the target state.
"""

from __future__ import annotations

import sys

from harness import terms as T
from harness.model import Setup
from harness.poset import Linearization, TracePoset
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities

DONTCARE = -1  # block content id when no pending read/RCW and a pending plain write


@register
class DownsetSolver(Solver):
    name = "fable51_1-sor-downset"
    description = (
        "Memoised DFS over downsets of the effect poset (a<b iff end(a) precedes start(b)); "
        "exact sets, consistency, witnesses; modes all and fixed"
    )
    capabilities = SolverCapabilities(
        rcw=True,
        sync=True,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        return _Search(setup, linearization).run()


def _reachability(poset: TracePoset) -> list[int]:
    """``reach[x]``: bitmask of the nodes strictly after ``x`` in the poset order."""
    n = len(poset)
    reach = [0] * n
    succs = poset.succs
    for x in reversed(poset.topological_order()):
        m = 0
        for y in succs[x]:
            m |= (1 << y) | reach[y]
        reach[x] = m
    return reach


class _Search:
    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.lin = None if lin is None else tuple(lin)
        self.mode = "all" if lin is None else "fixed"
        acts = list(setup.actions.values())
        self.acts = acts
        n = len(acts)
        self.n = n
        self.ids = [a.id for a in acts]
        index = {a.id: i for i, a in enumerate(acts)}
        self.index = index
        self.kind = [a.kind for a in acts]
        self.block = [a.block for a in acts]
        M = setup.blocks
        self.M = M
        self.full = (1 << n) - 1

        # ------------------------------------------------------------ effect poset Q
        poset = setup.poset
        starts = [poset.start_node[a.id] for a in acts]
        dones = [poset.done_node[a.id] for a in acts]
        qsucc = [0] * n
        if self.lin is None:
            reach = _reachability(poset)
            for i in range(n):
                r = reach[dones[i]]
                m = 0
                for j in range(n):
                    if (r >> starts[j]) & 1:
                        m |= 1 << j
                qsucc[i] = m
        else:
            pos = poset.positions(self.lin)
            for i in range(n):
                pe = pos[dones[i]]
                m = 0
                for j in range(n):
                    if pe < pos[starts[j]]:
                        m |= 1 << j
                qsucc[i] = m
        predmask = [0] * n  # all Q-predecessors of each action
        for i in range(n):
            m = qsucc[i]
            while m:
                low = m & -m
                predmask[low.bit_length() - 1] |= 1 << i
                m ^= low
        cover = [0] * n  # covering successors (transitive reduction of Q)
        for i in range(n):
            m = qsucc[i]
            via = 0
            mm = m
            while mm:
                low = mm & -mm
                via |= qsucc[low.bit_length() - 1]
                mm ^= low
            cover[i] = m & ~via
        self.predmask = predmask
        self.cover = cover

        # ------------------------------------------------------------ terms
        self.terms: list[T.Term] = []
        self.tid: dict[T.Term, int] = {}

        # ------------------------------------------------------------ expressions
        # Flatten every writer's data (and RCW expect) so that its only references are
        # to reads; a referenced writer is replaced by its own flattened data (its
        # content), an unknown writer by its Unk symbol.
        flat_cache: dict[str, T.Node] = {}

        def flatten(aid: str) -> T.Node:
            t = flat_cache.get(aid)
            if t is None:
                a = setup.actions[aid]
                t = T.Unk(aid) if a.data is None else T.substitute(a.data, lookup)
                flat_cache[aid] = t
            return t

        def lookup(x: str) -> T.Node:
            return T.Ref(x) if setup.actions[x].kind == "read" else flatten(x)

        self.content_expr: list[T.Node | None] = [None] * n
        self.expect_expr: list[T.Node | None] = [None] * n
        self.content_static: list[int | None] = [None] * n
        self.expect_static: list[int | None] = [None] * n
        self.slot_of = [-1] * n  # read -> env slot, or -1
        self.depmask = [0] * n  # read -> writers (transitively) referencing it
        self.refreads: list[list[int]] = [[] for _ in range(n)]  # writer -> read indices
        nslots = 0
        for i, a in enumerate(acts):
            if a.kind == "read":
                continue
            ce = flatten(a.id)
            self.content_expr[i] = ce
            rs = set(T.refs(ce))
            if not rs:
                self.content_static[i] = self.intern(ce)
            if a.kind == "rcw":
                ee = T.substitute(a.expect, lookup)
                self.expect_expr[i] = ee
                ers = T.refs(ee)
                if not ers:
                    self.expect_static[i] = self.intern(ee)
                rs |= ers
            for rid in sorted(rs):
                j = index[rid]
                if self.slot_of[j] < 0:
                    self.slot_of[j] = nslots
                    nslots += 1
                self.depmask[j] |= 1 << i
                self.refreads[i].append(j)
        self.nslots = nslots

        # ------------------------------------------------------------ observations
        self.obs: list[int | None] = [None] * n
        self.obs_flag: list[str | None] = [None] * n
        for i, a in enumerate(acts):
            if a.observed is None:
                continue
            if isinstance(a.observed, str):
                self.obs_flag[i] = a.observed  # "ok"/"fail" (rcw_result: flag)
            else:
                self.obs[i] = self.intern(a.observed)

        # ------------------------------------------------------------ block masks
        self.readmask = [0] * M  # reads and RCWs per block
        self.writemask = [0] * M  # plain writes per block
        for i, a in enumerate(acts):
            if a.kind == "write":
                self.writemask[a.block] |= 1 << i
            else:
                self.readmask[a.block] |= 1 << i

        # ------------------------------------------------------------ initial state
        blocks = []
        for b in range(M):
            if self.readmask[b] == 0 and self.writemask[b] != 0:
                blocks.append(DONTCARE)
            else:
                blocks.append(self.intern(setup.init[b]))
        self.init_state = (0,) + tuple(blocks) + (-1,) * nslots

    # ---------------------------------------------------------------- helpers

    def intern(self, t: T.Term) -> int:
        v = self.tid.get(t)
        if v is None:
            v = len(self.terms)
            self.terms.append(t)
            self.tid[t] = v
        return v

    def _eval(self, expr: T.Node, st: tuple) -> int:
        base = 1 + self.M
        terms = self.terms
        slot_of = self.slot_of
        index = self.index

        def look(x: str) -> T.Term:
            return terms[st[base + slot_of[index[x]]]]

        return self.intern(T.substitute(expr, look))

    def step(self, st: tuple, a: int):
        """Effect action ``a`` in state ``st``: ``(new_state, result_id | None)`` or None."""
        b = self.block[a]
        cur = st[1 + b]
        kind = self.kind[a]
        newE = st[0] | (1 << a)
        lst = list(st)
        lst[0] = newE
        M = self.M
        value = None
        if kind == "read":
            value = cur
            o = self.obs[a]
            if o is not None and o != value:
                return None
            s = self.slot_of[a]
            if s >= 0:
                lst[1 + M + s] = value
            newc = cur
        elif kind == "write":
            c = self.content_static[a]
            newc = c if c is not None else self._eval(self.content_expr[a], st)
        else:  # rcw
            value = cur
            o = self.obs[a]
            if o is not None and o != value:
                return None
            e = self.expect_static[a]
            if e is None:
                e = self._eval(self.expect_expr[a], st)
            ok = e == cur
            flag = self.obs_flag[a]
            if flag is not None and ok != (flag == "ok"):
                return None
            if ok:
                c = self.content_static[a]
                newc = c if c is not None else self._eval(self.content_expr[a], st)
            else:
                newc = cur
        if (self.readmask[b] & ~newE) == 0 and (self.writemask[b] & ~newE) != 0:
            newc = DONTCARE
        lst[1 + b] = newc
        for r in self.refreads[a]:
            if (self.depmask[r] & ~newE) == 0:
                lst[1 + M + self.slot_of[r]] = -1
        return tuple(lst), value

    # ---------------------------------------------------------------- search

    def run(self) -> Outcomes:
        n = self.n
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * n + 2000))
        self.memo: dict[tuple, bool] = {}
        self.nxt: dict[tuple, tuple | None] = {}
        self.path: list[int] = []
        self.results: list[set[int]] = [set() for _ in range(n)]
        self.final: list[set[int]] = [set() for _ in range(self.M)]
        self.witnesses: list[Schedule] = []
        enabled = 0
        for i in range(n):
            if self.predmask[i] == 0:
                enabled |= 1 << i
        good = self.visit(self.init_state, enabled)
        if not good:
            return Outcomes(self.mode, False)
        terms = self.terms
        results = {
            self.ids[i]: {terms[v] for v in self.results[i]}
            for i in range(n)
            if self.kind[i] != "write"
        }
        final = {b: {terms[v] for v in self.final[b]} for b in range(self.M)}
        return Outcomes(self.mode, True, results, final, self.witnesses)

    def visit(self, st: tuple, enabled: int) -> bool:
        memo = self.memo
        cached = memo.get(st)
        if cached is not None:
            return cached
        if st[0] == self.full:
            memo[st] = True
            self.nxt[st] = None
            terms = self.terms
            for b in range(self.M):
                v = st[1 + b]
                fs = self.final[b]
                if v not in fs:
                    fs.add(v)
                    self.add_witness(list(self.path), {"block": b, "value": T.to_value(terms[v])})
            return True
        good = False
        predmask = self.predmask
        cover = self.cover
        step = self.step
        path = self.path
        m = enabled
        while m:
            low = m & -m
            a = low.bit_length() - 1
            m ^= low
            res = step(st, a)
            if res is None:
                continue
            ns, value = res
            newE = ns[0]
            ne = enabled ^ low
            c = cover[a]
            while c:
                cl = c & -c
                c ^= cl
                pm = predmask[cl.bit_length() - 1]
                if (pm & newE) == pm:
                    ne |= cl
            path.append(a)
            g = self.visit(ns, ne)
            path.pop()
            if g:
                if not good:
                    good = True
                    self.nxt[st] = (a, ns)
                if value is not None:
                    vals = self.results[a]
                    if value not in vals:
                        vals.add(value)
                        self.add_witness(
                            path + [a] + self.completion(ns),
                            {"id": self.ids[a], "value": T.to_value(self.terms[value])},
                        )
        memo[st] = good
        return good

    def completion(self, s: tuple) -> list[int]:
        out = []
        nxt = self.nxt
        p = nxt[s]
        while p is not None:
            out.append(p[0])
            p = nxt[p[1]]
        return out

    # ---------------------------------------------------------------- witnesses

    def _execute(self, effects: list[int]):
        """Run the spec's block semantics along an effect order (independent of the DP)."""
        setup = self.setup
        acts = self.acts
        contents = list(setup.init)
        env: dict[str, T.Term] = {}

        def value_of(x: str) -> T.Term:
            v = env.get(x)
            if v is None:
                a = setup.actions[x]
                v = T.Unk(x) if a.data is None else T.substitute(a.data, value_of)
                env[x] = v
            return v

        results: dict[str, T.Term] = {}
        for i in effects:
            a = acts[i]
            b = a.block
            if a.kind == "read":
                results[a.id] = contents[b]
                env[a.id] = contents[b]
            elif a.kind == "write":
                contents[b] = value_of(a.id)
            else:
                old = contents[b]
                results[a.id] = old
                if T.substitute(a.expect, value_of) == old:
                    contents[b] = value_of(a.id)
        return results, contents

    def _order_for(self, effects: list[int]) -> Linearization:
        """A linearization of P admitting effect points in the order ``effects``."""
        poset = self.setup.poset
        n = len(poset)
        k = len(effects)
        succ = [list(s) for s in poset.succs] + [[] for _ in range(k)]
        indeg = [len(p) for p in poset.preds] + [0] * k
        prev = -1
        for j, i in enumerate(effects):
            e = n + j
            aid = self.ids[i]
            s, d = poset.start_node[aid], poset.done_node[aid]
            succ[s].append(e)
            indeg[e] += 1
            succ[e].append(d)
            indeg[d] += 1
            if prev >= 0:
                succ[prev].append(e)
                indeg[e] += 1
            prev = e
        ready = [x for x in range(n + k) if indeg[x] == 0]
        out = []
        while ready:
            x = ready.pop()
            if x < n:
                out.append(x)
            for y in succ[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    ready.append(y)
        return tuple(out)

    def add_witness(self, effects: list[int], certifies: dict) -> None:
        results, final = self._execute(effects)
        order = self.lin if self.lin is not None else self._order_for(effects)
        self.witnesses.append(
            Schedule(order, [self.ids[i] for i in effects], results, final, True, {"certifies": certifies})
        )
