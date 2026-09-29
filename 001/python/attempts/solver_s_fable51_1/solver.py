"""Exact possibility sets for cases ``b`` and ``s`` (sync allowed, no observed reads).

Method (own derivation; see SOURCES.md):

1. Effect orders.  A full schedule ``(L, pi)`` is a linear extension of the trace poset
   ``P`` extended with one effect node per action, placed strictly between that action's
   start and done.  Restricting linear extensions to the effect nodes shows that the
   effect orders reachable over *all* linearizations are exactly the linear extensions of
   the **action poset** ``Q``:  ``a < b`` iff ``done(a)`` reaches ``start(b)`` in ``P``.
   For one fixed ``L`` the same holds with ``a < b`` iff ``pos(done(a)) < pos(start(b))``.

2. Values.  Under an effect order a read returns the content of the last write to its
   block placed before it (or the block's initial content); a write's content is its
   expression with every referenced read replaced by that read's value (references to
   writes are inlined).  Hence a read's value is a function of a *source map*: which write
   (or ``init``) it reads from, recursively for the reads its source depends on.

3. Enumeration.  For every read (and for every block, through a virtual read placed
   after everything) source maps are enumerated depth-first, keeping only those for
   which some linear extension of ``Q`` realises every constraint
   "``w`` is the last write to ``b`` before ``r``" (or "no write to ``b`` before ``r``").

4. Feasibility of a constraint set is decided on the induced sub-poset of the relevant
   actions: constraints and forced relations are added as edges and propagated to a
   fixpoint, blockers that can always go first or last are dropped, and only when a
   genuine disjunction is left does a memoised search over ideals run.
"""

from __future__ import annotations

import sys

import harness.terms as T
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


def _bits(m: int):
    """Indices of the set bits of ``m``, lowest first."""
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


class _Engine:
    """All per-setup precomputation plus the enumeration and feasibility machinery.

    Actions are indexed ``0..n-1`` in ``setup.actions`` order; index ``n`` is a virtual
    read placed after every action, used for the final content of a block (its block is
    set per query).  Sets of actions are bit masks.
    """

    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        acts = list(setup.actions.values())
        self.acts = acts
        n = len(acts)
        self.n = n
        self.idx = {a.id: i for i, a in enumerate(acts)}
        self.block = [a.block for a in acts] + [0]
        self.is_write = [a.kind != "read" for a in acts] + [False]
        self.init = list(setup.init)
        poset = setup.poset

        # pred[i]: mask of actions strictly before i in the action poset Q (transitive).
        if lin is None:
            reach = self._reach(poset)
            done_reach = [reach[poset.done_node[a.id]] for a in acts]
            start_of = [poset.start_node[a.id] for a in acts]

            def before(j: int, i: int) -> bool:
                return bool((done_reach[j] >> start_of[i]) & 1)

        else:
            pos = poset.positions(lin)
            done_pos = [pos[poset.done_node[a.id]] for a in acts]
            start_pos = [pos[poset.start_node[a.id]] for a in acts]

            def before(j: int, i: int) -> bool:
                return done_pos[j] < start_pos[i]

        pred = [0] * (n + 1)
        for i in range(n):
            m = 0
            for j in range(n):
                if j != i and before(j, i):
                    m |= 1 << j
            pred[i] = m
        pred[n] = (1 << n) - 1
        self.pred = pred
        succ = [0] * (n + 1)
        for i in range(n):
            for j in _bits(pred[i]):
                succ[j] |= 1 << i
        self.succ = succ

        # writes per block
        self.wmask = [0] * setup.blocks
        for i, a in enumerate(acts):
            if a.kind != "read":
                self.wmask[a.block] |= 1 << i

        # flat[i]: write i's expression with write references inlined (leaves: Const,
        # Unk, Ref-to-read); deps[i]: mask of the reads it references.
        self.flat: list = [None] * n
        self.deps = [0] * n
        for i, a in enumerate(acts):
            if a.kind != "read":
                f = self._flatten(i)
                d = 0
                for x in T.refs(f):
                    d |= 1 << self.idx[x]
                self.deps[i] = d

        self._fcache: dict = {}

    @staticmethod
    def _reach(poset) -> list[int]:
        """reach[v]: mask of the nodes strictly reachable from v in P."""
        order = poset.topological_order()
        reach = [0] * len(poset)
        for v in reversed(order):
            m = 0
            for u in poset.succs[v]:
                m |= (1 << u) | reach[u]
            reach[v] = m
        return reach

    def _flatten(self, i: int):
        f = self.flat[i]
        if f is not None:
            return f
        a = self.acts[i]
        if a.data is None:
            f = T.Unk(a.id)
        else:

            def lookup(x: str):
                j = self.idx[x]
                if self.acts[j].kind == "read":
                    return T.Ref(x)
                return self._flatten(j)

            f = T.substitute(a.data, lookup)
        self.flat[i] = f
        return f

    # ------------------------------------------------------------------ queries

    def poss_read(self, i: int) -> set:
        return self._poss(i)

    def poss_final(self, b: int) -> set:
        self.block[self.n] = b
        return self._poss(self.n)

    def _poss(self, target: int) -> set:
        self._fcache = {}
        out: set = set()
        self._derive(frozenset(), 1 << target, 0, {}, out, target)
        return out

    def _candidates(self, p: int) -> list:
        """Sources of read p that pass the single-constraint test: None (init) or a write."""
        b = self.block[p]
        wm = self.wmask[b]
        out: list = []
        if wm & self.pred[p] == 0:
            out.append(None)
        for w in _bits(wm):
            if (self.succ[p] >> w) & 1:
                continue  # p before w
            if self.succ[w] & self.pred[p] & wm:
                continue  # another write to b strictly between w and p
            out.append(w)
        return out

    def _derive(self, C: frozenset, pending: int, assigned: int, src: dict, out: set, target: int) -> None:
        if pending == 0:
            out.add(self._value(target, src, {}))
            return
        low = pending & -pending
        p = low.bit_length() - 1
        rest = pending ^ low
        for w in self._candidates(p):
            C2 = C | frozenset(((p, w),))
            if not self._feasible(C2):
                continue
            src[p] = w
            newp = rest
            if w is not None:
                newp |= self.deps[w] & ~(assigned | low)
            self._derive(C2, newp, assigned | low, src, out, target)
            del src[p]

    def _value(self, p: int, src: dict, memo: dict):
        v = memo.get(p)
        if v is not None:
            return v
        w = src[p]
        if w is None:
            v = self.init[self.block[p]]
        else:
            v = T.substitute(self.flat[w], lambda x: self._value(self.idx[x], src, memo))
        memo[p] = v
        return v

    # ------------------------------------------------------------------ feasibility

    def _feasible(self, C: frozenset) -> bool:
        r = self._fcache.get(C)
        if r is None:
            r = self._decide(C)
            self._fcache[C] = r
        return r

    def _decide(self, C: frozenset) -> bool:
        """Is there a linear extension of Q realising every constraint of C?

        A constraint ``(p, w)`` means: ``w`` is the last write to ``block[p]`` before
        ``p``; ``(p, None)`` means: no write to ``block[p]`` before ``p``.
        """
        pred, block, wmask = self.pred, self.block, self.wmask
        cons = list(C)

        # Relevant actions: constrained reads and writes, plus the blockers (other writes
        # to a constrained block) that are not trivially outside every interval.
        con_mask = 0
        for p, w in cons:
            con_mask |= 1 << p
            if w is not None:
                con_mask |= 1 << w
        rel = con_mask
        for p, w in cons:
            m = wmask[block[p]]
            if w is not None:
                m &= ~(1 << w)
            for x in _bits(m):
                if (pred[x] >> p) & 1:
                    continue  # after p in every extension
                if w is not None and (pred[w] >> x) & 1:
                    continue  # before w in every extension
                rel |= 1 << x
        lp = {i: pred[i] & rel for i in _bits(rel)}  # local transitive closure

        def add_edge(u: int, v: int) -> bool:
            """Impose u before v; False if that closes a cycle."""
            if u == v or (lp[u] >> v) & 1:
                return False
            if (lp[v] >> u) & 1:
                return True
            add = lp[u] | (1 << u)
            for y in lp:
                if y == v or (lp[y] >> v) & 1:
                    lp[y] |= add
            return True

        # The constraints' own orderings.
        for p, w in cons:
            if w is not None:
                if not add_edge(w, p):
                    return False
            else:
                for x in _bits(wmask[block[p]] & rel):
                    if not add_edge(p, x):
                        return False

        # Forced resolutions of blockers, to a fixpoint.
        changed = True
        while changed:
            changed = False
            for p, w in cons:
                if w is None:
                    continue
                for x in _bits(wmask[block[p]] & rel & ~(1 << w)):
                    if (lp[p] >> x) & 1:  # x before p: it must precede w
                        if not (lp[w] >> x) & 1:
                            if not add_edge(x, w):
                                return False
                            changed = True
                    elif (lp[x] >> w) & 1:  # x after w: it must follow p
                        if not (lp[x] >> p) & 1:
                            if not add_edge(p, x):
                                return False
                            changed = True

        # Drop unconstrained blockers that can always go first or last.
        droppable = rel & ~con_mask
        changed = True
        while changed:
            changed = False
            for x in _bits(droppable & rel):
                if lp[x] & rel == 0:
                    rel &= ~(1 << x)
                    changed = True
                    continue
                maximal = True
                for y in _bits(rel & ~(1 << x)):
                    if (lp[y] >> x) & 1:
                        maximal = False
                        break
                if maximal:
                    rel &= ~(1 << x)
                    changed = True

        # Any disjunction left?  If not, the augmented order is acyclic, hence realisable.
        unresolved = False
        for p, w in cons:
            if w is None:
                continue
            for x in _bits(wmask[block[p]] & rel & ~(1 << w)):
                if (lp[w] >> x) & 1 or (lp[x] >> p) & 1:
                    continue
                unresolved = True
                break
            if unresolved:
                break
        if not unresolved:
            return True

        # Search over ideals of the reduced sub-poset, memoising failed ideals.
        conreads = 0
        for p, _ in cons:
            conreads |= 1 << p
        cons_by_block: dict = {}
        for p, w in cons:
            cons_by_block.setdefault(block[p], []).append((p, w))
        read_con = {p: w for p, w in cons}
        is_write = self.is_write
        failed: set = set()
        final_rel = rel

        def dfs(placed: int) -> bool:
            if placed & conreads == conreads:
                return True
            if placed in failed:
                return False
            rem = final_rel & ~placed
            for i in _bits(rem):
                if lp[i] & rem:
                    continue  # some predecessor still unplaced
                ok = True
                if is_write[i]:
                    for p, w in cons_by_block.get(block[i], ()):
                        if (placed >> p) & 1:
                            continue
                        if w is None or (w != i and (placed >> w) & 1):
                            ok = False
                            break
                else:
                    w = read_con.get(i)
                    if w is not None and not (placed >> w) & 1:
                        ok = False
                if ok and dfs(placed | (1 << i)):
                    return True
            failed.add(placed)
            return False

        return dfs(0)


@register
class LastWriteSolver(Solver):
    name = "fable51_1-s-lastwrite"
    description = "Exact Poss via source-map enumeration over the action poset (last-write constraints)"
    capabilities = SolverCapabilities(
        rcw=False,
        sync=True,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        n = len(setup.actions)
        limit = 4 * n + 2000
        if sys.getrecursionlimit() < limit:
            sys.setrecursionlimit(limit)
        eng = _Engine(setup, linearization)
        results: dict = {}
        for a in setup.returning():
            results[a.id] = eng.poss_read(eng.idx[a.id])
        final: dict = {}
        for b in range(setup.blocks):
            final[b] = eng.poss_final(b)
        return Outcomes(mode, True, results, final)
