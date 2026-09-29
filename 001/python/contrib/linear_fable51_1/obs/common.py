"""Shared model and the two fixed-``L`` feasibility tests behind the ``fable51-o-*`` algorithms.

Setting (premise.md §2.4-2.6): atomic register, distinct effect points, reads and writes
only, no sync (``P`` is ``N`` disjoint chains), write data may reference earlier reads
and writes of the same thread, some reads carry an observed term. Fix ``L``; every
action ``x`` has an interval ``[s(x), e(x)]``; an effect order ``π`` is admissible iff
it is a linear extension of the interval order ``x ≺ y iff e(x) < s(y)`` (the greedy
check of ``abio.semantics`` accepts exactly those, see ``contrib._archive.fable_obs.common``).

Which constant-data lemmas survive
----------------------------------
1. **Merging lemma (survives, and is stronger than "per-block independence").**
   Let ``A_1, ..., A_k`` be *any* partition of the actions and ``π_i`` a linear order
   of ``A_i`` extending ``≺|A_i``. Then ``≺ ∪ π_1 ∪ ... ∪ π_k`` is acyclic, so one
   global admissible ``π`` contains every ``π_i``. Proof: take a shortest cycle; two
   consecutive edges of the same relation merge by transitivity, so the cycle
   alternates ``π`` edges ``x <π y`` (which give ``s(x) <= e(y)``, as ``y ⊀ x``) and ``≺``
   edges ``y ≺ z`` (``e(y) < s(z)``); around the cycle this yields ``s(x) < s(x)``.
   The lemma is purely order-theoretic, so it holds with read-dependent data. What
   breaks is *independence*: the block contents are no longer independent, because a
   write on block ``b`` carries a value fixed by what a read on block ``b'`` returned in
   the same ``π``. So ``LinFeas`` is no longer an intersection of per-block sets; it
   *is* an intersection over the **components** of the data-flow graph (blocks joined
   by "a read on ``b'`` feeds a write on ``b``"), since values never cross components.
2. **"Unobserved reads never matter" (breaks; replaced by tracking).** An unobserved
   read that feeds a write whose content can be observed does matter (its value is the
   write's content). What survives: a read that no *surviving goal* (below) mentions
   can be inserted anywhere by lemma 1 (singleton part), so it is dropped.
3. **"Structural values" (replaced by matching).** A write's content is no longer a
   fixed term, but ``~`` is a free constructor, so *whether* ``content(w) = v`` for a
   given term ``v`` is decided by **matching** the write's expression (write references
   expanded, ``"*"`` = its own symbol) against ``v``: matching either fails or yields
   a unique requirement ``value(r_i) = v_i`` for every referenced read (``v_i`` a
   subterm of ``v``; a read referenced twice must get equal subterms). Hence an observed
   compound value such as ``init.1~7`` pins down both the write (``r1~7``) and what
   its inner read saw (``init.1``).

Goals and classes
-----------------
A *goal* is a pair ``(block b, term v)``, "some read of ``b`` must return ``v``".
Observed reads give the initial goals; matching every write of ``b`` against ``v``
gives the *sources* of the goal (``init(b)`` when it equals ``v``, or a write ``w``
with its requirements, each a goal on the block of the referenced read). A greatest
fixpoint removes goals with no source (init or a write all of whose requirements are
possible goals). The reads that appear in surviving requirements are the *feeder*
reads; observed and feeder reads are *tracked*; the writes of their blocks are tracked
as overwriters. Requirements on observed reads are checked statically (an observed
read returns its observation in every feasible schedule).

For a tracked block ``b`` let ``Vals_b`` be its goal values. The *class* of a content
of ``b`` is the index of the goal value it equals, or ``-1``. Since a term equals at
most one goal value, a class is a single number, and by induction over effect time it
determines exactly which requirements hold: ``content(w) = v`` iff the requirements of
the option ``v`` of ``w`` hold iff the classes of the referenced reads equal the
required indices. So the finite class abstraction of values is **exact** for
feasibility.

Two exact fixed-``L`` tests, both differentially tested against ``abio.semantics``:

``is_feasible_auto`` (automaton criterion, :func:`comp_feasible_auto`)
    Walk ``L`` and simulate the register nondeterministically per component: a
    configuration is ``(E, c, rk, wk)``: the in-flight tracked actions that took effect,
    the class of each block's content, the class returned by each *live* feeder read
    (kept from its effect to the start of the last write that references it) and the
    class each in-flight write will store (computed at its start, when all referenced
    reads have completed). After a start step the set of reachable configurations is
    closed under "one pending action takes effect" (a write stores ``wk``; a feeder read
    records the current class if it is one of its goal values; an observed read may
    take effect only when the current class is its observation); at ``done(x)`` the
    configurations with ``x`` not effected are dropped. ``L`` is feasible iff every
    component keeps a configuration to the end: every consistent ``π`` is traced by the
    simulation and every surviving path is a consistent ``π`` (the abstraction is exact
    by the class argument above; component independence by lemma 1).

``is_feasible_fast`` (reads-from criterion, :func:`comp_feasible_rf`)
    Goal-directed search over *reads-from* choices with term structure: resolve each
    goal ``(r, v)`` by a source (``init`` or a write with option ``v``), which spawns the
    option's requirements as new goals; a read already assigned must agree. Order is
    kept per block as a precedence digraph on the block's writes plus a virtual
    ``init`` node, with edges ``≺|writes``, ``init → every write``, and for each
    assigned read ``r`` with source ``w``: ``r ⊀ w``; ``w' ≺ r ⇒ w' → w``; ``r ≺ w' ⇒ w →
    w'``; and for assigned ``r'`` of the same block, ``r ≺ r' ⇒ rf(r) → rf(r')``
    (when different). Claim: a full assignment is realizable iff every block's digraph
    is acyclic. Proof: given a linear extension ``σ = w_1 < ... < w_k`` of the digraph,
    put every read in the *slot* of its source (rank ``2i`` for ``w_i``, ``2i+1`` for
    its readers); the required ``π_b`` exists iff "slot preorder ∪ ≺" is acyclic; a
    shortest cycle has no two consecutive ≺ edges, so it uses a ≺ edge going backwards
    or within a rank; backward edges are exactly what the digraph edges exclude
    (``w' ≺ r`` with ``w'`` after ``rf(r)``, ``r ≺ w'`` with ``w'`` at or before ``rf(r)``,
    ``r ≺ r'`` with a later slot for ``r``), and same-rank edges are among reads, a
    partial order. Conversely the write order of any realizing ``π`` satisfies every
    edge. Per-block ``π_b`` merge by lemma 1, unassigned reads are inserted by lemma 1,
    and values match by construction of the goals. Exponential only in the number of
    alternative sources per goal (Gibbons–Korach); polynomial when values are distinct.

Both criteria are used on **prefixes** too: with unplaced endpoints at ``+∞`` the
relation ``≺`` of a prefix is a subset of that of every completion, feasibility is
anti-monotone in ``≺``, and the automaton's configuration set after a prefix is a
function of the prefix alone. With constant data the goals are the observations, the
classes are content indices, and both tests reduce to those of ``contrib._archive.fable_obs``.
"""

from __future__ import annotations

from typing import Sequence

from abio import terms as T
from abio.capabilities import Capabilities
from abio.model import Setup
from abio.semantics import is_feasible as _oracle  # noqa: F401  (re-exported for tests)

DEP = Capabilities(rcw=False, sync=False, observed_reads=True)

INF = 1 << 40
FREE = -2  # class slot not in use
NONE = -1  # content / value that equals no goal value


# --------------------------------------------------------------------------- term matching


def expand(setup: Setup, wid: str) -> T.Node:
    """The expression of write ``wid`` with write references expanded: leaves are ``Const``, ``Unk``, ``Ref(read)``."""
    a = setup.actions[wid]
    if a.data is None:
        return T.Unk(wid)

    def sub(e: T.Node) -> T.Node:
        if isinstance(e, T.Pair):
            return T.Pair(sub(e.left), sub(e.right))
        if isinstance(e, T.Ref) and setup.actions[e.action].kind != "read":
            return expand(setup, e.action)
        return e

    return sub(a.data)


def match(e: T.Node, t: T.Term, out: dict[str, T.Term]) -> bool:
    """Does the expanded expression ``e`` equal ``t`` for some read values? Fills ``out`` (read -> value)."""
    if isinstance(e, T.Pair):
        return isinstance(t, T.Pair) and match(e.left, t.left, out) and match(e.right, t.right, out)
    if isinstance(e, T.Ref):
        if e.action in out:
            return out[e.action] == t
        out[e.action] = t
        return True
    return e == t


# --------------------------------------------------------------------------- static model


class Comp:
    """One data-flow component: its tracked actions (local indices ``0..m-1``) and their static data."""

    def __init__(self, model: "Model", blocks: list[int]) -> None:
        setup = model.setup
        P = setup.poset
        acts = setup.actions
        self.blocks = blocks
        bl = {b: i for i, b in enumerate(blocks)}
        tracked = [a for a in acts.values() if a.block in bl and (a.kind == "write" or a.id in model.tracked_reads)]
        self.m = m = len(tracked)
        self.ids = [a.id for a in tracked]
        loc = {a.id: i for i, a in enumerate(tracked)}
        self.is_write = [a.kind == "write" for a in tracked]
        self.blk = [bl[a.block] for a in tracked]
        self.start = [P.start_node[a.id] for a in tracked]
        self.done = [P.done_node[a.id] for a in tracked]
        self.nb = len(blocks)
        self.nvals = [len(model.vlist[b]) for b in blocks]
        self.init_cls = [model.vals[b].get(setup.init[b], NONE) for b in blocks]
        self.wmask = sum(1 << i for i in range(m) if self.is_write[i])
        self.rmask = ((1 << m) - 1) & ~self.wmask
        self.writes_of_block = [0] * self.nb
        for i in range(m):
            if self.is_write[i]:
                self.writes_of_block[self.blk[i]] |= 1 << i
        # feeder reads get a class slot; observed reads have a fixed class
        self.obs = [NONE] * m
        self.rslot = [-1] * m
        self.gmask = [0] * m
        nr = 0
        for i, a in enumerate(tracked):
            if a.kind == "read":
                if a.observed is not None:
                    self.obs[i] = model.vals[a.block][a.observed]
                else:
                    self.rslot[i] = nr
                    nr += 1
                    for vi in model.goals_of_read[a.id]:
                        self.gmask[i] |= 1 << vi
        self.nr = nr
        # write options: (class, [(read slot, required class)]) and a class slot per write with options
        self.options: list[list[tuple[int, list[tuple[int, int]]]]] = [[] for _ in range(m)]
        self.wslot = [-1] * m
        self.suppliers = [0] * m  # observed read i -> mask of writes with an option equal to its observation
        nw = 0
        referencers: dict[int, list[int]] = {}
        for i, a in enumerate(tracked):
            if a.kind != "write":
                continue
            for vi, reqs in model.options.get(a.id, []):
                self.options[i].append((vi, [(self.rslot[loc[rid]], vi2) for rid, _, vi2 in reqs]))
                for rid, _, _ in reqs:
                    referencers.setdefault(loc[rid], []).append(i)
            if self.options[i]:
                self.wslot[i] = nw
                nw += 1
        self.nw = nw
        for i in range(m):
            if self.obs[i] != NONE:
                for w in range(m):
                    if self.is_write[w] and self.blk[w] == self.blk[i] and any(vi == self.obs[i] for vi, _ in self.options[w]):
                        self.suppliers[i] |= 1 << w
        # a feeder read's class slot is freed at the start of the last-starting write that references it
        self.free_after: list[list[int]] = [[] for _ in range(m)]
        for r, ws in referencers.items():
            last = max(set(ws), key=lambda w: acts[self.ids[w]].start)
            self.free_after[last].append(self.rslot[r])
        # configuration layout: (E, c[nb], rk[nr], wk[nw])
        self.C = 1
        self.RK = 1 + self.nb
        self.WK = 1 + self.nb + nr
        self.n_obs = sum(1 for i in range(m) if self.obs[i] != NONE)


class Model:
    """Goals, tracked actions and components of a setup, plus node -> (component, local index) maps."""

    def __init__(self, setup: Setup) -> None:
        self.setup = setup
        acts = setup.actions
        P = setup.poset
        writes_by_block: dict[int, list] = {}
        for a in acts.values():
            if a.kind == "write":
                writes_by_block.setdefault(a.block, []).append(a)
        expanded = {a.id: expand(setup, a.id) for a in acts.values() if a.kind == "write"}
        self.vals: list[dict[T.Term, int]] = [{} for _ in range(setup.blocks)]
        self.vlist: list[list[T.Term]] = [[] for _ in range(setup.blocks)]
        sources: dict[tuple[int, int], list[tuple[str, list[tuple[str, int, int]]]]] = {}
        init_ok: dict[tuple[int, int], bool] = {}
        work: list[tuple[int, int]] = []

        def key(b: int, t: T.Term) -> int:
            vi = self.vals[b].get(t)
            if vi is None:
                vi = self.vals[b][t] = len(self.vlist[b])
                self.vlist[b].append(t)
                work.append((b, vi))
            return vi

        for a in acts.values():
            if a.kind == "read" and a.observed is not None:
                key(a.block, a.observed)
        while work:
            b, vi = work.pop()
            t = self.vlist[b][vi]
            init_ok[(b, vi)] = setup.init[b] == t
            lst = []
            for w in writes_by_block.get(b, []):
                out: dict[str, T.Term] = {}
                if not match(expanded[w.id], t, out):
                    continue
                reqs: list[tuple[str, int, int]] = []
                ok = True
                for rid, tt in out.items():
                    rr = acts[rid]
                    if rr.observed is not None:
                        if rr.observed != tt:
                            ok = False
                            break
                    else:
                        reqs.append((rid, rr.block, key(rr.block, tt)))
                if ok:
                    lst.append((w.id, reqs))
            sources[(b, vi)] = lst
        # greatest fixpoint: a goal is possible iff init supplies it or some option has only possible requirements
        possible = {k: True for k in sources}
        changed = True
        while changed:
            changed = False
            for k, lst in sources.items():
                if possible[k] and not (init_ok[k] or any(all(possible[(b2, v2)] for _, b2, v2 in reqs) for _, reqs in lst)):
                    possible[k] = False
                    changed = True
        self.options: dict[str, list[tuple[int, list[tuple[str, int, int]]]]] = {}
        self.goals_of_read: dict[str, set[int]] = {}
        for (b, vi), lst in sources.items():
            if not possible[(b, vi)]:
                continue
            for wid, reqs in lst:
                if all(possible[(b2, v2)] for _, b2, v2 in reqs):
                    self.options.setdefault(wid, []).append((vi, reqs))
                    for rid, _, v2 in reqs:
                        self.goals_of_read.setdefault(rid, set()).add(v2)
        self.impossible = any(a.kind == "read" and a.observed is not None and not possible[(a.block, self.vals[a.block][a.observed])]
                              for a in acts.values())
        self.tracked_reads = {a.id for a in acts.values() if a.kind == "read" and (a.observed is not None or self.goals_of_read.get(a.id))}
        tracked_blocks = sorted({acts[r].block for r in self.tracked_reads})
        # components: union-find over tracked blocks along requirement edges
        parent = {b: b for b in tracked_blocks}

        def find(b: int) -> int:
            while parent[b] != b:
                parent[b] = parent[parent[b]]
                b = parent[b]
            return b

        for wid, opts in self.options.items():
            for _, reqs in opts:
                for _, b2, _ in reqs:
                    ra, rb = find(acts[wid].block), find(b2)
                    if ra != rb:
                        parent[ra] = rb
        groups: dict[int, list[int]] = {}
        for b in tracked_blocks:
            groups.setdefault(find(b), []).append(b)
        self.comps = [Comp(self, bs) for _, bs in sorted(groups.items())]
        n = len(P)
        self.node_comp = [-1] * n
        self.node_local = [0] * n
        self.node_is_start = [False] * n
        for ci, c in enumerate(self.comps):
            for i in range(c.m):
                self.node_comp[c.start[i]] = ci
                self.node_local[c.start[i]] = i
                self.node_is_start[c.start[i]] = True
                self.node_comp[c.done[i]] = ci
                self.node_local[c.done[i]] = i

    def feasible_rf(self, order: Sequence[int]) -> bool:
        if self.impossible:
            return False
        pos = self.setup.poset.positions(order)
        return all(comp_feasible_rf(c, pos) for c in self.comps)

    def feasible_auto(self, order: Sequence[int]) -> bool:
        if self.impossible:
            return False
        pos = self.setup.poset.positions(order)
        return all(comp_feasible_auto(c, pos) for c in self.comps)


def precedence(comp: Comp, pos: Sequence[int]) -> list[int]:
    """``pre[x]`` = mask of local ``y`` with ``y ≺ x`` (``e(y) < s(x)``); unplaced endpoints count as ``+∞``."""
    m = comp.m
    s = [pos[x] if pos[x] >= 0 else INF for x in comp.start]
    e = [pos[x] if pos[x] >= 0 else INF for x in comp.done]
    pre = [0] * m
    for x in range(m):
        sx = s[x]
        mask = 0
        for y in range(m):
            if e[y] < sx and y != x:
                mask |= 1 << y
        pre[x] = mask
    return pre


# --------------------------------------------------------------------------- reads-from criterion


def comp_feasible_rf(comp: Comp, pos: Sequence[int]) -> bool:
    """Reads-from criterion for one component (module docstring). Exact for a complete order, sound for a prefix."""
    m, nb = comp.m, comp.nb
    if comp.n_obs == 0:
        return True
    pre = precedence(comp, pos)
    blk, is_write, wob = comp.blk, comp.is_write, comp.writes_of_block
    N = m + nb  # node m + b is the virtual initial write of local block b
    succ = [0] * N
    for w in range(m):
        if is_write[w]:
            for y in range(m):
                if pre[y] >> w & 1 and blk[y] == blk[w] and is_write[y]:
                    succ[w] |= 1 << y  # w ≺ y
    for b in range(nb):
        succ[m + b] = wob[b]
    by_val: list[dict[int, list[tuple[int, list[tuple[int, int]]]]]] = [{} for _ in range(nb)]
    slot_read = {comp.rslot[i]: i for i in range(m) if comp.rslot[i] >= 0}
    for w in range(m):
        for vi, reqs in comp.options[w]:
            by_val[blk[w]].setdefault(vi, []).append((w, [(slot_read[rs], v2) for rs, v2 in reqs]))
    trail: list[tuple[int, int]] = []

    def reaches(a: int, target: int) -> bool:
        seen = 1 << a
        stack = [a]
        while stack:
            u = stack.pop()
            if u == target:
                return True
            new = succ[u] & ~seen
            seen |= new
            while new:
                low = new & -new
                new ^= low
                stack.append(low.bit_length() - 1)
        return False

    def add_edge(u: int, v: int) -> bool:
        if u == v:
            return False
        if succ[u] >> v & 1:
            return True
        if reaches(v, u):
            return False
        trail.append((u, succ[u]))
        succ[u] |= 1 << v
        return True

    assigned: dict[int, tuple[int, int]] = {}

    def solve(goals: list[tuple[int, int]]) -> bool:
        if not goals:
            return True
        r, vi = goals[-1]
        if r in assigned:
            return assigned[r][1] == vi and solve(goals[:-1])
        b = blk[r]
        cands: list[tuple[int, list[tuple[int, int]]]] = []
        if comp.init_cls[b] == vi:
            cands.append((m + b, []))
        cands.extend(by_val[b].get(vi, ()))
        for src, reqs in cands:
            if src < m and pre[src] >> r & 1:
                continue  # r ≺ src: the source cannot take effect before the read
            mark = len(trail)
            ok = True
            bits = wob[b]
            while ok and bits:
                low = bits & -bits
                bits ^= low
                w2 = low.bit_length() - 1
                if w2 == src:
                    continue
                if pre[r] >> w2 & 1:
                    ok = add_edge(w2, src)
                elif pre[w2] >> r & 1:
                    ok = add_edge(src, w2)
            if ok:
                for r2, (src2, _) in assigned.items():
                    if blk[r2] != b or src2 == src:
                        continue
                    if pre[r2] >> r & 1:
                        ok = add_edge(src, src2)
                    elif pre[r] >> r2 & 1:
                        ok = add_edge(src2, src)
                    if not ok:
                        break
            if ok:
                assigned[r] = (src, vi)
                if solve(goals[:-1] + reqs):
                    return True
                del assigned[r]
            while len(trail) > mark:
                u, old = trail.pop()
                succ[u] = old
        return False

    return solve([(i, comp.obs[i]) for i in range(m) if comp.obs[i] != NONE])


# --------------------------------------------------------------------------- automaton criterion

State = tuple[int, frozenset]  # (in-flight mask, configurations)


def initial_state(comp: Comp) -> State:
    return 0, frozenset({(0,) + tuple(comp.init_cls) + (FREE,) * (comp.nr + comp.nw)})


def closure(comp: Comp, configs, inflight: int) -> frozenset:
    """Close a configuration set under "one pending tracked action takes effect"."""
    C, RK, WK = comp.C, comp.RK, comp.WK
    is_write, blk, wslot, rslot, gmask, obs = comp.is_write, comp.blk, comp.wslot, comp.rslot, comp.gmask, comp.obs
    out = set(configs)
    stack = list(configs)
    while stack:
        cf = stack.pop()
        E = cf[0]
        pend = inflight & ~E
        while pend:
            low = pend & -pend
            pend ^= low
            i = low.bit_length() - 1
            b = blk[i]
            if is_write[i]:
                ws = wslot[i]
                lst = list(cf)
                lst[0] = E | low
                if ws >= 0:
                    lst[C + b] = cf[WK + ws]
                    lst[WK + ws] = FREE
                else:
                    lst[C + b] = NONE
                nc = tuple(lst)
            elif obs[i] != NONE:
                if cf[C + b] != obs[i]:
                    continue
                nc = (E | low,) + cf[1:]
            else:
                c = cf[C + b]
                lst = list(cf)
                lst[0] = E | low
                lst[RK + rslot[i]] = c if c >= 0 and gmask[i] >> c & 1 else NONE
                nc = tuple(lst)
            if nc not in out:
                out.add(nc)
                stack.append(nc)
    return frozenset(out)


def step(comp: Comp, state: State, i: int, is_start: bool) -> State | None:
    """Advance a component's automaton state over an endpoint of local action ``i``; None when nothing survives."""
    inflight, configs = state
    bit = 1 << i
    if is_start:
        if comp.is_write[i] and (comp.wslot[i] >= 0 or comp.free_after[i]):
            RK, WK = comp.RK, comp.WK
            ws, opts, frees = comp.wslot[i], comp.options[i], comp.free_after[i]
            new = set()
            for cf in configs:
                lst = list(cf)
                if ws >= 0:
                    cls = NONE
                    for vi, reqs in opts:
                        if all(cf[RK + rs] == req for rs, req in reqs):
                            cls = vi
                            break
                    lst[WK + ws] = cls
                for rs in frees:
                    lst[RK + rs] = FREE
                new.add(tuple(lst))
            configs = new
        inflight |= bit
        return inflight, closure(comp, configs, inflight)
    keep = frozenset((cf[0] & ~bit,) + cf[1:] for cf in configs if cf[0] & bit)
    if not keep:
        return None
    return inflight & ~bit, keep


def comp_feasible_auto(comp: Comp, pos: Sequence[int]) -> bool:
    """Automaton criterion for one component over a complete order given by positions."""
    if comp.n_obs == 0:
        return True
    events = sorted([(pos[comp.start[i]], i, True) for i in range(comp.m)] + [(pos[comp.done[i]], i, False) for i in range(comp.m)])
    state = initial_state(comp)
    for _, i, is_start in events:
        state = step(comp, state, i, is_start)
        if state is None:
            return False
    return True


# --------------------------------------------------------------------------- public tests


def is_feasible_fast(setup: Setup, order: Sequence[int]) -> bool:
    """Fixed-``L`` feasibility by the reads-from criterion (module docstring)."""
    return Model(setup).feasible_rf(order)


def is_feasible_auto(setup: Setup, order: Sequence[int]) -> bool:
    """Fixed-``L`` feasibility by the automaton criterion (module docstring)."""
    return Model(setup).feasible_auto(order)
