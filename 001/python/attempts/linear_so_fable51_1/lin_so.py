"""Feasible linearizations for case ``so`` (sync points and observed reads).

Method
------
``Lin(P)`` is enumerated by depth-first backtracking over the minimal elements of the
trace poset, with an explicit stack (lazy, shallow, deterministic: candidates are tried
in increasing node index).

Feasibility (spec §5) reduces to an ordering problem.  Under a linearization ``L`` an
action ``a`` can take effect before ``b`` iff ``pos(start(a)) < pos(end(b))``; so the
effect orders realisable by some choice of distinct effect points are exactly the
linear extensions of the interval order ``a << b  iff  pos(end(a)) < pos(start(b))``.
``L`` is feasible iff one of them makes every observed read return its observed term.

Two facts make the check incremental while the prefix of ``L`` is being built:

* once two actions have started, their interval-order relation is fixed for good, and
  an action that starts later is forced after every action that has already ended;
* hence an observed read is decidable as soon as its ``done`` node is placed, and a
  linearization is feasible iff the check passes at each such moment (the check at the
  last observed ``done`` is also sufficient; earlier ones are necessary conditions).

Only "relevant" actions take part in a check: observed reads, every write on their
blocks, the reads those writes (transitively) reference, the writes on *their* blocks,
and so on.  The result of a check depends only on the interval order among the started
relevant actions, encoded as the sequence of *runs* (maximal groups of consecutive
starts, or consecutive dones, of relevant actions; a bitmask per run).  That encoding is
the key of two memo tables: check results, and dead DFS states ``(placed set, runs)``
whose whole subtree yields nothing.

The optional counter uses the same state ``(placed set, runs)`` in a level-by-level
dynamic programme for ``|LinFeas(P)|``, a plain ideal DP (or the multinomial
coefficient when ``K = 0``) for ``|Lin(P)|``.
"""

from __future__ import annotations

import math
import sys
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.registry import register
from harness.terms import Unk, refs, substitute

_CAPS = Capabilities(rcw=False, sync=True, observed_reads=True)
_MEMO_CAP = 1_000_000


class _Problem:
    """Precomputed tables for one setup, plus the enumeration / counting drivers."""

    def __init__(self, setup: Setup) -> None:
        self.setup = setup
        poset = setup.poset
        self.n = n = len(poset)
        self.preds = poset.preds
        self.succs = poset.succs
        self.pred_mask = [sum(1 << p for p in ps) for ps in poset.preds]
        actions = setup.actions
        self.actions = actions
        self.init = setup.init

        # Reads that the content of a write depends on, transitively through write refs.
        deps_cache: dict[str, frozenset[str]] = {}

        def read_deps(aid: str) -> frozenset[str]:
            got = deps_cache.get(aid)
            if got is not None:
                return got
            a = actions[aid]
            out: set[str] = set()
            if a.data is not None:
                for x in refs(a.data):
                    if actions[x].kind == "read":
                        out.add(x)
                    else:
                        out |= read_deps(x)
            got = frozenset(out)
            deps_cache[aid] = got
            return got

        # Relevant actions R*: closure from the observed reads.
        obs_ids = [a.id for a in actions.values() if a.kind == "read" and a.observed is not None]
        rel_blocks: set[int] = set()
        rel_reads: set[str] = set()
        queue = list(obs_ids)
        while queue:
            r = queue.pop()
            if r in rel_reads:
                continue
            rel_reads.add(r)
            b = actions[r].block
            if b in rel_blocks:
                continue
            rel_blocks.add(b)
            for w in actions.values():
                if w.kind == "write" and w.block == b:
                    for r2 in read_deps(w.id):
                        if r2 not in rel_reads:
                            queue.append(r2)
        ids = [
            a.id
            for a in actions.values()
            if a.id in rel_reads or (a.kind == "write" and a.block in rel_blocks)
        ]
        self.ids = ids
        self.m = m = len(ids)
        local = {aid: i for i, aid in enumerate(ids)}
        self.local = local
        self.is_read = [actions[aid].kind == "read" for aid in ids]
        self.observed = [actions[aid].observed if actions[aid].kind == "read" else None for aid in ids]
        self.block = [actions[aid].block for aid in ids]
        self.obs_local = [i for i in range(m) if self.observed[i] is not None]
        self.writes_on_block = {
            b: [i for i in range(m) if not self.is_read[i] and self.block[i] == b] for b in rel_blocks
        }
        self.read_deps_local = [
            [] if self.is_read[i] else sorted(local[r] for r in read_deps(aid)) for i, aid in enumerate(ids)
        ]
        self.dep_writes = [0] * m
        for w in range(m):
            for r in self.read_deps_local[w]:
                self.dep_writes[r] |= 1 << w

        # Node tables: which poset nodes are endpoints of relevant actions.
        self.node_local = [-1] * n
        self.node_done = [False] * n
        self.node_obs_done = [False] * n
        for x in range(n):
            k = poset.kind[x]
            if k in ("start", "done"):
                j = local.get(poset.action[x])
                if j is not None:
                    self.node_local[x] = j
                    if k == "done":
                        self.node_done[x] = True
                        if self.observed[j] is not None:
                            self.node_obs_done[x] = True

        self.check_memo: dict[tuple[int, ...], bool] = {}
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * m + 500))

    # ------------------------------------------------------------------ feasibility

    def _feasible(self, srun: list[int], drun: list[int]) -> bool:
        """Is there an effect order of the started relevant actions, extending the
        interval order given by the runs, under which every *closed* observed read
        returns its observed term?"""
        queue = [r for r in self.obs_local if drun[r] != -1]
        rel = 0
        for r in queue:
            rel |= 1 << r
        seen: set[int] = set()
        writes_on_block = self.writes_on_block
        block = self.block
        rdl = self.read_deps_local
        i = 0
        while i < len(queue):
            r = queue[i]
            i += 1
            b = block[r]
            if b in seen:
                continue
            seen.add(b)
            for w in writes_on_block[b]:
                if srun[w] != -1 and not rel >> w & 1:
                    rel |= 1 << w
                    for r2 in rdl[w]:
                        if not rel >> r2 & 1:
                            rel |= 1 << r2
                            queue.append(r2)
        elems = [j for j in range(self.m) if rel >> j & 1]
        pred: dict[int, int] = {}
        for b_ in elems:
            sb = srun[b_]
            pm = 0
            for a in elems:
                da = drun[a]
                if da != -1 and da < sb:
                    pm |= 1 << a
            pred[b_] = pm
        return self._search(rel, elems, pred)

    def _search(self, rel: int, elems: list[int], pred: dict[int, int]) -> bool:
        is_read = self.is_read
        observed = self.observed
        block = self.block
        writes_on_block = self.writes_on_block
        dep_writes = self.dep_writes
        actions = self.actions
        ids = self.ids
        local = self.local
        blocks_of = sorted({block[j] for j in elems})
        bidx = {b: i for i, b in enumerate(blocks_of)}
        reads = [j for j in elems if is_read[j]]
        rpos = {j: i for i, j in enumerate(reads)}
        n_reads = len(reads)
        elems_w_first = [j for j in elems if not is_read[j]] + reads
        failed: set = set()

        def value_of(aid: str, results: tuple):
            a = actions[aid]
            if a.kind == "read":
                return results[rpos[local[aid]]]
            if a.data is None:
                return Unk(aid)
            return substitute(a.data, lambda x: value_of(x, results))

        def rec(placed: int, blocks: tuple, results: tuple) -> bool:
            if placed == rel:
                return True
            free = rel & ~placed
            key = (
                placed,
                blocks,
                tuple(results[i] if dep_writes[reads[i]] & free else None for i in range(n_reads)),
            )
            if key in failed:
                return False
            minimal = [x for x in elems_w_first if free >> x & 1 and not pred[x] & free]
            # Safe greedy moves: a matching observed read, or a read nobody needs any more.
            greedy = -1
            for x in minimal:
                if not is_read[x]:
                    continue
                obs = observed[x]
                if obs is not None:
                    if blocks[bidx[block[x]]] == obs:
                        greedy = x
                        break
                    for w in writes_on_block[block[x]]:
                        if free >> w & 1 and not pred[w] >> x & 1:
                            break
                    else:
                        failed.add(key)
                        return False
                elif not dep_writes[x] & free:
                    greedy = x
                    break
            if greedy >= 0:
                x = greedy
                i = rpos[x]
                nres = results[:i] + (blocks[bidx[block[x]]],) + results[i + 1 :]
                ok = rec(placed | (1 << x), blocks, nres)
                if not ok:
                    failed.add(key)
                return ok
            for x in minimal:
                bit = 1 << x
                if is_read[x]:
                    if observed[x] is not None:
                        continue  # mismatching observed read: cannot be placed now
                    i = rpos[x]
                    nres = results[:i] + (blocks[bidx[block[x]]],) + results[i + 1 :]
                    if rec(placed | bit, blocks, nres):
                        return True
                else:
                    val = value_of(ids[x], results)
                    bi = bidx[block[x]]
                    if rec(placed | bit, blocks[:bi] + (val,) + blocks[bi + 1 :], results):
                        return True
            failed.add(key)
            return False

        init_blocks = tuple(self.init[b] for b in blocks_of)
        return rec(0, init_blocks, (None,) * n_reads)

    def _derive(self, runs: tuple[int, ...]) -> tuple[list[int], list[int]]:
        m = self.m
        srun = [-1] * m
        drun = [-1] * m
        for i, bits in enumerate(runs):
            arr = srun if i % 2 == 0 else drun
            while bits:
                low = bits & -bits
                arr[low.bit_length() - 1] = i
                bits ^= low
        return srun, drun

    # ------------------------------------------------------------------ enumeration

    def iterate(self) -> Iterator[tuple[int, ...]]:
        n = self.n
        if n == 0:
            yield ()
            return
        succs = self.succs
        indeg = [len(p) for p in self.preds]
        ready = {x for x in range(n) if indeg[x] == 0}
        node_local = self.node_local
        node_done = self.node_done
        node_obs_done = self.node_obs_done
        m = self.m
        srun = [-1] * m
        drun = [-1] * m
        runs: list[int] = []
        new_stack: list[bool] = []
        dead: set = set()
        check_memo = self.check_memo
        placed = 0
        order: list[int] = []
        cand_stack: list[list[int]] = [sorted(ready)]
        pos_stack: list[int] = [0]
        hit_stack: list[bool] = [False]

        def unplace() -> None:
            nonlocal placed
            x = order.pop()
            for y in succs[x]:
                if indeg[y] == 0:
                    ready.discard(y)
                indeg[y] += 1
            ready.add(x)
            placed ^= 1 << x
            j = node_local[x]
            if j >= 0:
                if new_stack.pop():
                    runs.pop()
                else:
                    runs[-1] ^= 1 << j
                if node_done[x]:
                    drun[j] = -1
                else:
                    srun[j] = -1

        while cand_stack:
            cands = cand_stack[-1]
            i = pos_stack[-1]
            if i < len(cands):
                x = cands[i]
                pos_stack[-1] = i + 1
                j = node_local[x]
                if j >= 0:
                    bit = 1 << j
                    if node_done[x]:
                        if runs and len(runs) % 2 == 0:
                            runs[-1] |= bit
                            new = False
                        else:
                            runs.append(bit)
                            new = True
                        drun[j] = len(runs) - 1
                    else:
                        if len(runs) % 2 == 1:
                            runs[-1] |= bit
                            new = False
                        else:
                            runs.append(bit)
                            new = True
                        srun[j] = len(runs) - 1
                    rk = tuple(runs)
                    key = (placed | (1 << x), rk)
                    ok = key not in dead
                    if ok and node_obs_done[x]:
                        r = check_memo.get(rk)
                        if r is None:
                            r = self._feasible(srun, drun)
                            if len(check_memo) > _MEMO_CAP:
                                check_memo.clear()
                            check_memo[rk] = r
                        if not r:
                            if len(dead) > _MEMO_CAP:
                                dead.clear()
                            dead.add(key)
                            ok = False
                    if not ok:
                        if new:
                            runs.pop()
                        else:
                            runs[-1] ^= bit
                        if node_done[x]:
                            drun[j] = -1
                        else:
                            srun[j] = -1
                        continue
                    new_stack.append(new)
                placed |= 1 << x
                order.append(x)
                ready.discard(x)
                for y in succs[x]:
                    indeg[y] -= 1
                    if indeg[y] == 0:
                        ready.add(y)
                if len(order) == n:
                    yield tuple(order)
                    hit_stack[-1] = True
                    unplace()
                    continue
                cand_stack.append(sorted(ready))
                pos_stack.append(0)
                hit_stack.append(False)
            else:
                cand_stack.pop()
                pos_stack.pop()
                hit = hit_stack.pop()
                if not order:
                    return
                if hit:
                    hit_stack[-1] = True
                elif node_local[order[-1]] >= 0:
                    if len(dead) > _MEMO_CAP:
                        dead.clear()
                    dead.add((placed, tuple(runs)))
                unplace()

    # ------------------------------------------------------------------ counting

    def count_lin(self) -> int:
        n = self.n
        if self.setup.sync_points == 0:
            total = math.factorial(n)
            for c in self.setup.poset.chains:
                total //= math.factorial(len(c))
            return total
        pm = self.pred_mask
        level: dict[int, int] = {0: 1}
        for _ in range(n):
            nxt: dict[int, int] = {}
            for mask, c in level.items():
                for x in range(n):
                    b = 1 << x
                    if mask & b or pm[x] & ~mask:
                        continue
                    nm = mask | b
                    nxt[nm] = nxt.get(nm, 0) + c
            level = nxt
        return sum(level.values())

    def count_feasible(self) -> int:
        n = self.n
        if n == 0:
            return 1
        pm = self.pred_mask
        node_local = self.node_local
        node_done = self.node_done
        node_obs_done = self.node_obs_done
        check_memo = self.check_memo
        level: dict[tuple[int, tuple[int, ...]], int] = {(0, ()): 1}
        for _ in range(n):
            nxt: dict[tuple[int, tuple[int, ...]], int] = {}
            for (mask, runs), c in level.items():
                for x in range(n):
                    b = 1 << x
                    if mask & b or pm[x] & ~mask:
                        continue
                    j = node_local[x]
                    nr = runs
                    if j >= 0:
                        bit = 1 << j
                        if node_done[x]:
                            if runs and len(runs) % 2 == 0:
                                nr = runs[:-1] + (runs[-1] | bit,)
                            else:
                                nr = runs + (bit,)
                        else:
                            if len(runs) % 2 == 1:
                                nr = runs[:-1] + (runs[-1] | bit,)
                            else:
                                nr = runs + (bit,)
                        if node_obs_done[x]:
                            r = check_memo.get(nr)
                            if r is None:
                                srun, drun = self._derive(nr)
                                r = self._feasible(srun, drun)
                                check_memo[nr] = r
                            if not r:
                                continue
                    key = (mask | b, nr)
                    nxt[key] = nxt.get(key, 0) + c
            level = nxt
        return sum(level.values())


@register
class SoEnumerator(LinEnumerator):
    name = "fable51_1-so-enum"
    description = "DFS over poset minimal elements; interval-order feasibility checked at observed dones, dead states memoised"
    capabilities = _CAPS
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[tuple[int, ...]]:
        return _Problem(setup).iterate()


@register
class SoCounter(LinCounter):
    name = "fable51_1-so-count"
    description = "Level DP over (ideal, runs of relevant endpoints) for |LinFeas|; ideal DP or multinomial for |Lin|"
    capabilities = _CAPS

    def count(self, setup: Setup) -> CountResult:
        prob = _Problem(setup)
        lin = prob.count_lin()
        feas = prob.count_feasible() if prob.obs_local else lin
        return CountResult(linearizations=lin, feasible=feas, method="ideal-runs-dp")
