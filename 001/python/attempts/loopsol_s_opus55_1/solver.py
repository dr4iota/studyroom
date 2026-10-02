"""Exact possibility sets for loop setups (task loopsol, case s).

Method (see SOURCES.md):

* Operational model.  A full schedule (L, pi) is the same thing as an interleaving of
  the threads' steps, the virtual sync steps and one "effect" step per action placed
  between its start and its end.  Non-effect steps (starts, dones, before/after/at
  events) only ever enable other steps, so they are taken eagerly; the only real
  choices are the effects and, at the end of a body iteration, whether the thread
  loops again or leaves the body.
* All iteration counts at once.  The search runs every thread with its own iteration
  counter, up to a cap ``L``; a thread may leave its body after any iteration, and only
  runs in which every thread leaves after the same count ``c`` are complete (they are
  exactly the runs of ``P_c``).  A backward pass gives, for every state, the set of
  counts with which it can complete (a bit mask), and so ``Poss_c`` for every
  ``c <= L`` from one search.
* Reduction.  An effect that conflicts with nothing any other thread can still do (and
  with no overlapping action of its own thread) is taken alone (a persistent set of
  size one); this keeps one representative of every equivalence class of runs.
* Large ``n``.  If ``n`` exceeds the largest cap affordable in the time budget, the
  answer sequence ``Poss_1 .. Poss_L`` is extended by its detected eventual period.
"""

from __future__ import annotations

import math
import time
from array import array

from harness import terms as T
from harness.capabilities import Capabilities
from harness.loop.api import LoopOutcomes, LoopSolver
from harness.loops import LoopSetup
from harness.registry import register

OP_START, OP_DONE, OP_BEFORE, OP_AFTER, OP_AT = 0, 1, 2, 3, 4
INF = 1 << 30

BUDGET = 8.0  # seconds spent growing the cap within one call
CAPMAX = 400  # never search beyond this cap
_CACHE: dict = {}
_CACHE_MAX = 48


def _passed_iter(l, i, k):
    """Has the thread in local state ``l`` executed body step ``k`` of iteration ``i``?"""
    s = l[0]
    if s == 0:
        return False
    if s == 1:
        return l[1] > i or (l[1] == i and l[2] > k)
    return True  # in the suffix or finished: all its iterations are done


class _Compiled:
    """The loop setup compiled for the search, plus term and observation tables."""

    def __init__(self, setup: LoopSetup) -> None:
        self.NT = len(setup.threads)
        self.M = setup.blocks
        K, Kb = setup.sync_points, setup.loop_sync_points
        self.terms: list = []
        self.tid: dict = {}
        self.init = tuple(self.intern(t) for t in setup.init)
        self.read_ids = list(setup.reads())
        self.obs_ids: dict = {}
        self.obs_list: list = []

        plain_at = [[] for _ in range(K)]
        plain_before = [[] for _ in range(K)]
        iter_at = [[] for _ in range(Kb)]
        iter_before = [[] for _ in range(Kb)]
        has_sync_steps = False

        self.steps, self.body_empty, self.body_len = [], [], []
        self.binfo, self.cc, self.dead, self.fut, self.futlast, self.nslots = [], [], [], [], [], []

        for t, th in enumerate(setup.threads):
            segs = (th.prefix, th.body, th.suffix)
            bit_of, start_pos, done_pos, kind_of, block_of, data_of = {}, {}, {}, {}, {}, {}
            for si, seg in enumerate(segs):
                for i, st in enumerate(seg):
                    if st.is_start:
                        bit_of[st.id] = 1 << len(bit_of)
                        start_pos[st.id] = (si, i)
                        kind_of[st.id] = st.kind
                        block_of[st.id] = st.target
                        data_of[st.id] = st.data
                    elif st.kind == "done":
                        done_pos[st.target] = (si, i)

            # value slots: actions whose value some write expression refers to
            refd = set()
            for aid, k in kind_of.items():
                if k == "write" and data_of[aid] is not None:
                    refd |= T.refs(data_of[aid])
            ordered = sorted(refd)
            slot_of = {aid: i for i, aid in enumerate(ordered)}
            ns = len(ordered)
            self.nslots.append(ns)

            # a slot may be dropped once its own done and the dones of its users are passed
            kill = {aid: done_pos[aid] for aid in ordered}
            for aid, k in kind_of.items():
                if k == "write" and data_of[aid] is not None:
                    ws = start_pos[aid][0]
                    use = done_pos[aid]
                    for r in T.refs(data_of[aid]):
                        u = use
                        if ws == 1 and start_pos[r][0] == 0:
                            u = (1, INF)  # prefix value used by every iteration
                        if u > kill[r]:
                            kill[r] = u
            dead_t = []
            for si, seg in enumerate(segs):
                dead_t.append([tuple(slot_of[a] for a in ordered if (si, i) > kill[a])
                               for i in range(len(seg) + 1)])
            dead_t.append([tuple(range(ns))])
            self.dead.append(dead_t)

            def spec_of(aid, data_of=data_of, slot_of=slot_of):
                d = data_of[aid]
                if d is None:
                    return (0, self.intern(T.Unk(aid)))
                if not T.refs(d):
                    return (0, self.intern(d))
                if isinstance(d, T.Ref):
                    return (1, slot_of[d.action])
                return (2, d, slot_of)

            binfo_t = {}
            for aid in kind_of:
                isw = kind_of[aid] == "write"
                binfo_t[bit_of[aid]] = (aid, isw, block_of[aid], slot_of.get(aid, -1),
                                        spec_of(aid) if isw else None)
            self.binfo.append(binfo_t)

            comp = []
            for si, seg in enumerate(segs):
                row = []
                for i, st in enumerate(seg):
                    if st.is_start:
                        b = bit_of[st.id]
                        if st.kind == "write":
                            row.append((OP_START, b, slot_of.get(st.id, -1), binfo_t[b][4]))
                        else:
                            row.append((OP_START, b, -1, None))
                    elif st.kind == "done":
                        row.append((OP_DONE, bit_of[st.target]))
                    else:
                        has_sync_steps = True
                        is_iter = si == 1
                        k = st.target
                        if st.kind == "before":
                            row.append((OP_BEFORE,))
                            if is_iter:
                                iter_before[k].append((t, i))
                            else:
                                plain_before[k].append((t, si, i))
                        elif st.kind == "after":
                            row.append((OP_AFTER, is_iter, k))
                        else:
                            row.append((OP_AT, is_iter, k))
                            if is_iter:
                                iter_at[k].append((t, i))
                            else:
                                plain_at[k].append((t, si, i))
                comp.append(row)
            self.steps.append(comp)
            self.body_empty.append(len(th.body) == 0)
            self.body_len.append(len(th.body))

            # future accesses (block bit masks) from each position, for the reduction
            def masks(aids, kind_of=kind_of, block_of=block_of):
                r = w = 0
                for a in aids:
                    if kind_of[a] == "write":
                        w |= 1 << block_of[a]
                    else:
                        r |= 1 << block_of[a]
                return r, w

            seg_acts = [[a for a in kind_of if start_pos[a][0] == si] for si in range(3)]
            br, bw = masks(seg_acts[1])
            sr, sw = masks(seg_acts[2])
            fut_t = []
            for si, seg in enumerate(segs):
                row = []
                for i in range(len(seg) + 1):
                    r, w = masks([a for a in seg_acts[si] if start_pos[a][1] >= i])
                    if si <= 1:
                        r |= br | sr
                        w |= bw | sw
                    row.append((r, w))
                fut_t.append(row)
            fut_t.append([(0, 0)])
            self.fut.append(fut_t)
            fl = []
            for i in range(len(th.body) + 1):
                r, w = masks([a for a in seg_acts[1] if start_pos[a][1] >= i])
                fl.append((r | sr, w | sw))
            self.futlast.append(fl)

            # conflicting actions of the same thread whose intervals overlap
            cc_t = {}
            for a in kind_of:
                sa, ia = start_pos[a]
                da = done_pos[a][1]
                lst = []
                for b in kind_of:
                    if b == a or start_pos[b][0] != sa or block_of[a] != block_of[b]:
                        continue
                    if kind_of[a] != "write" and kind_of[b] != "write":
                        continue
                    ib = start_pos[b][1]
                    db = done_pos[b][1]
                    if ib < da and ia < db:
                        lst.append((bit_of[b], ib))
                cc_t[bit_of[a]] = tuple(lst)
            self.cc.append(cc_t)

        self.plain_sync = [(tuple(plain_at[h]), tuple(plain_before[h])) for h in range(K)]
        self.iter_sync = [(tuple(iter_at[j]), tuple(iter_before[j])) for j in range(Kb)]
        self.plain_at = [x for x in self.plain_sync if x[0]]
        self.iter_at = [x for x in self.iter_sync if x[0]]
        self.has_at = bool(self.plain_at or self.iter_at)
        self.has_sync_steps = has_sync_steps

    # ------------------------------------------------------------------ tables

    def intern(self, t) -> int:
        i = self.tid.get(t)
        if i is None:
            i = len(self.terms)
            self.tid[t] = i
            self.terms.append(t)
        return i

    def _obs(self, aid, v) -> int:
        key = (aid, v)
        o = self.obs_ids.get(key)
        if o is None:
            o = len(self.obs_list)
            self.obs_ids[key] = o
            self.obs_list.append(key)
        return o

    def _content(self, spec, vals) -> int:
        m = spec[0]
        if m == 0:
            return spec[1]
        if m == 1:
            return vals[spec[1]]
        slot_of = spec[2]
        terms = self.terms
        return self.intern(T.substitute(spec[1], lambda r: terms[vals[slot_of[r]]]))

    # ------------------------------------------------------------------ sync guards

    def _after_ok(self, is_iter, k, it, locs) -> bool:
        if is_iter:
            atl, bel = self.iter_sync[k]
            if atl:
                ta, ka = atl[0]
                return _passed_iter(locs[ta], it, ka)
            for tb, kb in bel:
                if not _passed_iter(locs[tb], it, kb):
                    return False
            return True
        atl, bel = self.plain_sync[k]
        if atl:
            ta, sa, ia = atl[0]
            l = locs[ta]
            return l[0] > sa or (l[0] == sa and l[2] > ia)
        for tb, sb, ib in bel:
            l = locs[tb]
            if not (l[0] > sb or (l[0] == sb and l[2] > ib)):
                return False
        return True

    def _fire(self, locs) -> bool:
        fired = False
        for atl, bel in self.plain_at:
            ok = True
            for ta, sa, ia in atl:
                l = locs[ta]
                if l[0] != sa or l[2] != ia:
                    ok = False
                    break
            if ok:
                for tb, sb, ib in bel:
                    l = locs[tb]
                    if not (l[0] > sb or (l[0] == sb and l[2] > ib)):
                        ok = False
                        break
            if ok:
                for ta, sa, ia in atl:
                    l = locs[ta]
                    locs[ta] = (l[0], l[1], l[2] + 1, l[3], l[4])
                fired = True
        for atl, bel in self.iter_at:
            ta, ka = atl[0]
            l = locs[ta]
            if l[0] != 1 or l[2] != ka:
                continue
            i = l[1]
            ok = True
            for tb, kb in atl[1:]:
                l2 = locs[tb]
                if l2[0] != 1 or l2[1] != i or l2[2] != kb:
                    ok = False
                    break
            if ok:
                for tb, kb in bel:
                    if not _passed_iter(locs[tb], i, kb):
                        ok = False
                        break
            if ok:
                for tb, kb in atl:
                    l2 = locs[tb]
                    locs[tb] = (l2[0], l2[1], l2[2] + 1, l2[3], l2[4])
                fired = True
        return fired

    # ------------------------------------------------------------------ closure

    def _advance(self, t, locs) -> bool:
        seg, it, idx, pend, vals = locs[t]
        segs = self.steps[t]
        moved = False
        vl = None
        while seg != 3:
            steps = segs[seg]
            if idx == len(steps):
                if seg == 0:
                    if self.body_empty[t]:
                        seg, it, idx = 2, -1, 0
                    else:
                        seg, it, idx = 1, 1, 0
                elif seg == 1:
                    break  # end of an iteration: loop or leave is a choice
                else:
                    seg, idx = 3, 0
                moved = True
                continue
            st = steps[idx]
            op = st[0]
            if op == OP_START:
                pend |= st[1]
                if st[2] >= 0:
                    if vl is None:
                        vl = list(vals)
                    vl[st[2]] = self._content(st[3], vl)
            elif op == OP_DONE:
                if pend & st[1]:
                    break
            elif op == OP_AFTER:
                locs[t] = (seg, it, idx, pend, tuple(vl) if vl is not None else vals)
                if not self._after_ok(st[1], st[2], it, locs):
                    break
            elif op == OP_AT:
                break
            idx += 1
            moved = True
        if moved:
            locs[t] = (seg, it, idx, pend, tuple(vl) if vl is not None else vals)
        return moved

    def close(self, locs) -> None:
        NT = self.NT
        if self.has_sync_steps:
            while True:
                prog = False
                for t in range(NT):
                    if self._advance(t, locs):
                        prog = True
                if self.has_at and self._fire(locs):
                    prog = True
                if not prog:
                    break
        else:
            for t in range(NT):
                self._advance(t, locs)
        for t in range(NT):
            l = locs[t]
            vals = l[4]
            if not vals:
                continue
            dead = self.dead[t][l[0]][l[2]]
            if dead:
                for s in dead:
                    if vals[s] != -1:
                        vl = list(vals)
                        for s2 in dead:
                            vl[s2] = -1
                        locs[t] = (l[0], l[1], l[2], l[3], tuple(vl))
                        break

    # ------------------------------------------------------------------ transitions

    def _effect(self, S, t, b):
        locs, blocks = S
        seg, it, idx, pend, vals = locs[t]
        aid, isw, blk, slot, spec = self.binfo[t][b]
        if isw:
            c = vals[slot] if slot >= 0 else self._content(spec, vals)
            nb = blocks[:blk] + (c,) + blocks[blk + 1:]
            o = -1
        else:
            v = blocks[blk]
            nb = blocks
            if slot >= 0:
                vals = vals[:slot] + (v,) + vals[slot + 1:]
            o = self._obs(aid, v)
        nl = list(locs)
        nl[t] = (seg, it, idx, pend & ~b, vals)
        self.close(nl)
        return (tuple(nl), nb), o

    def _safe(self, locs, lim):
        """An effect that commutes with everything else that can still happen, or None."""
        NT = self.NT
        fr = [0] * NT
        fw = [0] * NT
        anyp = False
        for t in range(NT):
            s, it, idx, pend, _ = locs[t]
            if s == 3:
                continue
            if pend:
                anyp = True
            if s == 1 and it == lim:
                r, w = self.futlast[t][idx]
            else:
                r, w = self.fut[t][s][idx]
            p = pend
            bi = self.binfo[t]
            while p:
                b = p & -p
                p ^= b
                inf = bi[b]
                if inf[1]:
                    w |= 1 << inf[2]
                else:
                    r |= 1 << inf[2]
            fr[t] = r
            fw[t] = w
        if not anyp:
            return None
        for t in range(NT):
            s, it, idx, pend, _ = locs[t]
            if not pend:
                continue
            ow = 0
            orw = 0
            for u in range(NT):
                if u != t:
                    ow |= fw[u]
                    orw |= fr[u] | fw[u]
            bi = self.binfo[t]
            cct = self.cc[t]
            p = pend
            while p:
                b = p & -p
                p ^= b
                inf = bi[b]
                bb = 1 << inf[2]
                if inf[1]:
                    if orw & bb:
                        continue
                elif ow & bb:
                    continue
                ok = True
                for ob, ost in cct[b]:
                    if idx <= ost or (pend & ob):
                        ok = False
                        break
                if ok:
                    return (t, b)
        return None

    def successors(self, S, L):
        locs, blocks = S
        c = -1
        maxit = 0
        for l in locs:
            s = l[0]
            if s >= 2:
                if l[1] >= 0:
                    c = l[1]
            elif s == 1 and l[1] > maxit:
                maxit = l[1]
        lim = c if c >= 0 else L
        e = self._safe(locs, lim)
        if e is not None:
            return [self._effect(S, e[0], e[1])]
        out = []
        for t in range(self.NT):
            l = locs[t]
            p = l[3]
            while p:
                b = p & -p
                p ^= b
                out.append(self._effect(S, t, b))
            if l[0] == 1 and l[2] == self.body_len[t]:
                it = l[1]
                if it < lim:
                    nl = list(locs)
                    nl[t] = (1, it + 1, 0, 0, l[4])
                    self.close(nl)
                    out.append(((tuple(nl), blocks), -1))
                if (c < 0 or c == it) and maxit <= it:
                    nl = list(locs)
                    nl[t] = (2, it, 0, 0, l[4])
                    self.close(nl)
                    out.append(((tuple(nl), blocks), -1))
        return out

    # ------------------------------------------------------------------ search

    def explore(self, L, deadline):
        """Answers for every count 1..L: a list indexed by count, or None on timeout."""
        init = [(0, 0, 0, 0, (-1,) * self.nslots[t]) for t in range(self.NT)]
        self.close(init)
        S0 = (tuple(init), self.init)
        off = array("q", [0])
        esid = array("q")
        eobs = array("q")
        finals = []
        allbits = ((1 << (L + 1)) - 1) ^ 1
        layer = {S0: 0}
        nid = 1
        cnt = 0
        while layer:
            nxt: dict = {}
            for S, g in layer.items():
                locs = S[0]
                if all(l[0] == 3 for l in locs):
                    c = -1
                    for l in locs:
                        if l[1] >= 0:
                            c = l[1]
                    finals.append((g, S[1], (1 << c) if c >= 0 else allbits))
                else:
                    for S2, o in self.successors(S, L):
                        h = nxt.get(S2)
                        if h is None:
                            h = nid
                            nxt[S2] = h
                            nid += 1
                        esid.append(h)
                        eobs.append(o)
                off.append(len(esid))
                cnt += 1
                if (cnt & 255) == 0 and deadline is not None and time.monotonic() > deadline:
                    return None
            layer = nxt

        total = nid
        mask = [0] * total
        for g, _, m in finals:
            mask[g] = m
        om = [0] * len(self.obs_list)
        for g in range(total - 1, -1, -1):
            a = off[g]
            b = off[g + 1]
            if a == b:
                continue
            m = 0
            for e in range(a, b):
                sm = mask[esid[e]]
                if sm:
                    m |= sm
                    o = eobs[e]
                    if o >= 0:
                        om[o] |= sm
            mask[g] = m

        rix = {r: i for i, r in enumerate(self.read_ids)}
        res = [[set() for _ in self.read_ids] for _ in range(L + 1)]
        fin = [[set() for _ in range(self.M)] for _ in range(L + 1)]
        terms = self.terms
        for o, m in enumerate(om):
            if not m:
                continue
            rid, v = self.obs_list[o]
            i = rix[rid]
            term = terms[v]
            while m:
                lb = m & -m
                m ^= lb
                k = lb.bit_length() - 1
                if 1 <= k <= L:
                    res[k][i].add(term)
        fm: dict = {}
        for g, blocks, _ in finals:
            m = mask[g]
            for b in range(self.M):
                key = (b, blocks[b])
                fm[key] = fm.get(key, 0) | m
        for (b, v), m in fm.items():
            term = terms[v]
            while m:
                lb = m & -m
                m ^= lb
                k = lb.bit_length() - 1
                if 1 <= k <= L:
                    fin[k][b].add(term)
        tab = [None]
        for k in range(1, L + 1):
            tab.append((tuple(frozenset(s) for s in res[k]), tuple(frozenset(s) for s in fin[k])))
        return tab


# ---------------------------------------------------------------------- driver


def _key(setup: LoopSetup) -> str:
    parts = [setup.blocks, setup.sync_points, setup.loop_sync_points,
             tuple(T.format_term(t) for t in setup.init)]
    for th in setup.threads:
        parts.append(th.id)
        for seg in (th.prefix, th.body, th.suffix):
            parts.append(repr([s.to_doc() for s in seg]))
    return repr(parts)


def _predict(hist, nxt) -> float:
    L1, t1 = hist[-1]
    e = 2.5
    if len(hist) >= 2:
        L0, t0 = hist[-2]
        if t0 > 0.02 and t1 > 0.02 and L1 > L0:
            e = math.log(t1 / t0) / math.log(L1 / L0)
            e = min(4.0, max(1.0, e))
    return t1 * (nxt / L1) ** e


def _extend(ent, n) -> None:
    cp = ent["cp"]
    soft = time.monotonic() + BUDGET
    while True:
        L = ent["L"]
        if L >= n:
            return
        if L >= CAPMAX:
            ent["done"] = True
            return
        if L == 0:
            nxt = min(n, 2)
        else:
            nxt = min(n, CAPMAX, max(L + 1, (L * 3) // 2))
        now = time.monotonic()
        if L == 0:
            deadline = None  # the first table is always needed
        else:
            if now + _predict(ent["hist"], nxt) > soft:
                ent["done"] = True
                return
            deadline = soft
        tab = cp.explore(nxt, deadline)
        if tab is None:
            ent["done"] = True
            return
        ent["hist"].append((nxt, time.monotonic() - now))
        ent["L"] = nxt
        ent["tab"] = tab


def _pick(tab, L, n) -> int:
    """The count in 1..L whose answers equal those for ``n`` (eventual periodicity)."""
    if n <= L:
        return n
    if L <= 1:
        return L

    def start(p):
        for k in range(L - p, 0, -1):
            if tab[k] != tab[k + p]:
                return k + 1
        return 1

    chosen = None
    for p in range(1, L):
        if 3 * p > L:
            break
        t0 = start(p)
        if L - t0 + 1 >= max(3 * p, p + 4):
            chosen = (t0, p)
            break
    if chosen is None:
        best = None
        for p in range(1, L):
            t0 = start(p)
            if best is None or t0 + p < best[0] + best[1]:
                best = (t0, p)
        chosen = best
    t0, p = chosen
    return t0 + (n - t0) % p


@register
class StateSpaceLoopSolver(LoopSolver):
    name = "opus55_1-s-statespace"
    description = ("State-space search with per-thread iteration counters (all counts up to a cap "
                   "at once), eager non-effect steps and a one-effect reduction; periodic extension beyond the cap")
    capabilities = Capabilities(rcw=False, sync=True, observed_reads=False)

    def solve(self, setup: LoopSetup, n: int) -> LoopOutcomes:
        n = int(n)
        if n < 1:
            raise ValueError("n must be >= 1")
        key = _key(setup)
        ent = _CACHE.get(key)
        if ent is None:
            if len(_CACHE) >= _CACHE_MAX:
                _CACHE.clear()
            ent = {"cp": _Compiled(setup), "L": 0, "tab": None, "done": False, "hist": []}
            _CACHE[key] = ent
        if n > ent["L"] and not ent["done"]:
            _extend(ent, n)
        cp, tab, L = ent["cp"], ent["tab"], ent["L"]
        m = _pick(tab, L, n)
        res_t, fin_t = tab[m]
        results = {rid: set(res_t[i]) for i, rid in enumerate(cp.read_ids)}
        final = {b: set(fin_t[b]) for b in range(cp.M)}
        return LoopOutcomes(results=results, final=final)
