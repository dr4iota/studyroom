"""Exact solver for cases b, o, br and or (no sync points), with witnesses.

Method
------
A full schedule ``(L, pi)`` induces an *effect order*: the actions sorted by ``pi``.
The total orders ``sigma`` on the actions that arise this way are exactly the linear
extensions of the partial order ``Q``:

    a <_Q b   iff   done(a) precedes start(b) in the trace poset P    (mode "all"),
    a <_Q b   iff   done(a) precedes start(b) in L                    (mode "fixed").

Necessity: if done(a) < start(b) then pi(a) <= pos(done(a)) < pos(start(b)) <= pi(b).
Sufficiency (mode "all"): for ``sigma`` extending ``Q``, the relation
``P + {start(a) -> done(b) : a <_sigma b}`` is acyclic (a cycle would alternate added
edges and P-paths ``done(b_i) -> start(a_{i+1})``, giving
``a_1 <_sigma b_1 <_Q a_2 <_sigma b_2 ... <_sigma a_1``); a topological order of it is a
linearization in which ``start(a) < done(b)`` whenever ``a <_sigma b``, and then
effect points can be chosen greedily along ``sigma``.  In mode "fixed" the same
greedy choice works directly in ``L``.

So ``Poss`` is a union, over the linear extensions of ``Q``, of the atomic block
semantics.  The solver runs a memoised breadth-first search over states

    (set of applied actions, block contents, values of still-needed reads),

dropping a block's content from the state once its last action is applied, and a
read's value once every write/RCW whose data depends on it is applied (those values
are emitted as edge labels instead).  Observations prune edges.  A state is *alive*
when the terminal state (everything applied) is reachable from it; ``Poss`` collects
the labels of edges into alive states, and the setup is consistent iff a terminal
state was reached.  Witnesses follow a parent pointer (root -> state) and a
completion pointer (state -> terminal), are re-simulated, and get a linearization
built from their effect order.
"""

from __future__ import annotations

from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register
from harness.semantics import Schedule
from harness.solve.api import Outcomes, Solver, SolverCapabilities
from harness.terms import Term, Unk, refs, substitute, to_value


@register
class IdealDPSolver(Solver):
    name = "fable51_1-or-idealdp"
    description = "Exact Poss sets by memoised search over ideals of the realizable effect order, with witnesses."
    capabilities = SolverCapabilities(
        rcw=True,
        sync=False,
        observed_reads=True,
        modes=frozenset({"all", "fixed"}),
        witnesses=True,
    )

    def solve(self, setup: Setup, linearization: Linearization | None = None) -> Outcomes:
        return _Run(setup, linearization).run()


class _Run:
    def __init__(self, setup: Setup, lin: Linearization | None) -> None:
        self.setup = setup
        self.lin = None if lin is None else tuple(lin)
        self.mode = "all" if lin is None else "fixed"
        self.acts = acts = list(setup.actions.values())
        self.n = n = len(acts)
        self.index = {a.id: i for i, a in enumerate(acts)}
        self.kind = [a.kind for a in acts]
        self.block = [a.block for a in acts]

        # Term interning: every block content / read value in the search is an int id.
        self.terms: list[Term] = []
        self.tid: dict[Term, int] = {}
        self.init_ids = [self._intern(t) for t in setup.init]

        # Observed results: term id, or "ok"/"fail" (RCW under rcw_result: flag), or None.
        self.obs: list = [None] * n
        for i, a in enumerate(acts):
            if a.observed is not None:
                self.obs[i] = a.observed if isinstance(a.observed, str) else self._intern(a.observed)

        self.predmask = self._q_preds()

        self.block_mask = [0] * setup.blocks
        for i, a in enumerate(acts):
            self.block_mask[a.block] |= 1 << i

        # Transitive read dependencies of every write/RCW (through references to writes).
        deps: list = [None] * n

        def dep(i: int) -> frozenset:
            d = deps[i]
            if d is None:
                s: set[int] = set()
                for e in (acts[i].data, acts[i].expect):
                    if e is None:
                        continue
                    for name in refs(e):
                        x = self.index[name]
                        if acts[x].kind == "read":
                            s.add(x)
                        else:
                            s |= dep(x)
                d = deps[i] = frozenset(s)
            return d

        # key_reads[i]: unobserved reads whose values the content/expect of i depends on
        # (observed reads are constants).  users[r]: mask of writes/RCWs needing read r.
        self.users = [0] * n
        self.key_reads: list[tuple[int, ...]] = [()] * n
        for i, a in enumerate(acts):
            if a.kind == "read":
                continue
            ks = tuple(sorted(r for r in dep(i) if self.obs[r] is None))
            self.key_reads[i] = ks
            for r in ks:
                self.users[r] |= 1 << i
        self.live_pos = [-1] * n
        cnt = 0
        for i in range(n):
            if self.kind[i] == "read" and self.users[i]:
                self.live_pos[i] = cnt
                cnt += 1
        self.n_live = cnt
        self.vcache: dict = {}

    # ------------------------------------------------------------------ helpers

    def _intern(self, t: Term) -> int:
        k = self.tid.get(t)
        if k is None:
            k = len(self.terms)
            self.tid[t] = k
            self.terms.append(t)
        return k

    def _q_preds(self) -> list[int]:
        """predmask[i]: actions that must take effect before i (the order Q)."""
        acts, n = self.acts, self.n
        poset = self.setup.poset
        pm = [0] * n
        if self.lin is not None:
            pos = poset.positions(self.lin)
            sp = [pos[poset.start_node[a.id]] for a in acts]
            dp = [pos[poset.done_node[a.id]] for a in acts]
            for i in range(n):
                m = 0
                si = sp[i]
                for j in range(n):
                    if dp[j] < si:
                        m |= 1 << j
                pm[i] = m
        elif self.setup.sync_points == 0:
            for i in range(n):
                ai = acts[i]
                m = 0
                for j in range(n):
                    aj = acts[j]
                    if aj.thread == ai.thread and aj.done < ai.start:
                        m |= 1 << j
                pm[i] = m
        else:
            anc = [0] * len(poset)
            for v in poset.topological_order():
                m = 0
                for u in poset.preds[v]:
                    m |= anc[u] | (1 << u)
                anc[v] = m
            for i in range(n):
                a_i = anc[poset.start_node[acts[i].id]]
                m = 0
                for j in range(n):
                    if (a_i >> poset.done_node[acts[j].id]) & 1:
                        m |= 1 << j
                pm[i] = m
        return pm

    def _values(self, i: int, live: tuple) -> tuple:
        """(content id, expect id or None) of write/RCW i given the live read values."""
        lp = self.live_pos
        key = (i, tuple([live[lp[r]] for r in self.key_reads[i]]))
        hit = self.vcache.get(key)
        if hit is not None:
            return hit
        acts, terms, index, obs = self.acts, self.terms, self.index, self.obs
        memo: dict[int, Term] = {}

        def term_of(x: int) -> Term:
            t = memo.get(x)
            if t is None:
                a = acts[x]
                if a.kind == "read":
                    o = obs[x]
                    t = terms[o if o is not None else live[lp[x]]]
                elif a.data is None:
                    t = Unk(a.id)
                else:
                    t = substitute(a.data, lambda s: term_of(index[s]))
                memo[x] = t
            return t

        a = acts[i]
        c = self._intern(term_of(i))
        e = None if a.expect is None else self._intern(substitute(a.expect, lambda s: term_of(index[s])))
        hit = (c, e)
        self.vcache[key] = hit
        return hit

    def _step(self, done: int, contents: tuple, live: tuple, i: int):
        """Apply action i; None if its observation is violated, else the new state and labels."""
        b = self.block[i]
        kind = self.kind[i]
        cur = contents[b]
        res = None
        new_contents = contents
        new_live = live
        new_done = done | (1 << i)
        if kind == "read":
            o = self.obs[i]
            if o is not None and o != cur:
                return None
            res = cur
            lp = self.live_pos[i]
            if lp >= 0:
                nl = list(live)
                nl[lp] = cur
                new_live = tuple(nl)
        else:
            c, e = self._values(i, live)
            if kind == "write":
                new_c = c
            else:
                res = cur
                ok = cur == e
                o = self.obs[i]
                if o is not None:
                    if isinstance(o, str):
                        if ok != (o == "ok"):
                            return None
                    elif o != cur:
                        return None
                new_c = c if ok else cur
            if new_c != cur:
                nc = list(contents)
                nc[b] = new_c
                new_contents = tuple(nc)
            kr = self.key_reads[i]
            if kr:
                users = self.users
                nl = None
                for r in kr:
                    if (users[r] & ~new_done) == 0:
                        if nl is None:
                            nl = list(new_live)
                        nl[self.live_pos[r]] = -1
                if nl is not None:
                    new_live = tuple(nl)
        fins: tuple = ()
        if (self.block_mask[b] & ~new_done) == 0:
            fins = ((b, new_contents[b]),)
            nc = list(new_contents)
            nc[b] = -1
            new_contents = tuple(nc)
        return new_done, new_contents, new_live, res, fins

    # ------------------------------------------------------------------ main search

    def run(self) -> Outcomes:
        n, nb = self.n, self.setup.blocks
        full = (1 << n) - 1
        root_contents = list(self.init_ids)
        pre_finals = []
        for b in range(nb):
            if self.block_mask[b] == 0:
                pre_finals.append((b, root_contents[b]))
                root_contents[b] = -1
        root = (0, tuple(root_contents), (-1,) * self.n_live)
        keys = [root]
        states = {root: 0}
        edges: list[list] = [[]]
        parent: list = [None]
        rev: list[list] = [[]]
        frontier: dict[int, list[int]] = {}
        predmask = self.predmask
        step = self._step
        q = 0
        while q < len(keys):
            done, contents, live = keys[q]
            fr = frontier.get(done)
            if fr is None:
                fr = [i for i in range(n) if not (done >> i) & 1 and (predmask[i] & ~done) == 0]
                frontier[done] = fr
            out = edges[q]
            for i in fr:
                st = step(done, contents, live, i)
                if st is None:
                    continue
                nd, nc, nl, res, fins = st
                k = (nd, nc, nl)
                t = states.get(k)
                if t is None:
                    t = len(keys)
                    states[k] = t
                    keys.append(k)
                    edges.append([])
                    parent.append((q, i))
                    rev.append([])
                out.append((i, res, fins, t))
                rev[t].append((q, i))
            q += 1

        terminal = states.get((full, (-1,) * nb, (-1,) * self.n_live))
        if terminal is None:
            return Outcomes(self.mode, False)

        alive = [False] * len(keys)
        nxt: list = [None] * len(keys)
        alive[terminal] = True
        stack = [terminal]
        while stack:
            t = stack.pop()
            for s, i in rev[t]:
                if not alive[s]:
                    alive[s] = True
                    nxt[s] = (i, t)
                    stack.append(s)
        self.parent, self.nxt, self.terminal = parent, nxt, terminal

        acts, terms = self.acts, self.terms
        results: dict[str, set] = {a.id: set() for a in acts if a.kind != "write"}
        final: dict[int, set] = {b: set() for b in range(nb)}
        wit: list[Schedule] = []
        for b, v in pre_finals:
            tv = terms[v]
            final[b].add(tv)
            wit.append(self._witness(None, None, 0, {"block": b, "value": to_value(tv)}))
        for s in range(len(keys)):
            if not alive[s]:
                continue
            for i, res, fins, t in edges[s]:
                if not alive[t]:
                    continue
                if res is not None:
                    tv = terms[res]
                    rs = results[acts[i].id]
                    if tv not in rs:
                        rs.add(tv)
                        wit.append(self._witness(s, i, t, {"id": acts[i].id, "value": to_value(tv)}))
                for b, v in fins:
                    tv = terms[v]
                    fs = final[b]
                    if tv not in fs:
                        fs.add(tv)
                        wit.append(self._witness(s, i, t, {"block": b, "value": to_value(tv)}))
        return Outcomes(self.mode, True, results, final, wit)

    # ------------------------------------------------------------------ witnesses

    def _witness(self, s, i, t: int, cert: dict) -> Schedule:
        """A feasible schedule through edge (s, i, t), or through state t when s is None."""
        path: list[int] = []
        if s is not None:
            x = s
            while self.parent[x] is not None:
                p, a = self.parent[x]
                path.append(a)
                x = p
            path.reverse()
            path.append(i)
        x = t
        while x != self.terminal:
            a, y = self.nxt[x]
            path.append(a)
            x = y
        return self._schedule(path, cert)

    def _schedule(self, path: list[int], cert: dict) -> Schedule:
        acts, index = self.acts, self.index
        contents = [self.terms[k] for k in self.init_ids]
        env: dict[int, Term] = {}
        results: dict[str, Term] = {}

        def term_of(x: int) -> Term:
            t = env.get(x)
            if t is None:
                a = acts[x]
                t = Unk(a.id) if a.data is None else substitute(a.data, lambda s: term_of(index[s]))
                env[x] = t
            return t

        for i in path:
            a = acts[i]
            b = a.block
            if a.kind == "read":
                results[a.id] = env[i] = contents[b]
            elif a.kind == "write":
                contents[b] = term_of(i)
            else:
                old = contents[b]
                results[a.id] = old
                exp = substitute(a.expect, lambda s: term_of(index[s]))
                if old == exp:
                    contents[b] = term_of(i)
        order = self.lin if self.lin is not None else self._linearize(path)
        return Schedule(tuple(order), [acts[i].id for i in path], results, contents, True, {"certifies": cert})

    def _linearize(self, path: list[int]) -> list[int]:
        """A linearization of P in which the effect order ``path`` is realizable.

        Emit, for each action in effect order, its start node with all its P-predecessors;
        then everything left.  Then done(b) comes after start(a) whenever a precedes b.
        """
        poset = self.setup.poset
        preds = poset.preds
        emitted = [False] * len(poset)
        out: list[int] = []

        def emit(node: int) -> None:
            stack = [node]
            while stack:
                x = stack[-1]
                if emitted[x]:
                    stack.pop()
                    continue
                pend = [p for p in preds[x] if not emitted[p]]
                if pend:
                    stack.extend(pend)
                else:
                    emitted[x] = True
                    out.append(x)
                    stack.pop()

        for i in path:
            emit(poset.start_node[self.acts[i].id])
        for x in range(len(poset)):
            emit(x)
        return out
