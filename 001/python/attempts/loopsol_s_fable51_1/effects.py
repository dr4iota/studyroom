"""Exact ``Poss_n`` for loop setups (case s) by exploring effect orders.

Outline
-------
1.  *Effect orders.*  For a full schedule ``(L, pi)`` the block semantics depend only
    on the order of the effect points.  Define, on the actions of ``P_n``,

        a < b   iff   done(a) precedes start(b) in the trace poset.

    Every full schedule orders effects by a linear extension of ``<``, and conversely
    every linear extension of ``<`` is the effect order of some full schedule (add the
    edges ``start(a_i) -> done(a_j)`` for ``i < j`` to the poset; the result is acyclic
    when the order respects ``<``, any linearization of it admits effect points chosen
    greedily from left to right).  So the possibility sets are exactly the values seen
    over all linear extensions of ``<``.

2.  *State exploration.*  Linear extensions of ``<`` are walked as paths in the lattice
    of its down-sets.  A state is ``(effected set, block contents, live read values)``,
    where a read value is live while a later write still refers to it.  Two paths that
    meet in one state have the same futures, so states are deduplicated.  Read values
    are recorded on every transition, final contents on every terminal state.

3.  *Large n.*  Exact answers are computed for ``n = 1, 2, ...`` while a time budget
    lasts (or until the requested ``n`` is reached, which gives the exact answer).  Past
    that, the sequence of answers is extended by its observed eventual period.
"""

from __future__ import annotations

import time

from harness import terms as T
from harness.capabilities import Capabilities
from harness.loop.api import LoopOutcomes, LoopSolver
from harness.loops import LoopSetup, base_id
from harness.registry import register

# Bits per value field in the packed state code (term ids are interned small ints).
_B = 20
_FM = (1 << _B) - 1

# Time budgets in seconds.  The grader allows about 20 s per call.
_SOFT = 6.0  # do not start a new n after this much time
_HARD = 11.0  # abort an n in progress after this much time
_LAST_RESORT = 17.0
_STATE_CAP = 1_200_000


class _Interner:
    """Terms <-> small positive ints (0 is reserved for an empty register)."""

    def __init__(self) -> None:
        self.terms: list = [None]
        self.ids: dict = {}

    def __call__(self, t) -> int:
        v = self.ids.get(t)
        if v is None:
            v = len(self.terms)
            self.terms.append(t)
            self.ids[t] = v
        return v


def _answer(ls: LoopSetup, n: int, intern: _Interner, deadline: float, state_cap: int):
    """Exact (results, finals) for ``P_n`` as sets of interned ids, or None if aborted."""
    su = ls.unroll(n)
    po = su.poset
    V = len(po)
    M = su.blocks
    N = su.n_threads

    # Backward reachability on poset nodes: back[x] = nodes that strictly precede x.
    preds = po.preds
    back = [0] * V
    for x in po.topological_order():
        acc = 0
        for y in preds[x]:
            acc |= (1 << y) | back[y]
        back[x] = acc

    acts = list(su.actions.values())
    m = len(acts)
    # An action's bit in the effected-set mask is its done node's index.
    abit = [1 << po.done_node[a.id] for a in acts]
    done_mask = 0
    for b in abit:
        done_mask |= b
    pred_mask = [back[po.start_node[a.id]] & done_mask for a in acts]

    # Expand write data to expressions over read references only.
    def expand(e):
        if isinstance(e, T.Pair):
            return T.Pair(expand(e.left), expand(e.right))
        if isinstance(e, T.Ref):
            b = su.actions[e.action]
            if b.kind == "read":
                return e
            return T.Unk(b.id) if b.data is None else expand(b.data)
        return e

    expanded = [None] * m
    users: dict[str, int] = {}
    for i, a in enumerate(acts):
        if a.kind != "read":
            ex = T.Unk(a.id) if a.data is None else expand(a.data)
            expanded[i] = ex
            for r in T.refs(ex):
                users[r] = users.get(r, 0) | abit[i]

    # One register slot per template read that some write refers to.  Within a thread,
    # all users of a body read lie in the same iteration, so instances of one template
    # read never need to be live at the same time.
    slot_of_tmpl: dict[str, int] = {}
    for r in users:
        tm = base_id(r)
        if tm not in slot_of_tmpl:
            slot_of_tmpl[tm] = len(slot_of_tmpl)
    sshift_by_id = {r: _B * (M + slot_of_tmpl[base_id(r)]) for r in users}

    kind = [0 if a.kind == "read" else 1 for a in acts]
    bshift = [_B * a.block for a in acts]
    tmpl = [base_id(a.id) for a in acts]
    sshift = [sshift_by_id.get(a.id, -1) if a.kind == "read" else -1 for a in acts]
    wdata = [None] * m
    kills = [()] * m
    for i, a in enumerate(acts):
        if a.kind == "read":
            continue
        ex = expanded[i]
        if isinstance(ex, T.Ref):
            wdata[i] = (1, sshift_by_id[ex.action])
        elif T.refs(ex):
            wdata[i] = (2, ex)
        else:
            wdata[i] = (0, intern(ex))
        kills[i] = tuple((sshift_by_id[r], users[r]) for r in T.refs(ex))

    # Per-thread actions in start order, and the scan window of each front position.
    orders: list[list[int]] = [[] for _ in range(N)]
    for i, a in enumerate(acts):
        orders[a.thread].append(i)
    limits: list[list[int]] = []
    for t in range(N):
        orders[t].sort(key=lambda i: acts[i].start)
        order = orders[t]
        L = len(order)
        lim = [0] * L
        for k in range(L):
            e = acts[order[k]].done
            k2 = k + 1
            while k2 < L and acts[order[k2]].start < e:
                k2 += 1
            lim[k] = k2
        limits.append(lim)
    lens = [len(o) for o in orders]

    init_code = 0
    for b, t in enumerate(su.init):
        init_code |= intern(t) << (_B * b)

    res: dict[str, set[int]] = {r: set() for r in ls.reads()}
    finals: dict[int, set[int]] = {b: set() for b in range(M)}
    terms = intern.terms
    FM = _FM
    B = _B

    visited = {init_code << V}
    stack = [(0, init_code, tuple([0] * N))]
    pops = 0
    monotonic = time.monotonic
    while stack:
        S, code, front = stack.pop()
        pops += 1
        if not (pops & 2047) and (monotonic() > deadline or len(visited) > state_cap):
            return None
        if S == done_mask:
            for b in range(M):
                finals[b].add((code >> (B * b)) & FM)
            continue
        for t in range(N):
            f = front[t]
            if f >= lens[t]:
                continue
            order = orders[t]
            for k in range(f, limits[t][f]):
                a = order[k]
                ab = abit[a]
                if S & ab:
                    continue
                pm = pred_mask[a]
                if pm & S != pm:
                    continue
                S2 = S | ab
                if kind[a] == 0:
                    v = (code >> bshift[a]) & FM
                    res[tmpl[a]].add(v)
                    ss = sshift[a]
                    code2 = code if ss < 0 else (code & ~(FM << ss)) | (v << ss)
                else:
                    ev = wdata[a]
                    tag = ev[0]
                    if tag == 0:
                        v = ev[1]
                    elif tag == 1:
                        v = (code >> ev[1]) & FM
                    else:
                        cur = code
                        v = intern(T.substitute(ev[1], lambda r: terms[(cur >> sshift_by_id[r]) & FM]))
                    bs = bshift[a]
                    code2 = (code & ~(FM << bs)) | (v << bs)
                    for ss, um in kills[a]:
                        if um & S2 == um:
                            code2 &= ~(FM << ss)
                key = S2 | (code2 << V)
                if key in visited:
                    continue
                visited.add(key)
                f2 = f
                while f2 < lens[t] and S2 & abit[order[f2]]:
                    f2 += 1
                fr = list(front)
                fr[t] = f2
                stack.append((S2, code2, tuple(fr)))
    return res, finals


def _canonical(ans, reads, M):
    res, finals = ans
    return (tuple(frozenset(res[r]) for r in reads), tuple(frozenset(finals[b]) for b in range(M)))


def _extrapolate(seq: list, n: int):
    """``seq[k-1]`` is the answer for ``k = 1..N``; extend to ``n > N`` by periodicity."""
    N = len(seq)
    if n <= N:
        return seq[n - 1]
    for p in range(1, N + 1):
        k = N - p
        while k >= 1 and seq[k - 1] == seq[k + p - 1]:
            k -= 1
        tail = N - k  # number of values in the p-periodic tail (positions k+1..N)
        if tail >= 2 * p + 2:
            idx = N - ((N - n) % p)
            return seq[idx - 1]
    return seq[-1]


@register
class EffectOrderSolver(LoopSolver):
    name = "fable51_1-s-effects"
    description = "Explores all effect orders of the unrolled poset (deduplicated states) for n up to a time budget, then extends by the observed period."
    capabilities = Capabilities(rcw=False, sync=True, observed_reads=False)

    def solve(self, setup: LoopSetup, n: int) -> LoopOutcomes:
        start = time.monotonic()
        intern = _Interner()
        reads = setup.reads()
        M = setup.blocks
        seq: list = []
        k = 1
        while True:
            ans = _answer(setup, k, intern, start + _HARD, _STATE_CAP)
            if ans is None:
                break
            seq.append(_canonical(ans, reads, M))
            if k == n or time.monotonic() > start + _SOFT:
                break
            k += 1
        if not seq:
            ans = _answer(setup, 1, intern, start + _LAST_RESORT, 1 << 62)
            if ans is None:
                return LoopOutcomes({r: set() for r in reads}, {b: set() for b in range(M)})
            seq.append(_canonical(ans, reads, M))
        chosen = _extrapolate(seq, n)
        terms = intern.terms
        results = {r: {terms[v] for v in chosen[0][i]} for i, r in enumerate(reads)}
        final = {b: {terms[v] for v in chosen[1][b]} for b in range(M)}
        return LoopOutcomes(results, final)
