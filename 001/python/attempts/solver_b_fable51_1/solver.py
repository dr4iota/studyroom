"""Exact possibility-set solver for case ``b`` (no sync points, no observed reads).

Method
------
With ``K = 0`` the trace poset is a disjoint union of per-thread chains, and only the
*effect order* (the order of the actions' effect points) matters for the semantics.

* Under a fixed linearization ``L`` an effect order is realisable iff it is a linear
  extension of the interval order ``a < b  iff  pos(done(a)) < pos(start(b))``:
  the greedy choice ``pi(E_k) = max_{i<=k} pos(start(E_i)) + k*eps`` works exactly when
  no later action ends before an earlier one starts.
* Over all linearizations an effect order is realisable iff it is a linear extension of
  ``a < b  iff  same thread and done(a) precedes start(b) in program order``: the
  constraints ``start(E_i) < done(E_j)`` (``i < j``) together with program order are
  acyclic exactly then, since every cycle alternates one such edge with a program-order
  path ``done(y) -> start(z)``, i.e. ``y < z``.

So both modes reduce to: given a strict partial order ``<`` on the actions, compute the
read results and final contents over all of its linear extensions.

* Blocks whose writes never depend on reads ("static" components) have a closed form.
  A ``b``-write ``w`` can be the last write before read ``r`` iff ``r`` is not below
  ``w`` and no ``b``-write lies strictly between ``w`` and ``r``; ``r`` can see the
  initial content iff no ``b``-write is below ``r``; ``w`` can be the final writer iff no
  ``b``-write is above it; the initial content is final iff there is no ``b``-write.
* Blocks connected by data flow that contain a read-dependent write are solved by a
  memoised search over reachable states ``(down-set, block contents, live read values)``.
  Reads nobody references are not part of the search (dropping them does not change the
  achievable orders of the others); their results are collected at every state after
  which they could be inserted.  Contents of blocks that nothing can touch any more and
  values of reads no pending write needs are forgotten so that states merge.
"""

from __future__ import annotations

from typing import Iterator

from harness import terms as T
from harness.model import Action, Setup
from harness.poset import Linearization
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class DownsetSolver(Solver):
    name = "fable51_1-b-downset"
    description = (
        "Exact Poss over linear extensions of the effect-order poset: closed form for "
        "static blocks, memoised down-set search for read-dependent ones"
    )
    capabilities = SolverCapabilities(
        rcw=False,
        sync=False,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        results, final = _Problem(setup, linearization).run()
        return Outcomes(mode, True, results, final)


def _bits(m: int) -> Iterator[int]:
    """Indices of the set bits of ``m``, ascending."""
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


class _Problem:
    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.acts: list[Action] = list(setup.actions.values())
        acts = self.acts
        n = len(acts)
        self.n = n
        self.idx: dict[str, int] = {a.id: i for i, a in enumerate(acts)}

        # ---- the strict partial order on actions (bitmasks over action indices)
        self.pred = self._precedence(lin)
        self.succ = [0] * n
        for i in range(n):
            for j in _bits(self.pred[i]):
                self.succ[j] |= 1 << i

        # ---- write contents with references to earlier writes inlined:
        #      leaves are Const, Unk (a "*" write) and Ref(read id)
        self.flat: dict[str, T.Node] = {}
        self.need: list[frozenset[str]] = [frozenset()] * n  # reads the content depends on
        for i, a in enumerate(acts):
            if a.kind == "write":
                self.need[i] = frozenset(T.refs(self._flatten(a.id)))

        # ---- per-block action tables
        nb = setup.blocks
        self.bwrites = [0] * nb  # mask of writes of each block
        self.breads: list[list[int]] = [[] for _ in range(nb)]
        for i, a in enumerate(acts):
            if a.kind == "write":
                self.bwrites[a.block] |= 1 << i
            else:
                self.breads[a.block].append(i)

        self.results: dict[str, set[T.Term]] = {a.id: set() for a in acts if a.kind != "write"}
        self.final: dict[int, set[T.Term]] = {b: set() for b in range(nb)}

    # ------------------------------------------------------------------ setup

    def _precedence(self, lin: Linearization | None) -> list[int]:
        acts = self.acts
        n = len(acts)
        if lin is None:
            th = [a.thread for a in acts]
            st = [a.start for a in acts]
            dn = [a.done for a in acts]
        else:
            poset = self.setup.poset
            pos = poset.positions(lin)
            th = [0] * n
            st = [pos[poset.start_node[a.id]] for a in acts]
            dn = [pos[poset.done_node[a.id]] for a in acts]
        pred = [0] * n
        for i in range(n):
            m = 0
            si, ti = st[i], th[i]
            for j in range(n):
                if th[j] == ti and dn[j] < si:
                    m |= 1 << j
            pred[i] = m
        return pred

    def _flatten(self, aid: str) -> T.Node:
        t = self.flat.get(aid)
        if t is None:
            a = self.setup.actions[aid]
            if a.data is None:
                t = T.Unk(aid)
            else:
                t = T.substitute(a.data, self._inline)
            self.flat[aid] = t
        return t

    def _inline(self, x: str) -> T.Node:
        if self.setup.actions[x].kind == "read":
            return T.Ref(x)
        return self._flatten(x)

    # ------------------------------------------------------------------ driver

    def run(self) -> tuple[dict[str, set[T.Term]], dict[int, set[T.Term]]]:
        nb = self.setup.blocks
        parent = list(range(nb))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        acts, idx, need = self.acts, self.idx, self.need
        for i, a in enumerate(acts):
            if a.kind == "write" and need[i]:
                for r in need[i]:
                    rx, ry = find(a.block), find(acts[idx[r]].block)
                    if rx != ry:
                        parent[rx] = ry
        dynamic_roots = {find(a.block) for i, a in enumerate(acts) if a.kind == "write" and need[i]}
        comps: dict[int, list[int]] = {}
        for b in range(nb):
            comps.setdefault(find(b), []).append(b)
        for root, blocks in comps.items():
            if root in dynamic_roots:
                self._search(blocks)
            else:
                for b in blocks:
                    self._static(b)
        return self.results, self.final

    # ------------------------------------------------------------------ static blocks

    def _static(self, b: int) -> None:
        acts, pred, succ, flat = self.acts, self.pred, self.succ, self.flat
        wm = self.bwrites[b]
        init = self.setup.init[b]
        final = self.final[b]
        if wm == 0:
            final.add(init)
        writes = list(_bits(wm))
        for w in writes:
            if succ[w] & wm == 0:
                final.add(flat[acts[w].id])
        for r in self.breads[b]:
            s = self.results[acts[r].id]
            pr = pred[r]
            if pr & wm == 0:
                s.add(init)
            for w in writes:
                if (pred[w] >> r) & 1:  # r must take effect before w
                    continue
                if succ[w] & pr & wm:  # some b-write is forced between w and r
                    continue
                s.add(flat[acts[w].id])

    # ------------------------------------------------------------------ dynamic components

    def _search(self, blocks: list[int]) -> None:
        acts, pred, succ, need, flat, idx = self.acts, self.pred, self.succ, self.need, self.flat, self.idx
        results, final = self.results, self.final

        loc = {b: k for k, b in enumerate(blocks)}
        writes = [i for b in blocks for i in _bits(self.bwrites[b])]
        reads = sorted({idx[r] for w in writes for r in need[w]})
        rl = {i: k for k, i in enumerate(reads)}
        members = writes + reads
        rel = 0
        for i in members:
            rel |= 1 << i
        lazy = [i for b in blocks for i in self.breads[b] if i not in rl]
        nreads = len(reads)

        needers = [0] * nreads  # per referenced read: mask of the writes needing its value
        for w in writes:
            for r in need[w]:
                needers[rl[idx[r]]] |= 1 << w
        rpred = {i: pred[i] & rel for i in members + lazy}
        rsucc = {i: succ[i] & rel for i in members + lazy}
        block_rel = {b: 0 for b in blocks}
        for i in members:
            block_rel[acts[i].block] |= 1 << i
        lazy_by_block = {b: [i for i in lazy if acts[i].block == b] for b in blocks}
        lazy_info = [(acts[i].id, loc[acts[i].block]) for i in lazy]

        # per member: (is_read, local block, read slot, term, slots of needed reads)
        info: dict[int, tuple] = {}
        for i in members:
            a = acts[i]
            if a.kind == "write":
                slots = {r: rl[idx[r]] for r in need[i]}
                info[i] = (False, loc[a.block], -1, a.id, flat[a.id], slots)
            else:
                info[i] = (True, loc[a.block], rl[i], a.id, None, None)

        def close(D: int, mem: list) -> None:
            """Record and forget the contents of blocks nothing can touch any more."""
            for k, b in enumerate(blocks):
                if mem[k] is None or block_rel[b] & ~D:
                    continue
                for j in lazy_by_block[b]:
                    if rsucc[j] & D == 0:  # this read may still be inserted later
                        break
                else:
                    final[b].add(mem[k])
                    mem[k] = None

        mem0 = [self.setup.init[b] for b in blocks]
        close(0, mem0)
        state0 = (0, tuple(mem0), (None,) * nreads)
        seen = {state0}
        stack = [state0]
        enabled_cache: dict[int, list[int]] = {}
        lazy_cache: dict[int, list[int]] = {}
        substitute = T.substitute

        while stack:
            D, mem, live = stack.pop()

            ins = lazy_cache.get(D)
            if ins is None:
                ins = [p for p, i in enumerate(lazy) if rpred[i] & ~D == 0 and rsucc[i] & D == 0]
                lazy_cache[D] = ins
            for p in ins:
                rid, k = lazy_info[p]
                results[rid].add(mem[k])

            if D == rel:
                for k, b in enumerate(blocks):
                    if mem[k] is not None:
                        final[b].add(mem[k])
                continue

            en = enabled_cache.get(D)
            if en is None:
                en = [i for i in members if not (D >> i) & 1 and rpred[i] & ~D == 0]
                enabled_cache[D] = en

            for i in en:
                is_read, k, slot, aid, term, slots = info[i]
                D2 = D | (1 << i)
                if is_read:
                    v = mem[k]
                    results[aid].add(v)
                    live2 = list(live)
                    live2[slot] = v
                    mem2 = list(mem)
                else:
                    if slots:
                        cur = live
                        v = substitute(term, lambda x, cur=cur, slots=slots: cur[slots[x]])
                    else:
                        v = term
                    mem2 = list(mem)
                    mem2[k] = v
                    live2 = list(live)
                for kk in range(nreads):
                    if live2[kk] is not None and needers[kk] & ~D2 == 0:
                        live2[kk] = None
                close(D2, mem2)
                st = (D2, tuple(mem2), tuple(live2))
                if st not in seen:
                    seen.add(st)
                    stack.append(st)
