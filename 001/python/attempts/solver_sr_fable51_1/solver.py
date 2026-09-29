"""Exact ``Poss`` sets for case ``sr`` (sync points and RCWs, no observations).

Method (own derivation; see SOURCES.md).

1.  **Precedence order on actions.** Fix a linearization ``L``.  An effect order
    ``s_1 < ... < s_n`` is realised by some ``pi`` (distinct effect points inside the
    intervals) iff for every ``i < j``, ``end(s_j)`` is not before ``start(s_i)`` in ``L``
    (greedy placement shows sufficiency).  Over all ``L`` in ``Lin(P)``: the effect order
    is realised by some ``(L, pi)`` iff for every ``i < j``, ``end(s_j)`` does not precede
    ``start(s_i)`` in the poset ``P``.  Necessity is immediate; sufficiency: add the edges
    ``start(s_i) -> end(s_j)`` (``i < j``) to ``P``; a cycle would need a chain
    ``end(s_j1) <=_P start(s_i2)``, ``i2 < j2``, ``end(s_j2) <=_P start(s_i3)``, ...,
    which the pairwise condition forbids, so the augmented graph is acyclic, any
    topological order is an ``L`` realising the effect order.

    Hence, with ``a < b  iff  end(a) <_P start(b)`` (a strict partial order, transitive
    because ``start(x) <_P end(x)``), the realisable effect orders are exactly the linear
    extensions of ``<``.  In mode ``fixed`` the same holds with ``<_L``.

2.  **Search.**  Linear extensions are enumerated as paths through downsets of ``<``,
    memoised on ``(downset, block contents, live read results)``.  Every reachable state
    is a prefix of a full schedule, so every value seen is possible, and every possible
    value is seen.

3.  **Decomposition.**  Blocks are grouped by data dependency (a write or RCW on block
    ``b`` referring to a read of block ``b'``).  The projection of a linear extension
    onto a subset is a linear extension of the restriction, and conversely every linear
    extension of a restriction extends to the whole order, so each group is solved on
    its own actions.  Reads that nothing refers to are not enumerated: their value at
    every state where they can be inserted (all predecessors in, no successor in) is
    the content of their block there.

Witnesses: for every new value a prefix is completed to a full effect order (Kahn's
algorithm on ``<`` plus the prefix chain), re-executed, and, in mode ``all``, turned
into a linearization by placing the down-closure of each start in effect order.
"""

from __future__ import annotations

import heapq
from bisect import bisect_right

from harness import terms as T
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities

READ, WRITE, RCW = 0, 1, 2
_KIND = {"read": READ, "write": WRITE, "rcw": RCW}


def _bits(m: int):
    """Indices of the set bits of ``m``, ascending."""
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


class _Context:
    """Setup-wide data: precedence masks, flattened expressions, term interning."""

    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.lin = None if lin is None else tuple(lin)
        self.P = setup.poset
        self.acts = list(setup.actions.values())
        self.n = n = len(self.acts)
        self.ids = [a.id for a in self.acts]
        self.gidx = {a.id: i for i, a in enumerate(self.acts)}
        self.kind = [_KIND[a.kind] for a in self.acts]
        self.block = [a.block for a in self.acts]
        self.pred = self._precedence()  # pred[i]: mask of j with j < i (end(j) before start(i))
        self.succ = [0] * n
        for j in range(n):
            for i in _bits(self.pred[j]):
                self.succ[i] |= 1 << j
        self.flat_data: dict[str, T.Node] = {}  # write/rcw id -> data with only read refs
        self.flat_expect: dict[str, T.Node] = {}  # rcw id -> expect with only read refs
        self.read_refs: dict[str, set[str]] = {}  # action id -> reads its content/expect uses
        self._flatten()
        self.term_id: dict[T.Term, int] = {}
        self.terms: list[T.Term] = []

    # ------------------------------------------------------------------ terms

    def intern(self, t: T.Term) -> int:
        i = self.term_id.get(t)
        if i is None:
            i = len(self.terms)
            self.term_id[t] = i
            self.terms.append(t)
        return i

    # ------------------------------------------------------------------ precedence

    def _precedence(self) -> list[int]:
        P, n = self.P, self.n
        pred = [0] * n
        if self.lin is None:
            # reach[v]: mask of actions whose start node is reachable from v (strictly after).
            reach = [0] * len(P)
            for v in reversed(P.topological_order()):
                m = 0
                for s in P.succs[v]:
                    m |= reach[s]
                    if P.kind[s] == "start":
                        m |= 1 << self.gidx[P.action[s]]
                reach[v] = m
            for j, a in enumerate(self.acts):
                bit = 1 << j
                for i in _bits(reach[P.done_node[a.id]]):
                    pred[i] |= bit
        else:
            pos = P.positions(self.lin)
            order = sorted(range(n), key=lambda i: pos[P.start_node[self.ids[i]]])
            starts = [pos[P.start_node[self.ids[i]]] for i in order]
            for j, a in enumerate(self.acts):
                e = pos[P.done_node[a.id]]
                bit = 1 << j
                for k in range(bisect_right(starts, e), n):
                    pred[order[k]] |= bit
        return pred

    # ------------------------------------------------------------------ expressions

    def _flatten(self) -> None:
        """Inline references to writes/RCWs so that only read references remain."""
        acts = self.setup.actions
        fd = self.flat_data

        def look(x: str) -> T.Node:
            return T.Ref(x) if acts[x].kind == "read" else flat(x)

        def flat(aid: str) -> T.Node:
            t = fd.get(aid)
            if t is None:
                a = acts[aid]
                t = T.Unk(aid) if a.data is None else T.substitute(a.data, look)
                fd[aid] = t
            return t

        for a in self.acts:
            if a.kind == "read":
                self.read_refs[a.id] = set()
                continue
            rr = set(T.refs(flat(a.id)))
            if a.kind == "rcw":
                e = T.substitute(a.expect, look)
                self.flat_expect[a.id] = e
                rr |= T.refs(e)
            self.read_refs[a.id] = rr

    # ------------------------------------------------------------------ components

    def components(self) -> list[list[int]]:
        """Blocks grouped by data dependency, each group sorted, groups sorted."""
        par = list(range(self.setup.blocks))

        def find(x: int) -> int:
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        for g in range(self.n):
            if self.kind[g] != READ:
                for r in self.read_refs[self.ids[g]]:
                    a, b = find(self.block[g]), find(self.block[self.gidx[r]])
                    if a != b:
                        par[a] = b
        groups: dict[int, list[int]] = {}
        for b in range(self.setup.blocks):
            groups.setdefault(find(b), []).append(b)
        return sorted(groups.values())

    # ------------------------------------------------------------------ witnesses

    def witness(self, prefix: list[int], certifies: dict) -> Schedule:
        """A full schedule whose effect order starts with ``prefix`` (global indices)."""
        sigma = self._complete(prefix)
        ids = [self.ids[g] for g in sigma]
        results, final = self.execute(ids)
        order = self.lin if self.lin is not None else self._linearize(ids)
        return Schedule(order, ids, results, final, True, {"certifies": certifies})

    def _complete(self, prefix: list[int]) -> list[int]:
        """Topological order of ``<`` plus the chain ``prefix``, keeping prefix first."""
        n, pred, succ = self.n, self.pred, self.succ
        rank = list(range(n, 2 * n))
        for k, g in enumerate(prefix):
            rank[g] = k
        indeg = [bin(pred[g]).count("1") for g in range(n)]
        chain = [-1] * n
        for k in range(1, len(prefix)):
            u, v = prefix[k - 1], prefix[k]
            if not (pred[v] >> u) & 1:
                chain[u] = v
                indeg[v] += 1
        heap = [(rank[g], g) for g in range(n) if indeg[g] == 0]
        heapq.heapify(heap)
        out: list[int] = []
        while heap:
            _, u = heapq.heappop(heap)
            out.append(u)
            v = chain[u]
            if v >= 0:
                indeg[v] -= 1
                if indeg[v] == 0:
                    heapq.heappush(heap, (rank[v], v))
            for v in _bits(succ[u]):
                indeg[v] -= 1
                if indeg[v] == 0:
                    heapq.heappush(heap, (rank[v], v))
        if len(out) != n:
            raise RuntimeError("witness completion failed (precedence cycle)")
        return out

    def execute(self, ids: list[str]) -> tuple[dict[str, T.Term], list[T.Term]]:
        """Atomic block semantics along the effect order ``ids``."""
        acts = self.setup.actions
        contents = list(self.setup.init)
        results: dict[str, T.Term] = {}
        rv: dict[str, T.Term] = {}
        look = rv.__getitem__
        fd, fe = self.flat_data, self.flat_expect
        for aid in ids:
            a = acts[aid]
            if a.kind == "read":
                v = contents[a.block]
                results[aid] = v
                rv[aid] = v
            elif a.kind == "write":
                contents[a.block] = T.substitute(fd[aid], look)
            else:
                old = contents[a.block]
                results[aid] = old
                if old == T.substitute(fe[aid], look):
                    contents[a.block] = T.substitute(fd[aid], look)
        return results, contents

    def _linearize(self, ids: list[str]) -> tuple[int, ...]:
        """A linearization of ``P`` in which the effect order ``ids`` can be realised.

        Place the down-closure of ``start(a)`` for each ``a`` in effect order, then the
        rest.  Since ``ids`` is a linear extension of ``<``, ``end(s_j)`` lies in the
        closure of ``start(s_k)`` only for ``k > j``, so every ``start(s_i)``, ``i < j``,
        is placed before ``end(s_j)``.
        """
        P = self.P
        preds = P.preds
        placed = [False] * len(P)
        out: list[int] = []

        def close(v: int) -> None:
            if placed[v]:
                return
            stack = [v]
            while stack:
                u = stack[-1]
                if placed[u]:
                    stack.pop()
                    continue
                todo = [p for p in preds[u] if not placed[p]]
                if todo:
                    stack.extend(todo)
                else:
                    placed[u] = True
                    out.append(u)
                    stack.pop()

        for aid in ids:
            close(P.start_node[aid])
        for v in range(len(P)):
            close(v)
        return tuple(out)


class _Component:
    """Search over one group of data-linked blocks."""

    def __init__(self, ctx: _Context, blocks: list[int]) -> None:
        self.ctx = ctx
        self.blocks = blocks
        bl = {b: k for k, b in enumerate(blocks)}
        acts = [g for g in range(ctx.n) if ctx.block[g] in bl]
        needed: set[int] = set()
        for g in acts:
            if ctx.kind[g] != READ:
                needed.update(ctx.gidx[r] for r in ctx.read_refs[ctx.ids[g]])
        self.active = active = [g for g in acts if ctx.kind[g] != READ or g in needed]
        na = len(active)
        loc = {g: i for i, g in enumerate(active)}

        def lmask(gm: int) -> int:
            m = 0
            for g2, i2 in loc.items():
                if (gm >> g2) & 1:
                    m |= 1 << i2
            return m

        self.pred = [lmask(ctx.pred[g]) for g in active]
        self.kind = [ctx.kind[g] for g in active]
        self.blk = [bl[ctx.block[g]] for g in active]
        # Passive reads: (global index, local block, active preds, active succs).
        self.passive = [
            (g, bl[ctx.block[g]], lmask(ctx.pred[g]), lmask(ctx.succ[g]))
            for g in acts
            if ctx.kind[g] == READ and g not in needed
        ]
        reads = [g for g in active if ctx.kind[g] == READ]
        self.nr = len(reads)
        self.rlid = rlid = {ctx.ids[g]: k for k, g in enumerate(reads)}  # read id -> slot
        self.rlocal = [rlid.get(ctx.ids[g], -1) for g in active]  # active index -> slot
        self.dep_mask = [0] * self.nr  # slot -> mask of active actions using the read
        self.resets = [[] for _ in active]  # active index -> slots it may retire
        self.cdata: list[int | None] = [None] * na
        self.fdata: list[T.Node | None] = [None] * na
        self.cexp: list[int | None] = [None] * na
        self.fexp: list[T.Node | None] = [None] * na
        for i, g in enumerate(active):
            if ctx.kind[g] == READ:
                continue
            aid = ctx.ids[g]
            for r in ctx.read_refs[aid]:
                k = rlid[r]
                self.dep_mask[k] |= 1 << i
                self.resets[i].append(k)
            d = ctx.flat_data[aid]
            if T.refs(d):
                self.fdata[i] = d
            else:
                self.cdata[i] = ctx.intern(d)
            if ctx.kind[g] == RCW:
                e = ctx.flat_expect[aid]
                if T.refs(e):
                    self.fexp[i] = e
                else:
                    self.cexp[i] = ctx.intern(e)

    def run(self, out: Outcomes) -> None:
        ctx = self.ctx
        terms, intern, ids, rlid = ctx.terms, ctx.intern, ctx.ids, self.rlid
        active = self.active
        na = len(active)
        full = (1 << na) - 1
        pred, kind, blk = self.pred, self.kind, self.blk
        cdata, fdata, cexp, fexp = self.cdata, self.fdata, self.cexp, self.fexp
        resets, dep_mask, rlocal = self.resets, self.dep_mask, self.rlocal
        passive = self.passive
        witnesses = out.witnesses

        seen: list[set[int]] = [set() for _ in active]
        pseen: dict[int, set[int]] = {p[0]: set() for p in passive}
        fseen: list[set[int]] = [set() for _ in self.blocks]

        key0 = (0, tuple(intern(ctx.setup.init[b]) for b in self.blocks), (-1,) * self.nr)
        keys = [key0]
        index = {key0: 0}
        parent = [-1]
        via = [-1]
        ready_cache: dict[int, list[int]] = {}
        passive_cache: dict[int, list[tuple[int, int]]] = {}

        def path(qi: int) -> list[int]:
            p = []
            while qi > 0:
                p.append(active[via[qi]])
                qi = parent[qi]
            p.reverse()
            return p

        qi = 0
        while qi < len(keys):
            D, contents, rv = keys[qi]

            pl = passive_cache.get(D)
            if pl is None:
                pl = [(g, b) for g, b, pp, ps in passive if pp & D == pp and not ps & D]
                passive_cache[D] = pl
            for g, b in pl:
                v = contents[b]
                s = pseen[g]
                if v not in s:
                    s.add(v)
                    witnesses.append(ctx.witness(path(qi) + [g], {"id": ids[g], "value": T.to_value(terms[v])}))

            if D == full:
                for k, b in enumerate(self.blocks):
                    v = contents[k]
                    s = fseen[k]
                    if v not in s:
                        s.add(v)
                        witnesses.append(ctx.witness(path(qi), {"block": b, "value": T.to_value(terms[v])}))
                qi += 1
                continue

            rd = ready_cache.get(D)
            if rd is None:
                rd = [i for i in range(na) if not (D >> i) & 1 and pred[i] & D == pred[i]]
                ready_cache[D] = rd

            for i in rd:
                D2 = D | (1 << i)
                k = kind[i]
                b = blk[i]
                contents2 = contents
                rv2 = rv
                if k == READ:
                    v = contents[b]
                    s = seen[i]
                    if v not in s:
                        s.add(v)
                        g = active[i]
                        witnesses.append(ctx.witness(path(qi) + [g], {"id": ids[g], "value": T.to_value(terms[v])}))
                    rv2 = list(rv)
                    rv2[rlocal[i]] = v
                else:
                    if k == RCW:
                        old = contents[b]
                        s = seen[i]
                        if old not in s:
                            s.add(old)
                            g = active[i]
                            witnesses.append(
                                ctx.witness(path(qi) + [g], {"id": ids[g], "value": T.to_value(terms[old])})
                            )
                        e = cexp[i]
                        if e is None:
                            e = intern(T.substitute(fexp[i], lambda x: terms[rv[rlid[x]]]))
                        ok = old == e
                    else:
                        ok = True
                    if ok:
                        c = cdata[i]
                        if c is None:
                            c = intern(T.substitute(fdata[i], lambda x: terms[rv[rlid[x]]]))
                        if c != contents[b]:
                            contents2 = contents[:b] + (c,) + contents[b + 1 :]
                    for r in resets[i]:
                        if rv2[r] != -1 and dep_mask[r] & D2 == dep_mask[r]:
                            if rv2 is rv:
                                rv2 = list(rv)
                            rv2[r] = -1
                key2 = (D2, contents2, rv if rv2 is rv else tuple(rv2))
                if key2 not in index:
                    index[key2] = len(keys)
                    keys.append(key2)
                    parent.append(qi)
                    via.append(i)
            qi += 1

        for i, g in enumerate(active):
            if kind[i] != WRITE:
                out.results[ids[g]] = {terms[v] for v in seen[i]}
        for g, s in pseen.items():
            out.results[ids[g]] = {terms[v] for v in s}
        for k, b in enumerate(self.blocks):
            out.final[b] = {terms[v] for v in fseen[k]}


@register
class DownsetSolver(Solver):
    name = "fable51_1-sr-downset"
    description = (
        "Exact Poss by memoised search over downsets of the end-before-start precedence "
        "order on actions, per data-linked block group, with witnesses; modes all and fixed"
    )
    capabilities = SolverCapabilities(
        rcw=True,
        sync=True,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        ctx = _Context(setup, linearization)
        out = Outcomes("all" if linearization is None else "fixed", True)
        for blocks in ctx.components():
            _Component(ctx, blocks).run(out)
        return out
