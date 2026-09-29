"""Exact possibility-set solver for case b (no sync points, no observed reads).

Idea
----
Without sync points the trace poset is a disjoint union of thread chains. The effect
orders reachable by some full schedule ``(L, pi)`` are exactly the linear extensions of
the relation ``a -> b`` iff ``a`` and ``b`` are in the same thread and ``done(a)`` comes
before ``start(b)`` in program order (mode "all"), or ``pos_L(done(a)) < pos_L(start(b))``
(mode "fixed", the interval order of ``L``).

We explore all linear extensions by forward reachability over states

    (executed-action set, block contents, values of executed reads still needed by an
     unexecuted write)

which fully determine the future, recording every value a read returns and every final
content. Terms are interned to integers so states hash cheaply. A block's content is
forgotten (set to -1) when no read of it remains but a write of it does, since it can
no longer be observed.
"""

from __future__ import annotations

from harness import terms as T
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class ReachSolver(Solver):
    name = "opus55_1-b-reach"
    description = "Exact Poss via state reachability over linear extensions of the effect-order constraints"
    capabilities = SolverCapabilities(
        rcw=False,
        sync=False,
        observed_reads=False,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup, linearization=None) -> Outcomes:
        acts = list(setup.actions.values())
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        mode = "all" if linearization is None else "fixed"
        nb = setup.blocks

        # ---- ordering constraints on effect points
        preds = [0] * n
        if linearization is None:
            for i, a in enumerate(acts):
                for j, b in enumerate(acts):
                    if i != j and a.thread == b.thread and a.done < b.start:
                        preds[j] |= 1 << i
        else:
            P = setup.poset
            pos = P.positions(linearization)
            for i, a in enumerate(acts):
                de = pos[P.done_node[a.id]]
                for j, b in enumerate(acts):
                    if i != j and de < pos[P.start_node[b.id]]:
                        preds[j] |= 1 << i

        # ---- term interning
        tlist: list = []
        tids: dict = {}

        def intern(t) -> int:
            k = tids.get(t)
            if k is None:
                k = len(tlist)
                tids[t] = k
                tlist.append(t)
            return k

        # ---- reads and dependencies
        is_read = [a.kind == "read" for a in acts]
        slot = [-1] * n
        read_ids: list[int] = []
        for i in range(n):
            if is_read[i]:
                slot[i] = len(read_ids)
                read_ids.append(i)
        nr = len(read_ids)

        dep_memo: dict[str, frozenset] = {}

        def deps_of(aid: str) -> frozenset:
            """Read ids (strings) that write ``aid``'s content depends on, transitively."""
            if aid in dep_memo:
                return dep_memo[aid]
            a = acts[idx[aid]]
            out: set[str] = set()
            if a.data is not None:
                for r in T.refs(a.data):
                    if acts[idx[r]].kind == "read":
                        out.add(r)
                    else:
                        out |= deps_of(r)
            fs = frozenset(out)
            dep_memo[aid] = fs
            return fs

        dep_slots: list[tuple[int, ...]] = [()] * n
        need_mask = [0] * nr  # writes needing each read
        static_content: list[int] = [-1] * n
        for i, a in enumerate(acts):
            if is_read[i]:
                continue
            ds = tuple(sorted(slot[idx[r]] for r in deps_of(a.id)))
            dep_slots[i] = ds
            for k in ds:
                need_mask[k] |= 1 << i
            if not ds:
                static_content[i] = intern(setup.static_content(a.id))

        eval_cache: dict = {}

        def write_content(i: int, lv: tuple) -> int:
            if static_content[i] >= 0:
                return static_content[i]
            key = (i, tuple(lv[k] for k in dep_slots[i]))
            r = eval_cache.get(key)
            if r is not None:
                return r

            def look(x: str):
                j = idx[x]
                if is_read[j]:
                    v = lv[slot[j]]
                    return tlist[v]
                return content_term(j)

            def content_term(j: int):
                d = acts[j].data
                if d is None:
                    return T.Unk(acts[j].id)
                return T.substitute(d, look)

            r = intern(content_term(i))
            eval_cache[key] = r
            return r

        # ---- block masks
        brm = [0] * nb
        bwm = [0] * nb
        for i, a in enumerate(acts):
            if is_read[i]:
                brm[a.block] |= 1 << i
            else:
                bwm[a.block] |= 1 << i
        full = (1 << n) - 1

        def forget(b: int, rem: int) -> bool:
            return not (rem & brm[b]) and bool(rem & bwm[b])

        init_c = [intern(t) for t in setup.init]
        for b in range(nb):
            if forget(b, full):
                init_c[b] = -1
        init_state = (tuple(init_c), tuple([-1] * nr))

        poss = [set() for _ in range(nr)]
        layer: dict[int, set] = {0: {init_state}}
        for _ in range(n):
            nxt: dict[int, set] = {}
            for E, sts in layer.items():
                for i in range(n):
                    if (E >> i) & 1 or (preds[i] & ~E):
                        continue
                    E2 = E | (1 << i)
                    rem2 = full & ~E2
                    a = acts[i]
                    b = a.block
                    fb = forget(b, rem2)
                    tgt = nxt.get(E2)
                    if tgt is None:
                        tgt = set()
                        nxt[E2] = tgt
                    if is_read[i]:
                        k = slot[i]
                        pk = poss[k]
                        keep = bool(need_mask[k] & rem2)
                        for c, lv in sts:
                            v = c[b]
                            pk.add(v)
                            if keep:
                                lv2 = list(lv)
                                lv2[k] = v
                                lv2 = tuple(lv2)
                            else:
                                lv2 = lv
                            if fb:
                                c2 = list(c)
                                c2[b] = -1
                                c2 = tuple(c2)
                            else:
                                c2 = c
                            tgt.add((c2, lv2))
                    else:
                        drop = [k for k in dep_slots[i] if not (need_mask[k] & rem2)]
                        for c, lv in sts:
                            w = -1 if fb else write_content(i, lv)
                            c2 = list(c)
                            c2[b] = w
                            c2 = tuple(c2)
                            if drop:
                                lv2 = list(lv)
                                for k in drop:
                                    lv2[k] = -1
                                lv2 = tuple(lv2)
                            else:
                                lv2 = lv
                            tgt.add((c2, lv2))
            layer = nxt

        finals = layer.get(full, set())
        out = Outcomes(mode, True)
        for k, i in enumerate(read_ids):
            out.results[acts[i].id] = {tlist[v] for v in poss[k]}
        for b in range(nb):
            out.final[b] = {tlist[c[b]] for c, _ in finals}
        return out
