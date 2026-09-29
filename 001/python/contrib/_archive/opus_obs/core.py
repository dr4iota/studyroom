"""Feasibility of observed reads for Read/Write registers: the theory and the fixed-``L`` test.

Scope: actions are Read and Write only; write data is a constant, ``"*"`` (the free symbol
``Unk(w)``) or an expression over constants and earlier *writes* (``static_content``);
``init[b]`` is a constant or ``Init(b)``. Terms are compared structurally. Sync is
irrelevant here: it only shapes ``Lin(P)``; feasibility is a property of one ``L``.

Notation. Fix ``L``. For an action ``x`` let ``s(x), e(x)`` be the positions of its two
endpoints (distinct integers). ``x < y`` (``x`` *precedes* ``y``) iff ``e(x) < s(y)``;
this is the interval order of ``L``.

Lemma 0 (effect orders = linear extensions of the interval order). A linear order of the
actions is an admissible effect order (``semantics.check_effects``) iff it extends
``<``. Necessity: if ``x < y`` then ``pi(x) <= e(x) < s(y) <= pi(y)``. Sufficiency: the
greedy walk ``t := max(t + eps, s(x))`` never passes ``e(x)``: the current ``t`` is
``s(z) + k eps`` for an earlier ``z`` (or ``s(x)`` itself); ``z`` earlier and the order
extends ``<`` means not ``x < z``, i.e. ``s(z) < e(x)`` (distinct integers), so
``t < e(x)``.

Lemma 1 (blocks are independent). The register of block ``b`` only sees the actions on
``b``. If each block has an admissible order of its own actions matching its
observations, the points chosen by the greedy walk per block lie in the open intervals
``(s, e)``; perturbing them to be pairwise distinct keeps each block's order, and sorting
all points gives one global admissible effect order. So ``L`` is feasible iff each block
is. Unobserved reads never constrain anything (a read changes no content, and its point
can be put anywhere in its interval), so per block only the *writes* ``W_b`` and the
*observed reads* ``R_b`` matter: the *relevant* actions.

Reads-from. In an effect order every observed read ``r`` reads from the last earlier write
(``rf(r) = w``) or from the initial content (``rf(r) = INIT``). It is consistent iff
``content(rf(r)) == obs(r)``: the *candidates* of ``r``. ``rf`` groups the block's
actions into *clusters*: ``C_w = {w} + rf^-1(w)`` for each write, and
``C_0 = rf^-1(INIT)``. In the effect order ``C_0`` comes first, then the clusters one
after another, each write before its readers (the readers of ``w`` lie between ``w`` and
the next write).

Theorem (fixed ``L``, fixed ``rf``). For clusters ``C, D`` write ``C -> D`` iff some
``x in C`` precedes some ``y in D``. ``rf`` is realizable by an admissible effect order iff

  (i)   ``not r < rf(r)`` for every read ``r`` with ``rf(r) = w`` (``s(w) < e(r)``);
  (ii)  ``not D -> C_0`` for every write cluster ``D`` (no action of a write cluster
        precedes a read of the initial content);
  (iii) no two write clusters ``C != D`` with ``C -> D`` and ``D -> C``.

Proof. Placing a cluster ``C`` with the greedy walk when the running instant is ``t``:
``w`` goes to ``max(t, s(w)) + eps`` and each reader ``r`` to ``max(t, s(w), s(r)) + 2eps``
(readers in any order); this succeeds iff ``t < d(C) := min_{x in C} e(x)`` and (i) holds,
and afterwards ``t = max(t, a(C))`` with ``a(C) := max_{x in C} s(x)``. Greedy is optimal
for a fixed cluster sequence (smaller ``t`` is never worse). So a sequence
``C_0, C_1, .., C_k`` works iff (i) holds and ``a(C_i) < d(C_j)`` for all ``i < j``
(including ``i = 0``). Now ``a(C) > d(D)`` iff some ``y in D`` has ``e(y) < s(x)`` for some
``x in C`` iff ``D -> C``. So "``C`` before ``D``" is allowed iff not ``D -> C``: the
write clusters must be ordered as a topological order of ``->`` and ``C_0`` must have no
incoming ``->`` (ii). A topological order exists iff ``->`` is acyclic, and a cycle
implies a 2-cycle (iii): ``C -> D`` iff ``d(C) < a(D)``; in a shortest cycle of length
``k >= 3`` take ``C_j`` with maximal ``a``; then ``d(C_{j-2}) < a(C_{j-1}) <= a(C_j)``,
so ``C_{j-2} -> C_j`` shortcuts the cycle. QED.

Corollary (the fixed-``L`` test). ``L`` is feasible iff every block has an ``rf`` from the
candidates satisfying (i)-(iii). (i)-(iii) are monotone: adding members to clusters or
pairs to ``<`` only creates violations. So a backtracking search that assigns reads one
at a time (fewest candidates first) and checks (ii)/(iii) incrementally is exact. The
check for one assignment costs ``O(|W_b|)`` word operations (clusters as bitmasks, ``->``
as "the union of the successor masks of ``C`` meets ``D``").

Cost of the test. Building the successor masks: ``O(n + sum_b |W_b + R_b|^2)``. The search
is ``O(|R_b| |W_b|)`` per branch; it branches only on reads with >= 2 candidates. When
every observed value identifies its write (unknown data ``"*"``, distinct constants), the
test is polynomial, ``O(|R_b| |W_b|)`` after the masks. With repeated constants the
problem is NP-complete in general (linearizability of a register with repeated values,
Gibbons-Korach 1997), so an exponential worst case in the number of ambiguous reads is
expected; in practice the search is tiny.

Relations other than an interval order. Every definition above makes sense for an
arbitrary relation ``R`` in place of ``<`` (``F(R)`` := "some ``rf`` satisfies (i)-(iii)
with ``R``"), and ``F`` is antitone: ``R subset R'`` implies ``F(R') => F(R)``. The
enumerators use this with lower bounds (pairs certainly in ``<`` for every completion) to
prune and with upper bounds (pairs not certainly out) to accept whole sub-posets.
"""

from __future__ import annotations

from typing import Sequence

from abio.model import Setup

INIT = -1


class BlockProblem:
    """Relevant actions of one block with at least one observed read.

    Local indices: writes ``0..W-1``, then observed reads ``W..W+R-1``. ``cand[j]`` lists
    the candidate sources of read ``W+j`` (write indices, ``INIT``).
    """

    __slots__ = ("block", "ids", "W", "R", "n", "cand", "order", "snode", "enode", "full")

    def __init__(self, setup: Setup, block: int, writes: list[str], reads: list[str]) -> None:
        P = setup.poset
        self.block = block
        self.ids = writes + reads
        self.W, self.R = len(writes), len(reads)
        self.n = self.W + self.R
        self.full = (1 << self.n) - 1
        contents = [setup.static_content(w) for w in writes]
        self.cand: list[list[int]] = []
        for r in reads:
            obs = setup.actions[r].observed
            c = [i for i, v in enumerate(contents) if v == obs]
            if setup.init[block] == obs:
                c.append(INIT)
            self.cand.append(c)
        # static search order: fewest candidates first (ties by index), deterministic
        self.order = sorted(range(self.R), key=lambda j: (len(self.cand[j]), j))
        self.snode = [P.start_node[a] for a in self.ids]
        self.enode = [P.done_node[a] for a in self.ids]

    # ---------------------------------------------------------------- F(R)

    def feasible(self, prec: Sequence[int]) -> bool:
        """``F(prec)``: is there an ``rf`` satisfying (i)-(iii)?

        ``prec[x]`` is the local bitmask of the actions ``y`` with ``x R y``.
        """
        W = self.W
        # singleton write clusters: (iii) may already fail for a non-interval relation
        for a in range(W):
            pa = prec[a]
            for b in range(a + 1, W):
                if (pa >> b) & 1 and (prec[b] >> a) & 1:
                    return False
        wprec_any = 0  # actions preceded by some write
        for a in range(W):
            wprec_any |= prec[a]
        cands: list[list[int]] = []
        for j in range(self.R):
            r = W + j
            pr = prec[r]
            cs = [w for w in self.cand[j] if w >= 0 and not (pr >> w) & 1]  # (i)
            if INIT in self.cand[j] and not (wprec_any >> r) & 1:  # (ii) for singletons
                cs.append(INIT)
            if not cs:
                return False
            cands.append(cs)
        order = sorted(range(self.R), key=lambda j: (len(cands[j]), j))
        M = [1 << w for w in range(W)]  # cluster members
        out = [prec[w] for w in range(W)]  # union of successor masks of the cluster
        m0 = 0  # readers of INIT
        R = self.R

        def rec(k: int) -> bool:
            nonlocal m0
            if k == R:
                return True
            j = order[k]
            r = W + j
            bit = 1 << r
            pr = prec[r]
            for c in cands[j]:
                if c == INIT:
                    if any((o >> r) & 1 for o in out):  # (ii)
                        continue
                    m0 |= bit
                    if rec(k + 1):
                        return True
                    m0 ^= bit
                else:
                    no = out[c] | pr
                    if no & m0:  # (ii): C_c -> C_0
                        continue
                    nm = M[c] | bit
                    bad = False
                    for d in range(W):
                        if d != c and (no & M[d]) and (out[d] & nm):  # (iii)
                            bad = True
                            break
                    if bad:
                        continue
                    oo, om = out[c], M[c]
                    out[c], M[c] = no, nm
                    if rec(k + 1):
                        return True
                    out[c], M[c] = oo, om
            return False

        return rec(0)

    def prec_from_positions(self, pos: Sequence[int]) -> list[int]:
        """Successor masks of the interval order of a full linearization."""
        s = [pos[x] for x in self.snode]
        e = [pos[x] for x in self.enode]
        n = self.n
        out = []
        for x in range(n):
            ex = e[x]
            m = 0
            for y in range(n):
                if s[y] > ex:
                    m |= 1 << y
            out.append(m)
        return out


class ObsModel:
    """Per-setup precomputation: the relevant blocks and their candidate lists."""

    def __init__(self, setup: Setup) -> None:
        feats = setup.features()
        if feats.rcw:
            raise ValueError("opus_obs: RCW is not supported")
        if setup.has_data_from_reads():
            raise ValueError("opus_obs: read-dependent write data is not supported")
        self.setup = setup
        by_block_w: dict[int, list[str]] = {}
        by_block_r: dict[int, list[str]] = {}
        for a in setup.actions.values():
            if a.kind == "write":
                by_block_w.setdefault(a.block, []).append(a.id)
            elif a.kind == "read" and a.observed is not None:
                by_block_r.setdefault(a.block, []).append(a.id)
        self.blocks = [BlockProblem(setup, b, by_block_w.get(b, []), by_block_r[b]) for b in sorted(by_block_r)]
        # observed reads with no candidate at all: nothing is feasible
        self.hopeless = any(not c for bp in self.blocks for c in bp.cand)

    @property
    def trivial(self) -> bool:
        return not self.blocks

    def feasible_positions(self, pos: Sequence[int]) -> bool:
        if self.hopeless:
            return False
        return all(bp.feasible(bp.prec_from_positions(pos)) for bp in self.blocks)


def is_feasible_fast(setup: Setup, order: Sequence[int], model: ObsModel | None = None) -> bool:
    """Exact fixed-``L`` feasibility (see the module docstring for the proof).

    Equivalent to ``abio.semantics.is_feasible`` for Read/Write setups whose write data
    does not depend on reads. Pass a prebuilt ``model`` to amortize the precomputation.
    """
    m = model if model is not None else ObsModel(setup)
    if m.trivial:
        return True
    pos = [0] * len(order)
    for i, x in enumerate(order):
        pos[x] = i
    return m.feasible_positions(pos)
