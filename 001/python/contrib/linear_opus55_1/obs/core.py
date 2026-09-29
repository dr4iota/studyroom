"""Feasibility with observed reads AND read-dependent write data: theory and fixed-``L`` test.

Scope: Read/Write actions, no sync (the code itself works on any DAG, so sync edges would
not break it, but only ``K = 0`` is declared and tested). Write data is any expression of
formats.md §2.2: constants, ``"*"`` (the free symbol ``Unk(w)``), references to earlier
completed reads of the same thread, references to earlier writes of the same thread, and
``~``-trees of these. ``init[b]`` is a term or ``Init(b)``. Some reads carry an observed
term (possibly compound). Terms are compared structurally (free, non-commutative ``~``).

Notation. Fix ``L``; ``s(x), e(x)`` are the positions of the endpoints of action ``x``;
``x < y`` iff ``e(x) < s(y)`` (the interval order of ``L``).

Expanded write expressions. Replacing every reference to a write by that write's own
(expanded) expression, or by ``Unk(w')`` if its data is ``"*"``, gives ``exp(w)``: a tree
whose leaves are constants, ``Unk`` symbols and ``Ref(r)`` for reads ``r``. In any
schedule ``content(w) = exp(w)[r := val(r)]`` (formats.md §2.2; ``semantics._State``).

What survives from the constant-data theory (contrib._archive.opus_obs.core) and what breaks
---------------------------------------------------------------------------------
* SURVIVES, Lemma 0 (admissible effect orders = linear extensions of ``<``): it never
  looks at data.
* SURVIVES, Lemma 1 *for realizability only*: an effect order per block, each extending
  ``<`` on that block, merges into one global admissible effect order (points in the open
  intervals, perturbed apart). This is about positions, not values.
* SURVIVES, the cluster Theorem for a FIXED reads-from map ``rf`` on a set ``S`` of reads of
  one block (conditions (i)-(iii) below); again it never looks at values. Reads outside
  ``S`` can be given any point in their interval.
* BREAKS, "feasible iff each block is feasible": blocks are coupled through values: which
  write ``w`` a read on block 0 sees determines what a write on block 1 (fed by that read)
  contains, hence which observed reads on block 1 it can serve.
* BREAKS, "unobserved reads never matter" and "blocks without observed reads never
  matter": an unobserved read feeding a write that an observed read sees is constrained
  to return a specific term, so its reads-from matters, possibly on a block with no
  observation at all.
* BREAKS, "the candidates of an observed read are static": whether ``content(w) = obs(r)``
  depends on the reads-from of the reads feeding ``w``.
* SURVIVES (in a new form), antitonicity: the value part of the problem does not depend
  on the relation ``R`` (see below), so ``F`` is still antitone in ``R``; every prefix /
  poset bound of the constant-data enumerators still applies.

Requirements (term structure). Call a read *required with term t* if the schedule must
make it return ``t``. Observed reads are required with their observation. If a required
read ``r`` (term ``t``) reads from write ``w`` then ``t = exp(w)[r' := val(r')]``; since
``~`` is a free constructor, *matching* ``exp(w)`` against ``t`` either fails or yields a
unique binding ``r' -> t'`` for every read leaf ``r'`` of ``exp(w)`` (a compound observed
value such as ``init.1~7`` therefore pins down what the inner read saw). Each bound read
becomes required with its bound term, and two requirements on one read must be equal.
If it reads from INIT then ``t = init[b]``. Reads that are never required are *free*:
whatever they return is irrelevant, so they are simply left out of ``S``.

Definition. For a relation ``R`` on the relevant actions (below), ``F(R)`` holds iff there is
a set ``S`` of reads with requirements ``req`` and a map ``rf: S -> writes + {INIT}`` with

  (V) every observed read is in ``S`` with ``req = obs``; for ``r in S``, ``rf(r) = INIT``
      implies ``req(r) = init[blk r]``, and ``rf(r) = w`` (a write on ``blk r``) implies
      ``exp(w)`` matches ``req(r)`` and every read leaf ``r'`` of ``exp(w)`` is in ``S``
      with ``req(r')`` = its binding;
  (i)   not ``r R rf(r)`` whenever ``rf(r)`` is a write;
  (ii)  per block, no member of a write cluster ``R``-precedes a reader of INIT;
  (iii) per block, no two write clusters ``C != D`` with ``C ->_R D`` and ``D ->_R C``,

where clusters are ``C_w = {w} + rf^-1(w)`` over all writes ``w`` of the block, and
``C ->_R D`` iff some ``x in C`` has ``x R y`` for some ``y in D``.

Theorem. ``L`` is feasible iff ``F(<_L)``.
Proof. (=>) Take a feasible ``(L, pi)``; ``pi`` extends ``<_L`` (Lemma 0). Let ``S`` be the
closure of the observed reads under "leaf of the write I read from", ``req = val``,
``rf`` = what ``pi`` makes each read see. (V) holds because the actual values satisfy the
equations; (i)-(iii) hold by the cluster Theorem (necessity) applied per block.
(<=) By the cluster Theorem, per block there is an effect order of the block's writes and
the reads of ``S`` that extends ``<_L`` and realizes ``rf``; by Lemma 1 they merge into one
admissible global order ``pi`` (other reads anywhere in their intervals). Under ``pi`` every
``r in S`` returns ``content(rf(r))`` at the time ``pi(rf(r)) < pi(r)``. Induction along
``pi``: the leaves ``r'`` of ``exp(w)`` satisfy ``pi(r') < e(r') < s(w) <= pi(w)`` (program
order: a referenced read is completed before the write starts), so by induction
``val(r') = req(r')``, hence ``content(w) = exp(w)[req] = req(r)`` by (V); INIT likewise.
So every observed read returns its observation. QED.
Note that (V) alone could accept a *circular* justification (``r`` reads ``w`` fed by
``r'`` which reads ``w'`` fed by ``r``); with ``R = <_L`` (i) plus program order excludes it
(``e(r') < s(w) < e(r) < s(w') < e(r')``), so the theorem needs no extra acyclicity check.

Antitonicity. (V) does not mention ``R``; (i)-(iii) only get harder when pairs are added
to ``R``. So ``R subset R'`` implies ``F(R') => F(R)``. Hence a lower bound ``R0`` of ``<_L``
gives a sound cut (``not F(R0)`` => infeasible) and an upper bound ``R1`` gives a sound
acceptance (``F(R1)`` => feasible), exactly as for constant data.

Relevant actions. Relevant blocks/reads are the closure of the observed reads under
"block of a relevant read is relevant" and "read leaves of ``exp(w)`` for writes ``w`` on a
relevant block are relevant". Only these can ever be required. On a relevant block all
writes are relevant. ``R`` is only ever needed on relevant actions.

The search (``DepModel.solve``). Depth-first over required-but-unassigned reads, always
the one with the fewest currently admissible sources (dynamic MRV). A source is tried
when (i) holds, its bindings agree with the existing requirements, and the incremental
(ii)/(iii) checks on bitmask clusters pass (the checks are monotone in ``S`` and ``rf``, so
cutting on a violation is exact). New bindings join the worklist. The match
``exp(w) ~ t`` is cached per ``(w, t)``. Cost per search node ``O(|pending| * W + W)``
word operations; the search branches only on reads with >= 2 admissible sources. When
sources are unambiguous (e.g. ``"*"`` data, distinct tags), it is polynomial:
``O(|S| (|S| + W))`` per evaluation. In general it is NP-hard (it contains the
constant-data case, Gibbons-Korach).

Witnesses. ``solve`` returns the ``rf`` it found; ``verify`` rechecks a witness against
another relation in ``O(m^2 / wordsize)``. Since (V) does not depend on ``R``, a witness
valid for ``R`` stays a witness for any ``R'`` on which (i)-(iii) still hold: the
enumerators try the previous witness first and search only when it breaks.

Static pins (``static_pins``). Using term structure before enumerating: for a read that is
*certainly* required with ``t`` (observed, or bound identically by every viable source of a
certainly-required read), compute the sources that are viable (matching, not excluded by
(i)/(ii) under the poset, and whose bound reads are recursively viable; circular
justification is treated optimistically, which over-approximates viability and is
therefore safe). If exactly one write ``w`` is viable, every feasible ``L`` has
``s(w) < e(r)`` (condition (i)): add the edge ``start(w) -> done(r)``. If only INIT is
viable, every feasible ``L`` has ``s(r) < e(w)`` for every write ``w`` of the block
(condition (ii) on singletons): add ``start(r) -> done(w)``. No viable source, conflicting
certain requirements, or an edge closing a cycle: nothing is feasible. Iterated to a
fixpoint. The pinned poset ``Q`` satisfies ``LinFeas(P) subset Lin(Q) subset Lin(P)``.
"""

from __future__ import annotations

from typing import Sequence

from abio import terms as T
from abio.model import Setup

INIT = -1


def _match(e: T.Node, t: T.Node, binds: dict) -> bool:
    """Match expanded expression ``e`` (``Ref`` leaves are reads) against term ``t``."""
    if isinstance(e, T.Pair):
        return isinstance(t, T.Pair) and _match(e.left, t.left, binds) and _match(e.right, t.right, binds)
    if isinstance(e, T.Ref):
        cur = binds.get(e.action)
        if cur is None:
            binds[e.action] = t
            return True
        return cur == t
    return e == t


class Block:
    """Relevant actions of one relevant block: writes ``0..W-1`` then reads ``W..n-1``."""

    __slots__ = ("block", "ids", "W", "n", "full", "snode", "enode", "exp", "init", "gids")

    def __init__(self, setup: Setup, block: int, writes: list[str], reads: list[str], exp: dict) -> None:
        P = setup.poset
        self.block = block
        self.ids = writes + reads
        self.W = len(writes)
        self.n = len(self.ids)
        self.full = (1 << self.n) - 1
        self.snode = [P.start_node[a] for a in self.ids]
        self.enode = [P.done_node[a] for a in self.ids]
        self.exp = [exp[w] for w in writes]
        self.init = setup.init[block]
        self.gids: list[int] = []

    def prec_from_positions(self, pos: Sequence[int]) -> list[int]:
        s = [pos[x] for x in self.snode]
        e = [pos[x] for x in self.enode]
        out = []
        for x in range(self.n):
            ex = e[x]
            m = 0
            for y in range(self.n):
                if s[y] > ex:
                    m |= 1 << y
            out.append(m)
        return out

    def prec_from_reach(self, reach: Sequence[int]) -> list[int]:
        """Lower bound: ``x R y`` iff ``e(x) <_Q s(y)`` (``reach`` = strict up-sets)."""
        out = []
        for x in range(self.n):
            rx = reach[self.enode[x]]
            m = 0
            for y in range(self.n):
                if y != x and (rx >> self.snode[y]) & 1:
                    m |= 1 << y
            out.append(m)
        return out


class DepModel:
    """Per-setup precomputation: expanded expressions, relevant closure, match cache."""

    def __init__(self, setup: Setup) -> None:
        if setup.features().rcw:
            raise ValueError("opus_dep: RCW is not supported")
        self.setup = setup
        acts = setup.actions
        exp: dict[str, T.Node] = {}

        def exp_of(w: str) -> T.Node:
            if w not in exp:
                a = acts[w]
                exp[w] = T.Unk(w) if a.data is None else T.substitute(a.data, look)
            return exp[w]

        def look(x: str) -> T.Node:
            return T.Ref(x) if acts[x].kind == "read" else exp_of(x)

        writes_of: dict[int, list[str]] = {}
        for a in acts.values():
            if a.kind == "write":
                writes_of.setdefault(a.block, []).append(a.id)
                exp_of(a.id)
        self.exp = exp
        rel_reads = {a.id for a in acts.values() if a.kind == "read" and a.observed is not None}
        rel_blocks: set[int] = set()
        todo = sorted({acts[r].block for r in rel_reads})
        while todo:
            b = todo.pop()
            if b in rel_blocks:
                continue
            rel_blocks.add(b)
            for w in writes_of.get(b, []):
                for r in T.refs(exp[w]):
                    if r not in rel_reads:
                        rel_reads.add(r)
                    if acts[r].block not in rel_blocks:
                        todo.append(acts[r].block)
        self.blocks: list[Block] = []
        self.rblock: list[int] = []
        self.rloc: list[int] = []
        self.rid: list[str] = []
        self.gid: dict[str, int] = {}
        for b in sorted(rel_blocks):
            reads = [a.id for a in acts.values() if a.kind == "read" and a.block == b and a.id in rel_reads]
            bp = Block(setup, b, writes_of.get(b, []), reads, exp)
            bi = len(self.blocks)
            for j, r in enumerate(reads):
                g = len(self.rid)
                self.gid[r] = g
                self.rid.append(r)
                self.rblock.append(bi)
                self.rloc.append(bp.W + j)
                bp.gids.append(g)
            self.blocks.append(bp)
        self.obs_gids = [self.gid[a.id] for a in acts.values() if a.kind == "read" and a.observed is not None]
        self.req0 = {g: acts[self.rid[g]].observed for g in self.obs_gids}
        self._cand: dict = {}
        self.hopeless = any(not self.cand(g, t) for g, t in self.req0.items())

    @property
    def trivial(self) -> bool:
        return not self.obs_gids

    # ------------------------------------------------------------------ value part (V)

    def cand(self, g: int, t: T.Term) -> list[tuple[int, tuple]]:
        """Value-compatible sources of read ``g`` required with ``t``: ``(src, bindings)``."""
        key = (g, t)
        c = self._cand.get(key)
        if c is None:
            bp = self.blocks[self.rblock[g]]
            c = []
            for w, e in enumerate(bp.exp):
                binds: dict = {}
                if _match(e, t, binds):
                    c.append((w, tuple((self.gid[r], v) for r, v in binds.items())))
            if bp.init == t:
                c.append((INIT, ()))
            self._cand[key] = c
        return c

    # ------------------------------------------------------------------ F(R)

    def solve(self, prec: Sequence[Sequence[int]]) -> dict | None:
        """A witness ``{gid: source}`` of ``F(prec)``, or None. ``prec[bi][x]`` = successor mask."""
        blocks = self.blocks
        nb = len(blocks)
        for bi in range(nb):
            p, W = prec[bi], blocks[bi].W
            for a in range(W):
                pa = p[a]
                for b in range(a + 1, W):
                    if (pa >> b) & 1 and (p[b] >> a) & 1:
                        return None
        wany = []
        Ms, outs = [], []
        for bi in range(nb):
            p, W = prec[bi], blocks[bi].W
            m = 0
            for a in range(W):
                m |= p[a]
            wany.append(m)
            Ms.append([1 << w for w in range(W)])
            outs.append([p[w] for w in range(W)])
        m0 = [0] * nb
        req = dict(self.req0)
        pending = list(self.obs_gids)
        assign: dict[int, int] = {}
        rblock, rloc, cand = self.rblock, self.rloc, self.cand
        found: list[dict] = []

        def options(g: int) -> list:
            bi, x = rblock[g], rloc[g]
            pr = prec[bi][x]
            res = []
            for src, binds in cand(g, req[g]):
                if src == INIT:
                    if (wany[bi] >> x) & 1:
                        continue
                elif (pr >> src) & 1:  # (i)
                    continue
                res.append((src, binds))
            return res

        def rec() -> bool:
            if not pending:
                found.append(dict(assign))
                return True
            best, bo = -1, None
            for k, g in enumerate(pending):
                o = options(g)
                if bo is None or len(o) < len(bo):
                    best, bo = k, o
                    if len(o) <= 1:
                        break
            if not bo:
                return False
            g = pending.pop(best)
            bi, x = rblock[g], rloc[g]
            bit = 1 << x
            pr = prec[bi][x]
            M, out, W = Ms[bi], outs[bi], blocks[bi].W
            for src, binds in bo:
                new = []
                ok = True
                for g2, t2 in binds:
                    cur = req.get(g2)
                    if cur is None:
                        new.append((g2, t2))
                    elif cur != t2:
                        ok = False
                        break
                if not ok:
                    continue
                if src == INIT:
                    if any((o >> x) & 1 for o in out):  # (ii)
                        continue
                    m0[bi] |= bit
                    saved = None
                else:
                    no = out[src] | pr
                    if no & m0[bi]:  # (ii)
                        continue
                    nm = M[src] | bit
                    bad = False
                    for d in range(W):
                        if d != src and (no & M[d]) and (out[d] & nm):  # (iii)
                            bad = True
                            break
                    if bad:
                        continue
                    saved = (out[src], M[src])
                    out[src], M[src] = no, nm
                for g2, t2 in new:
                    req[g2] = t2
                    pending.append(g2)
                assign[g] = src
                if rec():
                    return True
                del assign[g]
                for g2, _ in new:
                    del req[g2]
                if new:
                    del pending[len(pending) - len(new):]
                if saved is None:
                    m0[bi] ^= bit
                else:
                    out[src], M[src] = saved
            pending.insert(best, g)
            return False

        return found[0] if rec() else None

    def feasible(self, prec: Sequence[Sequence[int]]) -> bool:
        return self.solve(prec) is not None

    def _clusters(self, witness: dict, prec: Sequence[Sequence[int]]):
        """Per block: (members, out, m0) of the clusters of ``witness`` under ``prec``,
        or None if (i) fails for some read."""
        res = []
        per_block: list[list[tuple[int, int]]] = [[] for _ in self.blocks]
        for g, src in witness.items():
            per_block[self.rblock[g]].append((self.rloc[g], src))
        for bi, bp in enumerate(self.blocks):
            p = prec[bi]
            M = [1 << w for w in range(bp.W)]
            out = [p[w] for w in range(bp.W)]
            m0 = 0
            for x, src in per_block[bi]:
                if src == INIT:
                    m0 |= 1 << x
                else:
                    if (p[x] >> src) & 1:
                        return None
                    M[src] |= 1 << x
                    out[src] |= p[x]
            res.append((M, out, m0))
        return res

    def verify(self, witness: dict, prec: Sequence[Sequence[int]]) -> bool:
        """Does ``witness`` (satisfying (V)) also satisfy (i)-(iii) under ``prec``?"""
        cl = self._clusters(witness, prec)
        if cl is None:
            return False
        for M, out, m0 in cl:
            W = len(M)
            for c in range(W):
                if out[c] & m0:
                    return False
                for d in range(c + 1, W):
                    if (out[c] & M[d]) and (out[d] & M[c]):
                        return False
        return True

    def branch_pair(self, witness: dict, r1: Sequence[Sequence[int]], r0: Sequence[Sequence[int]]):
        """For a witness valid under ``r0`` but not under ``r1 >= r0``: a pair ``(bi, x, y)``
        with ``x r1 y``, not ``x r0 y``, involved in a violation (so it is undecided)."""
        per_block: list[list[tuple[int, int]]] = [[] for _ in self.blocks]
        for g, src in witness.items():
            per_block[self.rblock[g]].append((self.rloc[g], src))
        for bi, bp in enumerate(self.blocks):
            p1, p0 = r1[bi], r0[bi]
            W = bp.W
            M = [1 << w for w in range(W)]
            m0 = 0
            for x, src in per_block[bi]:
                if src == INIT:
                    m0 |= 1 << x
                else:
                    if (p1[x] >> src) & 1 and not (p0[x] >> src) & 1:
                        return bi, x, src
                    M[src] |= 1 << x

            def pairs(A: int, B: int):
                for x in range(bp.n):
                    if (A >> x) & 1:
                        hit = p1[x] & B
                        for y in range(bp.n):
                            if (hit >> y) & 1:
                                yield x, y

            for c in range(W):
                for x, y in pairs(M[c], m0):
                    if not (p0[x] >> y) & 1:
                        return bi, x, y
                for d in range(c + 1, W):
                    cd = list(pairs(M[c], M[d]))
                    dc = list(pairs(M[d], M[c]))
                    if cd and dc:
                        for x, y in cd + dc:
                            if not (p0[x] >> y) & 1:
                                return bi, x, y
        return None

    # ------------------------------------------------------------------ fixed L

    def feasible_positions(self, pos: Sequence[int]) -> bool:
        if self.trivial:
            return True
        if self.hopeless:
            return False
        return self.feasible([bp.prec_from_positions(pos) for bp in self.blocks])


def is_feasible_fast(setup: Setup, order: Sequence[int], model: DepModel | None = None) -> bool:
    """Exact fixed-``L`` feasibility (``F(<_L)``; proof in the module docstring).

    Equivalent to ``abio.semantics.is_feasible`` for Read/Write setups with any write
    expressions. Pass a prebuilt ``model`` to amortize the precomputation.
    """
    m = model if model is not None else DepModel(setup)
    pos = [0] * len(order)
    for i, x in enumerate(order):
        pos[x] = i
    return m.feasible_positions(pos)


# ---------------------------------------------------------------------- posets / pins


def topo(n: int, succs: Sequence[Sequence[int]]) -> list[int] | None:
    import heapq

    indeg = [0] * n
    for x in range(n):
        for y in succs[x]:
            indeg[y] += 1
    ready = [x for x in range(n) if indeg[x] == 0]
    heapq.heapify(ready)
    out = []
    while ready:
        x = heapq.heappop(ready)
        out.append(x)
        for y in succs[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(ready, y)
    return out if len(out) == n else None


def reach_of(n: int, succs: Sequence[Sequence[int]]) -> list[int]:
    """``reach[x]`` = bitmask of nodes strictly above ``x``."""
    order = topo(n, succs)
    assert order is not None
    reach = [0] * n
    for x in reversed(order):
        m = 0
        for y in succs[x]:
            m |= reach[y] | (1 << y)
        reach[x] = m
    return reach


def static_pins(model: DepModel) -> list[tuple[int, int]] | None:
    """Edges every feasible ``L`` satisfies (module docstring, "Static pins"), or None if
    no ``L`` is feasible. Deterministic."""
    if model.trivial:
        return []
    if model.hopeless:
        return None
    P = model.setup.poset
    n = len(P)
    succs = [list(s) for s in P.succs]
    edges: list[tuple[int, int]] = []
    blocks = model.blocks
    while True:
        reach = reach_of(n, succs)
        memo: dict = {}

        def scands(g: int, t: T.Term) -> list:
            bp = blocks[model.rblock[g]]
            x = model.rloc[g]
            er, sr = bp.enode[x], bp.snode[x]
            res = []
            for src, binds in model.cand(g, t):
                if src == INIT:
                    if any((reach[bp.enode[w]] >> sr) & 1 for w in range(bp.W)):
                        continue
                elif (reach[er] >> bp.snode[src]) & 1:
                    continue
                res.append((src, binds))
            return res

        def viable(g: int, t: T.Term) -> bool:
            key = (g, t)
            v = memo.get(key)
            if v is not None:
                return v
            memo[key] = True  # optimistic on cycles: over-approximation, safe
            v = any(all(viable(g2, t2) for g2, t2 in b) for _, b in scands(g, t))
            memo[key] = v
            return v

        certain = dict(model.req0)
        work = list(model.obs_gids)
        new_edges: list[tuple[int, int]] = []
        while work:
            g = work.pop(0)
            t = certain[g]
            V = []
            for src, b in scands(g, t):
                if all(certain.get(g2, t2) == t2 for g2, t2 in b) and all(viable(g2, t2) for g2, t2 in b):
                    V.append((src, b))
            if not V:
                return None
            bp = blocks[model.rblock[g]]
            x = model.rloc[g]
            if len(V) == 1:
                src = V[0][0]
                if src == INIT:
                    for w in range(bp.W):
                        new_edges.append((bp.snode[x], bp.enode[w]))
                else:
                    new_edges.append((bp.snode[src], bp.enode[x]))
            common = dict(V[0][1])
            for _, b in V[1:]:
                bd = dict(b)
                common = {k: v for k, v in common.items() if bd.get(k) == v}
            for g2, t2 in common.items():
                if g2 not in certain:
                    certain[g2] = t2
                    work.append(g2)
        added = False
        for u, v in new_edges:
            if u == v or (reach[u] >> v) & 1:
                continue
            if (reach[v] >> u) & 1:
                return None  # a necessary edge closes a cycle
            succs[u].append(v)
            edges.append((u, v))
            added = True
            reach = reach_of(n, succs)
        if not added:
            return edges
