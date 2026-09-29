"""Exact possibility-set solver over effect orders (case sor).

Reduction (see SOURCES.md): a full schedule is determined, for the semantics, by the
order of its effect points.  A total order sigma of the actions is realisable by some
feasible-time full schedule (L, pi) iff sigma extends the precedence relation
``a -> b  iff  end(a) <_P start(b)`` (mode "all"), or ``pos_L(end a) < pos_L(start b)``
(mode "fixed").  We enumerate such orders by a layered DP over states
(done-set, block contents, still-needed read values), then keep only the transitions
that lie on a path to a complete schedule (observations are enforced on transitions).
"""

from __future__ import annotations

from harness import terms as T
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class EffectOrderDP(Solver):
    name = "opus55_1-sor-effdp"
    description = "Layered DP over linear extensions of the interval precedence order, with observation pruning"
    capabilities = SolverCapabilities(
        rcw=True,
        sync=True,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=False,
    )

    def solve(self, setup, linearization=None) -> Outcomes:
        mode = "all" if linearization is None else "fixed"
        acts = list(setup.actions.values())
        n = len(acts)
        idx = {a.id: i for i, a in enumerate(acts)}
        P = setup.poset
        start = [P.start_node[a.id] for a in acts]
        done = [P.done_node[a.id] for a in acts]

        # ---- precedence: pred[j] = mask of actions whose effect must precede j's
        pred = [0] * n
        if linearization is None:
            N = len(P)
            desc = [0] * N
            for x in reversed(P.topological_order()):
                m = 0
                for y in P.succs[x]:
                    m |= (1 << y) | desc[y]
                desc[x] = m
            for i in range(n):
                d = desc[done[i]]
                for j in range(n):
                    if i != j and (d >> start[j]) & 1:
                        pred[j] |= 1 << i
        else:
            pos = P.positions(linearization)
            for i in range(n):
                for j in range(n):
                    if i != j and pos[done[i]] < pos[start[j]]:
                        pred[j] |= 1 << i

        # ---- read dependencies of each writer's content / expected value
        is_read = [a.kind == "read" for a in acts]
        dmemo: dict[int, int] = {}

        def expr_deps(e) -> int:
            m = 0
            for r in T.refs(e):
                k = idx[r]
                if is_read[k]:
                    m |= 1 << k
                else:
                    m |= data_deps(k)
            return m

        def data_deps(i: int) -> int:
            if i in dmemo:
                return dmemo[i]
            dmemo[i] = 0
            a = acts[i]
            m = expr_deps(a.data) if a.data is not None else 0
            dmemo[i] = m
            return m

        full_deps = [0] * n
        static: list = [None] * n
        static_expect: list = [None] * n
        for i, a in enumerate(acts):
            if is_read[i]:
                continue
            dd = data_deps(i)
            full_deps[i] = dd
            if a.expect is not None:
                ed = expr_deps(a.expect)
                full_deps[i] |= ed
            else:
                ed = 0
            if dd == 0:
                static[i] = setup.static_content(a.id)
            if a.kind == "rcw" and ed == 0:
                static_expect[i] = T.substitute(a.expect, setup.static_content)

        def content(i: int, env):
            s = static[i]
            if s is not None:
                return s
            a = acts[i]
            if a.data is None:
                return T.Unk(a.id)
            return T.substitute(a.data, lambda x: lookup(x, env))

        def lookup(x: str, env):
            k = idx[x]
            if is_read[k]:
                return env[k]
            return content(k, env)

        need_cache: dict[int, int] = {}

        def needed(mask: int) -> int:
            v = need_cache.get(mask)
            if v is None:
                v = 0
                for i in range(n):
                    if not is_read[i] and not (mask >> i) & 1:
                        v |= full_deps[i]
                need_cache[mask] = v
            return v

        obs = [a.observed for a in acts]
        blocks = [a.block for a in acts]
        kinds = [a.kind for a in acts]

        # ---- forward layered exploration
        init_state = (0, tuple(setup.init), (None,) * n)
        layer_states: list[list] = [[init_state]]
        layer_edges: list[list] = []
        for k in range(n):
            nxt: dict = {}
            nxt_list: list = []
            edges_k: list = []
            for mask, cont, env in layer_states[k]:
                es = []
                for j in range(n):
                    bit = 1 << j
                    if mask & bit or (pred[j] & ~mask):
                        continue
                    b = blocks[j]
                    kind = kinds[j]
                    cur = cont[b]
                    ob = obs[j]
                    val = None
                    nc = cont
                    if kind == "read":
                        if ob is not None and cur != ob:
                            continue
                        val = cur
                    elif kind == "write":
                        c = content(j, env)
                        if c != cur:
                            lc = list(cont)
                            lc[b] = c
                            nc = tuple(lc)
                    else:  # rcw
                        e = static_expect[j]
                        if e is None:
                            e = T.substitute(acts[j].expect, lambda x: lookup(x, env))
                        succ = cur == e
                        if ob is not None:
                            if isinstance(ob, str):
                                if (ob == "ok") != succ:
                                    continue
                            elif cur != ob:
                                continue
                        val = cur
                        if succ:
                            c = content(j, env)
                            if c != cur:
                                lc = list(cont)
                                lc[b] = c
                                nc = tuple(lc)
                    nm = mask | bit
                    need = needed(nm)
                    le = list(env)
                    if kind == "read":
                        le[j] = val
                    for i in range(n):
                        if le[i] is not None and not (need >> i) & 1:
                            le[i] = None
                    key = (nm, nc, tuple(le))
                    t = nxt.get(key)
                    if t is None:
                        t = len(nxt_list)
                        nxt[key] = t
                        nxt_list.append(key)
                    es.append((j, val, t))
                edges_k.append(es)
            layer_edges.append(edges_k)
            layer_states.append(nxt_list)
            if not nxt_list:
                return Outcomes(mode, False)

        terminal = layer_states[n]
        if not terminal:
            return Outcomes(mode, False)

        # ---- backward: keep transitions on paths to a complete schedule
        results: dict[str, set] = {a.id: set() for a in acts if a.kind != "write"}
        good_next = [True] * len(terminal)
        for k in range(n - 1, -1, -1):
            g = []
            for es in layer_edges[k]:
                ok = False
                for j, val, t in es:
                    if good_next[t]:
                        ok = True
                        if val is not None:
                            results[acts[j].id].add(val)
                g.append(ok)
            good_next = g
        if not good_next[0]:
            return Outcomes(mode, False)

        final = {b: set() for b in range(setup.blocks)}
        for _, cont, _ in terminal:
            for b in range(setup.blocks):
                final[b].add(cont[b])
        return Outcomes(mode, True, results, final)
