"""Feasible-linearization enumerator and counter for case ``sor``.

Idea (see SOURCES.md):

* A linearization ``L`` is feasible iff some order of effect points, compatible with the
  intervals ``I_L(a)``, makes every observed read/RCW return its observed term.
* We build ``L`` node by node and carry, for the current prefix, the set of reachable
  *configurations* ``(effected-mask, memory, read-env)`` of the atomic execution.
  Effects are normalised to happen only immediately before ``done`` nodes: before
  ``done(a)`` either ``a`` has already taken effect and nothing happens, or a sequence
  of pending (started, not yet effected) actions ending with ``a`` takes effect.
* A search state is ``(placed-node mask, frozenset of configurations)``; the future
  depends only on it, so liveness ("has a feasible completion") is memoised. The
  enumerator only descends into live states, so it never explores a dead branch twice.
* Only *relevant* actions are simulated: observed reads/RCWs, reads whose values feed
  data/expected values of relevant writers, and writers on blocks whose content can be
  observed (directly or through such reads). With no observations every linearization
  is feasible and a plain linear-extension enumerator is used.
"""

from __future__ import annotations

from typing import Iterator

from harness import terms as T
from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

CAPS = Capabilities(rcw=True, sync=True, observed_reads=True)

_READ, _WRITE, _RCW = 0, 1, 2


class _Problem:
    def __init__(self, setup: Setup) -> None:
        P = setup.poset
        self.n = n = len(P)
        self.full = (1 << n) - 1
        self.preds = [list(p) for p in P.preds]
        self.succs = [list(s) for s in P.succs]
        pm = [0] * n
        for v in range(n):
            m = 0
            for u in P.preds[v]:
                m |= 1 << u
            pm[v] = m
        self.predmask = pm

        actions = setup.actions
        self.actions = actions
        acts = list(actions.values())

        # ---- relevant blocks / needed reads (fixed point)
        rel_blocks = {a.block for a in acts if a.observed is not None}
        needed: set[str] = set()
        while True:
            todo = [e for a in acts if a.writes and a.block in rel_blocks for e in (a.data, a.expect) if e is not None]
            seen_w: set[str] = set()
            while todo:
                e = todo.pop()
                for r in T.refs(e):
                    b = actions[r]
                    if b.kind == "read":
                        needed.add(r)
                    elif r not in seen_w:
                        seen_w.add(r)
                        if b.data is not None:
                            todo.append(b.data)
            nb = rel_blocks | {actions[r].block for r in needed}
            if nb == rel_blocks:
                break
            rel_blocks = nb

        self.needed = [a.id for a in acts if a.id in needed]
        self.env_idx = {r: i for i, r in enumerate(self.needed)}

        rel = [a for a in acts if (a.writes and a.block in rel_blocks) or a.observed is not None or a.id in needed]
        self.R = len(rel)
        self.rel_info = []
        for a in rel:
            kind = _READ if a.kind == "read" else _WRITE if a.kind == "write" else _RCW
            eidx = self.env_idx.get(a.id, -1)
            stat_c = None
            stat_e = None
            if a.writes and not setup.depends_on_reads(a.id):
                stat_c = setup.static_content(a.id)
                if a.expect is not None:
                    stat_e = T.substitute(a.expect, setup.static_content)
            self.rel_info.append((kind, a.block, a.observed, eidx, a.id, stat_c, stat_e, a.data, a.expect))
        self.done_rel = [-1] * n
        self.rel_start = []
        for i, a in enumerate(rel):
            self.done_rel[P.done_node[a.id]] = i
            self.rel_start.append((P.start_node[a.id], 1 << i))

        self.init_cfg = (0, tuple(setup.init), tuple(None for _ in self.needed))
        self.memo: dict = {}

    # ------------------------------------------------------------------ semantics

    def _eval(self, e: T.Expr, env: tuple) -> T.Term:
        acts = self.actions
        eidx = self.env_idx

        def lk(x: str) -> T.Term:
            a = acts[x]
            if a.kind == "read":
                return env[eidx[x]]
            if a.data is None:
                return T.Unk(x)
            return T.substitute(a.data, lk)

        return T.substitute(e, lk)

    def _content(self, info: tuple, env: tuple) -> T.Term:
        if info[5] is not None:
            return info[5]
        if info[7] is None:
            return T.Unk(info[4])
        return self._eval(info[7], env)

    def _apply(self, cfg: tuple, i: int):
        mask, mem, env = cfg
        info = self.rel_info[i]
        kind, blk, obs, eidx = info[0], info[1], info[2], info[3]
        nmask = mask | (1 << i)
        if kind == _READ:
            v = mem[blk]
            if obs is not None and v != obs:
                return None
            if eidx >= 0:
                env = env[:eidx] + (v,) + env[eidx + 1:]
            return (nmask, mem, env)
        if kind == _WRITE:
            c = self._content(info, env)
            return (nmask, mem[:blk] + (c,) + mem[blk + 1:], env)
        # RCW
        old = mem[blk]
        exp = info[6] if info[6] is not None else self._eval(info[8], env)
        ok = old == exp
        if obs is not None:
            if isinstance(obs, str):
                if (obs == "ok") != ok:
                    return None
            elif old != obs:
                return None
        if ok:
            c = self._content(info, env)
            mem = mem[:blk] + (c,) + mem[blk + 1:]
        return (nmask, mem, env)

    def _done(self, C: frozenset, a: int, started: int) -> frozenset:
        abit = 1 << a
        result = set()
        frontier = []
        for c in C:
            if c[0] & abit:
                result.add(c)
            else:
                frontier.append(c)
        seen = set(frontier)
        queue = frontier
        R = self.R
        while queue:
            c = queue.pop()
            r = self._apply(c, a)
            if r is not None:
                result.add(r)
            pend = started & ~c[0] & ~abit
            p = 0
            while pend:
                if pend & 1:
                    nc = self._apply(c, p)
                    if nc is not None and nc not in seen:
                        seen.add(nc)
                        queue.append(nc)
                pend >>= 1
                p += 1
                if p >= R:
                    break
        return frozenset(result)

    # ------------------------------------------------------------------ search

    def _avail(self, mask: int) -> list[int]:
        pm = self.predmask
        return [x for x in range(self.n) if not (mask >> x) & 1 and not (pm[x] & ~mask)]

    def children(self, state: tuple) -> list:
        mask, C = state
        out = []
        for x in self._avail(mask):
            nm = mask | (1 << x)
            a = self.done_rel[x]
            if a < 0:
                out.append((x, (nm, C)))
                continue
            started = 0
            for node, bit in self.rel_start:
                if (nm >> node) & 1:
                    started |= bit
            cs = self._done(C, a, started)
            if cs:
                out.append((x, (nm, cs)))
        return out

    def root(self) -> tuple:
        return (0, frozenset([self.init_cfg]))

    def alive(self, state: tuple) -> bool:
        memo = self.memo
        v = memo.get(state)
        if v is not None:
            return v
        full = self.full
        if state[0] == full:
            memo[state] = True
            return True
        stack = [(state, iter(self.children(state)))]
        while stack:
            s, it = stack[-1]
            pushed = False
            for _x, cs in it:
                if cs[0] == full:
                    for s2, _ in stack:
                        memo[s2] = True
                    return True
                v = memo.get(cs)
                if v is True:
                    for s2, _ in stack:
                        memo[s2] = True
                    return True
                if v is False:
                    continue
                stack.append((cs, iter(self.children(cs))))
                pushed = True
                break
            if not pushed:
                memo[s] = False
                stack.pop()
        return False

    def enum_feasible(self) -> Iterator[Linearization]:
        if self.n == 0:
            yield ()
            return
        root = self.root()
        if not self.alive(root):
            return
        full = self.full
        order: list[int] = []
        stack = [iter(self.children(root))]
        while stack:
            it = stack[-1]
            pushed = False
            for x, cs in it:
                if cs[0] == full:
                    order.append(x)
                    yield tuple(order)
                    order.pop()
                    continue
                if self.alive(cs):
                    order.append(x)
                    stack.append(iter(self.children(cs)))
                    pushed = True
                    break
            if not pushed:
                stack.pop()
                if order:
                    order.pop()

    def enum_plain(self) -> Iterator[Linearization]:
        n = self.n
        if n == 0:
            yield ()
            return
        succs = self.succs
        indeg = [len(p) for p in self.preds]
        order: list[int] = []
        stack = [[[x for x in range(n) if indeg[x] == 0], 0]]
        while stack:
            frame = stack[-1]
            choices, i = frame
            if i:
                y = order.pop()
                for z in succs[y]:
                    indeg[z] += 1
            if i == len(choices):
                stack.pop()
                continue
            x = choices[i]
            frame[1] = i + 1
            order.append(x)
            nxt = [c for c in choices if c != x]
            for z in succs[x]:
                indeg[z] -= 1
                if indeg[z] == 0:
                    nxt.append(z)
            if len(order) == n:
                yield tuple(order)
            else:
                stack.append([nxt, 0])

    def count_lin(self) -> int:
        layer = {0: 1}
        for _ in range(self.n):
            new: dict[int, int] = {}
            for mask, w in layer.items():
                for x in self._avail(mask):
                    nm = mask | (1 << x)
                    new[nm] = new.get(nm, 0) + w
            layer = new
        return layer.get(self.full, 0)

    def count_feasible(self) -> int:
        layer = {self.root(): 1}
        for _ in range(self.n):
            new: dict = {}
            for st, w in layer.items():
                for _x, cs in self.children(st):
                    new[cs] = new.get(cs, 0) + w
            layer = new
        return sum(layer.values())


@register
class SorEnumerator(LinEnumerator):
    name = "opus55_1-sor-enum"
    description = "DFS over linearization prefixes tracking reachable atomic-execution states, memoised liveness pruning"
    capabilities = CAPS
    gray_code = False

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        prob = _Problem(setup)
        if prob.R == 0:
            return prob.enum_plain()
        return prob.enum_feasible()


@register
class SorCounter(LinCounter):
    name = "opus55_1-sor-count"
    description = "Layered DP over down-sets (Lin) and over (down-set, execution-state set) pairs (LinFeas)"
    capabilities = CAPS

    def count(self, setup: Setup) -> CountResult:
        prob = _Problem(setup)
        lin = prob.count_lin()
        feas = None
        if setup.features().observed_reads:
            feas = lin if prob.R == 0 else prob.count_feasible()
        return CountResult(linearizations=lin, feasible=feas, method="downset-dp")
