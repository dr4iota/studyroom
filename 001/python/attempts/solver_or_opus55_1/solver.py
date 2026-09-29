"""Exact possibility-set solver for case `or` (reads, writes, RCWs, observations, K = 0).

Reduction: a full schedule (L, pi) exists with effect order sigma iff sigma is a linear
extension of the precedence relation a < b  <=>  done(a) <_P start(b) (mode "all"), or
pos_L(done(a)) < pos_L(start(b)) (mode "fixed").  The solver then explores effect orders
with memoised DFS over states (executed set, block contents, live read values).  Each
state returns a bitset of the (id, value) / (block, value) facts produced by some
feasible completion from it, or None when no feasible completion exists.
"""

from __future__ import annotations

import sys

from harness import terms as T
from harness.model import Setup
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class OrSolver(Solver):
    name = "opus55_1-or-memo"
    description = "Memoised DFS over effect orders extending interval precedence (reads, writes, RCWs, observations)"
    capabilities = SolverCapabilities(
        rcw=True, sync=False, observed_reads=True, modes=frozenset({"all", "fixed"}), witnesses=False
    )

    def solve(self, setup: Setup, linearization=None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        acts = list(setup.actions.values())
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        P = setup.poset

        # ---------------------------------------------------------------- precedence
        pred_mask = [0] * n
        if linearization is None:
            nn = len(P)
            anc = [0] * nn
            for v in P.topological_order():
                m = 0
                for u in P.preds[v]:
                    m |= anc[u] | (1 << u)
                anc[v] = m
            for j, b in enumerate(acts):
                sb = anc[P.start_node[b.id]]
                m = 0
                for i, a in enumerate(acts):
                    if i != j and (sb >> P.done_node[a.id]) & 1:
                        m |= 1 << i
                pred_mask[j] = m
        else:
            pos = P.positions(linearization)
            for j, b in enumerate(acts):
                sb = pos[P.start_node[b.id]]
                m = 0
                for i, a in enumerate(acts):
                    if i != j and pos[P.done_node[a.id]] < sb:
                        m |= 1 << i
                pred_mask[j] = m

        # ---------------------------------------------------------------- dependencies
        def reads_of(e, seen_w):
            out = set()
            if e is None:
                return out
            for r in T.refs(e):
                k = idx[r]
                if acts[k].kind == "read":
                    out.add(k)
                elif k not in seen_w:
                    seen_w.add(k)
                    out |= reads_of(acts[k].data, seen_w)
            return out

        writer_reads = {}
        for i, a in enumerate(acts):
            if a.kind != "read":
                writer_reads[i] = reads_of(a.data, set()) | reads_of(a.expect, set())
        ref_reads = sorted(set().union(*writer_reads.values()) if writer_reads else set())
        slot = {k: s for s, k in enumerate(ref_reads)}
        dep_mask = [0] * len(ref_reads)
        for w, rs in writer_reads.items():
            for k in rs:
                dep_mask[slot[k]] |= 1 << w

        # static contents for writers whose content does not depend on reads
        content_reads = {}
        for i, a in enumerate(acts):
            if a.kind != "read":
                content_reads[i] = reads_of(a.data, set())
        static = {}
        for i, a in enumerate(acts):
            if a.kind != "read" and not content_reads[i]:
                static[i] = setup.static_content(a.id)

        def content(i, env):
            s = static.get(i)
            if s is not None:
                return s
            a = acts[i]
            if a.data is None:
                return T.Unk(a.id)
            return evaluate(a.data, env)

        def evaluate(e, env):
            def lookup(x):
                k = idx[x]
                if acts[k].kind == "read":
                    return env[slot[k]]
                return content(k, env)

            return T.substitute(e, lookup)

        # ---------------------------------------------------------------- facts as bits
        fact_bit: dict = {}
        facts: list = []

        def bit(key):
            b = fact_bit.get(key)
            if b is None:
                b = len(facts)
                fact_bit[key] = b
                facts.append(key)
            return 1 << b

        full = (1 << n) - 1
        nblocks = setup.blocks
        memo: dict = {}

        kinds = [a.kind for a in acts]
        blocks_of = [a.block for a in acts]
        observed = [a.observed for a in acts]
        ids = [a.id for a in acts]
        expects = [a.expect for a in acts]
        slot_of = [slot.get(i, -1) for i in range(n)]
        nslots = len(ref_reads)

        def sub(mask, blocks, env):
            key = (mask, blocks, env)
            if key in memo:
                return memo[key]
            if mask == full:
                r = 0
                for b in range(nblocks):
                    r |= bit(("b", b, blocks[b]))
                memo[key] = r
                return r
            acc = None
            for i in range(n):
                if (mask >> i) & 1 or (pred_mask[i] & ~mask):
                    continue
                k = kinds[i]
                blk = blocks_of[i]
                cur = blocks[blk]
                ob = observed[i]
                nb = blocks
                ne = env
                pair = 0
                if k == "read":
                    if ob is not None and ob != cur:
                        continue
                    pair = bit(("r", ids[i], cur))
                    s = slot_of[i]
                    if s >= 0:
                        lst = list(env)
                        lst[s] = cur
                        ne = tuple(lst)
                elif k == "write":
                    c = content(i, env)
                    if c != cur:
                        lst = list(blocks)
                        lst[blk] = c
                        nb = tuple(lst)
                else:  # rcw
                    exp = evaluate(expects[i], env)
                    ok = exp == cur
                    if ob is not None:
                        if isinstance(ob, str):
                            if (ob == "ok") != ok:
                                continue
                        elif ob != cur:
                            continue
                    pair = bit(("r", ids[i], cur))
                    if ok:
                        c = content(i, env)
                        if c != cur:
                            lst = list(blocks)
                            lst[blk] = c
                            nb = tuple(lst)
                nm = mask | (1 << i)
                # drop read values no longer needed by any unexecuted writer
                if nslots:
                    lst = None
                    for s in range(nslots):
                        if ne[s] is not None and not (dep_mask[s] & ~nm):
                            if lst is None:
                                lst = list(ne)
                            lst[s] = None
                    if lst is not None:
                        ne = tuple(lst)
                r = sub(nm, nb, ne)
                if r is None:
                    continue
                acc = (r | pair) if acc is None else (acc | r | pair)
            memo[key] = acc
            return acc

        old = sys.getrecursionlimit()
        need = 4 * n + 200
        if old < need:
            sys.setrecursionlimit(need)
        try:
            root = sub(0, tuple(setup.init), (None,) * nslots)
        finally:
            if old < need:
                sys.setrecursionlimit(old)

        if root is None:
            return Outcomes(mode, False)
        out = Outcomes(mode, True)
        for a in acts:
            if a.kind != "write":
                out.results[a.id] = set()
        for b in range(nblocks):
            out.final[b] = set()
        x = root
        while x:
            low = x & -x
            f = facts[low.bit_length() - 1]
            x ^= low
            if f[0] == "r":
                out.results[f[1]].add(f[2])
            else:
                out.final[f[1]].add(f[2])
        return out
