"""Loop solver, case b: possibility sets of the unrolled setup P_n.

Model (derived from spec v3, sections 3-5 and 8, with no sync points):

* Starts and ends touch no memory, so a full schedule is fixed by the order of the
  effect points. Inside one thread, action ``a`` must take effect before ``b`` exactly
  when ``a`` ends before ``b`` starts in program order. Any order of the effects that
  respects this, per thread, is realisable by some linearization: the threads are not
  linked to each other, and a point can be placed in each interval greedily.
* Every action ends in the segment and iteration it starts in, so the effects of one
  thread go segment by segment and iteration by iteration.
* We explore the global states: for each thread, its segment, the set of actions of the
  current segment (or iteration) that have already taken effect, and how many body
  iterations it has completed; plus the block contents and the read values still
  needed by later writes. Nothing ever blocks, so every reachable state completes.
  This means a read can return ``v`` exactly when some reachable state has that read
  enabled while its block holds ``v``.
* The iteration count is handled for all ``n`` at once. Before any thread leaves its
  body, a state is valid for every ``n`` at least the largest current iteration index.
  Once a thread leaves its body after ``m`` iterations, ``n = m`` is fixed, and every
  other thread must do exactly ``m`` iterations.
* The search goes level by level: level ``N`` allows iteration indices up to ``N``,
  so after level ``N`` the answers are exact for every ``n <= N``. For larger ``n`` a
  fact seen before any thread leaves its body holds for all larger ``n``. Facts that
  need some thread to have left its body are extended past the explored range by the
  periodic pattern their membership shows over ``1..N``.
* Partial-order reduction: if every effect a thread can take next commutes with
  everything the other threads may still do, only that thread is expanded.
"""

from __future__ import annotations

import time

from harness import terms as T
from harness.capabilities import Capabilities
from harness.loop.api import LoopOutcomes, LoopSolver
from harness.registry import register

PREFIX, BODY, SUFFIX, DONE = 0, 1, 2, 3
SEG_NAMES = ("prefix", "body", "suffix")
VMUL = 1 << 32

HARD = 13.0  # seconds per call: abort exploration (resumable) after this
SOFT_EXACT = 8.0  # n <= NMAX: do not start a new level after this
SOFT_LARGE = 4.0  # n > NMAX: do not start a new level after this
NMAX = 256  # deepest level explored
STATE_CAP = 2_000_000


class _Act:
    __slots__ = ("id", "thread", "seg", "j", "kind", "block", "data")

    def __init__(self, aid, thread, seg, j, kind, block, data):
        self.id = aid
        self.thread = thread
        self.seg = seg
        self.j = j
        self.kind = kind
        self.block = block
        self.data = data


def _extrapolate(seq, n):
    """``seq[1..nc]`` is exact membership; extend it periodically to ``n > nc``."""
    nc = len(seq) - 1
    if nc <= 0:
        return False
    for p in range(1, nc // 2 + 1):
        a = 1
        for k in range(nc - p, 0, -1):
            if seq[k] != seq[k + p]:
                a = k + 1
                break
        if nc - a + 1 >= 2 * p:
            return seq[a + (n - a) % p]
    return seq[nc]


class _Engine:
    def __init__(self, setup):
        nT = len(setup.threads)
        M = setup.blocks
        self.T = nT
        self.M = M
        self.mi = 2 * nT
        self.mem0 = 2 * nT + 1
        self.slot0 = self.mem0 + M
        self.terms = []
        self.term_ids = {}

        act = {}
        seg_ids = []
        seg_pred = []
        for ti, th in enumerate(setup.threads):
            ids3, pred3 = [], []
            for si, name in enumerate(SEG_NAMES):
                steps = th.segment(name)
                ids, startp, donep = [], {}, {}
                for pos, st in enumerate(steps):
                    if st.is_start:
                        startp[st.id] = pos
                        act[st.id] = _Act(st.id, ti, si, len(ids), st.kind, st.target, st.data)
                        ids.append(st.id)
                    elif st.kind == "done":
                        donep[st.target] = pos
                end = len(steps)
                preds = []
                for a in ids:
                    pm = 0
                    for i, b in enumerate(ids):
                        if donep.get(b, end) < startp[a]:
                            pm |= 1 << i
                    preds.append(pm)
                ids3.append(ids)
                pred3.append(preds)
            seg_ids.append(ids3)
            seg_pred.append(pred3)
        self.act = act

        # read slots
        self.read_list = []
        read_index = {}
        slotpos = {}
        thread_slots = []
        k = self.slot0
        for ti in range(nT):
            sl = []
            for si in range(3):
                for aid in seg_ids[ti][si]:
                    if act[aid].kind == "read":
                        read_index[aid] = len(self.read_list)
                        self.read_list.append(aid)
                        slotpos[aid] = k
                        sl.append(aid)
                        k += 1
            thread_slots.append(sl)
        self.nslots = k - self.slot0
        self.slotpos = slotpos
        self.final_base = len(self.read_list) * VMUL

        # writes
        self.wids = []
        widx = {}
        for aid, a in act.items():
            if a.kind != "read":
                widx[aid] = len(self.wids)
                self.wids.append(aid)
        memo = {}

        def deps_of(aid):
            if aid in memo:
                return memo[aid]
            a = act[aid]
            out = set()
            if a.data is not None:
                for r in T.refs(a.data):
                    b = act.get(r)
                    if b is None:
                        continue
                    if b.kind == "read":
                        out.add(slotpos[r])
                    else:
                        out |= deps_of(r)
            memo[aid] = frozenset(out)
            return memo[aid]

        self.wdepset = [deps_of(w) for w in self.wids]
        self.wdeps = [tuple(sorted(d)) for d in self.wdepset]
        self.wcache = [dict() for _ in self.wids]
        self.wconst = [self._intern(self._wterm(w, None)) if not self.wdeps[i] else -1
                       for i, w in enumerate(self.wids)]

        self.trans, self.clear, self.isb = [], [], []
        self.frf, self.fwf, self.frl, self.fwl, self.er, self.ew = [], [], [], [], [], []
        self.counted, self.body_start, self.suffix_start, self.start_loc = [], [], [], []
        for ti in range(nT):
            self._build_thread(ti, seg_ids[ti], seg_pred[ti], thread_slots[ti], read_index, widx)

        init = [0] * self.slot0 + [-1] * self.nslots
        for t in range(nT):
            init[t] = self.start_loc[t]
        for b in range(M):
            init[self.mem0 + b] = self._intern(setup.init[b])
        self.init = tuple(init)

        self.visited = set()
        self.stack = []
        self.deferred = {}
        self.lmin = {}
        self.mset = {}
        self.Nc = 0
        self.cur_level = 0
        self.complete = False
        self.capped = False
        self.last_level_time = 0.0

    # ------------------------------------------------------------------ terms

    def _intern(self, term):
        i = self.term_ids.get(term)
        if i is None:
            i = len(self.terms)
            self.terms.append(term)
            self.term_ids[term] = i
        return i

    def _wterm(self, aid, s):
        a = self.act[aid]
        if a.data is None:
            return T.Unk(aid)

        def look(r):
            b = self.act[r]
            if b.kind == "read":
                v = s[self.slotpos[r]]
                if v < 0:
                    raise RuntimeError(f"value of read {r} is not available for {aid}")
                return self.terms[v]
            return self._wterm(r, s)

        return T.substitute(a.data, look)

    def _content(self, wi, s):
        deps = self.wdeps[wi]
        if not deps:
            return self.wconst[wi]
        if len(deps) == 1:
            key = s[deps[0]]
        else:
            key = tuple([s[p] for p in deps])
        c = self.wcache[wi]
        v = c.get(key)
        if v is None:
            v = self._intern(self._wterm(self.wids[wi], s))
            c[key] = v
        return v

    # ------------------------------------------------------------------ thread tables

    def _build_thread(self, ti, ids3, pred3, slots, read_index, widx):
        act = self.act
        slotpos = self.slotpos
        full = [(1 << len(ids3[s])) - 1 for s in range(3)]
        nb = len(ids3[BODY])
        locid = {}
        seglist, masklist, work = [], [], []

        def get(seg, mask):
            key = (seg, mask)
            i = locid.get(key)
            if i is None:
                i = len(seglist)
                locid[key] = i
                seglist.append(seg)
                masklist.append(mask)
                work.append(i)
            return i

        get(DONE, 0)  # id 0

        def norm(seg, mask):
            while True:
                if seg == DONE:
                    return 0
                if mask == full[seg]:
                    if seg == PREFIX:
                        seg = BODY if nb else SUFFIX
                        mask = 0
                        continue
                    if seg == BODY:
                        return -1
                    seg, mask = DONE, 0
                    continue
                return get(seg, mask)

        start = norm(PREFIX, 0)
        bstart = get(BODY, 0) if nb else -1
        sstart = norm(SUFFIX, 0)

        def fp(aids):
            r = w = 0
            for aid in aids:
                a = act[aid]
                if a.kind == "read":
                    r |= 1 << a.block
                else:
                    w |= 1 << a.block
            return r, w

        def rest(seg, mask):
            return [aid for j, aid in enumerate(ids3[seg]) if not (mask >> j) & 1]

        def writes(aids):
            return [aid for aid in aids if act[aid].kind != "read"]

        allb = fp(ids3[BODY])
        alls = fp(ids3[SUFFIX])
        body_w = writes(ids3[BODY])
        suf_w = writes(ids3[SUFFIX])

        trans, clear, isb, frf, fwf, frl, fwl, er, ew = {}, {}, {}, {}, {}, {}, {}, {}, {}
        wi = 0
        while wi < len(work):
            loc = work[wi]
            wi += 1
            seg, mask = seglist[loc], masklist[loc]
            if seg == DONE:
                trans[loc] = ()
                clear[loc] = tuple(slotpos[a] for a in slots)
                isb[loc] = False
                frf[loc] = fwf[loc] = frl[loc] = fwl[loc] = er[loc] = ew[loc] = 0
                continue
            tl = []
            e_r = e_w = 0
            for j, aid in enumerate(ids3[seg]):
                if (mask >> j) & 1 or (pred3[seg][j] & ~mask):
                    continue
                a = act[aid]
                target = norm(seg, mask | (1 << j))
                if a.kind == "read":
                    tl.append((True, self.mem0 + a.block, slotpos[aid], read_index[aid] * VMUL, target))
                    e_r |= 1 << a.block
                else:
                    tl.append((False, self.mem0 + a.block, widx[aid], 0, target))
                    e_w |= 1 << a.block
            trans[loc] = tuple(tl)
            er[loc] = e_r
            ew[loc] = e_w
            cur = rest(seg, mask)
            r0, w0 = fp(cur)
            if seg == PREFIX:
                frf[loc] = frl[loc] = r0 | allb[0] | alls[0]
                fwf[loc] = fwl[loc] = w0 | allb[1] | alls[1]
            elif seg == BODY:
                frf[loc] = allb[0] | alls[0]
                fwf[loc] = allb[1] | alls[1]
                frl[loc] = r0 | alls[0]
                fwl[loc] = w0 | alls[1]
            else:
                frf[loc] = frl[loc] = r0
                fwf[loc] = fwl[loc] = w0
            isb[loc] = seg == BODY

            # which read values are still needed
            cur_w = writes(cur)
            if seg == PREFIX:
                pw_pre = cur_w + body_w + suf_w
            elif seg == BODY:
                pw_pre = body_w + suf_w
            else:
                pw_pre = cur_w
            cl = []
            for r in slots:
                a = act[r]
                sp = slotpos[r]
                eff = a.seg < seg or (a.seg == seg and (mask >> a.j) & 1)
                keep = False
                if eff:
                    if a.seg == PREFIX:
                        cand = pw_pre
                    elif a.seg == seg:  # body read in body, suffix read in suffix
                        cand = cur_w
                    else:
                        cand = []
                    keep = any(sp in self.wdepset[widx[w]] for w in cand)
                if not keep:
                    cl.append(sp)
            clear[loc] = tuple(cl)

        n = len(seglist)
        self.trans.append([trans[i] for i in range(n)])
        self.clear.append([clear[i] for i in range(n)])
        self.isb.append([isb[i] for i in range(n)])
        self.frf.append([frf[i] for i in range(n)])
        self.fwf.append([fwf[i] for i in range(n)])
        self.frl.append([frl[i] for i in range(n)])
        self.fwl.append([fwl[i] for i in range(n)])
        self.er.append([er[i] for i in range(n)])
        self.ew.append([ew[i] for i in range(n)])
        self.counted.append(nb > 0)
        self.body_start.append(bstart)
        self.suffix_start.append(sstart)
        self.start_loc.append(start)

    # ------------------------------------------------------------------ search

    def _explore(self, level, deadline):
        nT = self.T
        mi = self.mi
        mem0 = self.mem0
        M = self.M
        stack = self.stack
        visited = self.visited
        trans = self.trans
        clear = self.clear
        isb = self.isb
        frf, fwf, frl, fwl, er, ew = self.frf, self.fwf, self.frl, self.fwl, self.er, self.ew
        counted = self.counted
        body_start = self.body_start
        suffix_start = self.suffix_start
        lmin = self.lmin
        mset = self.mset
        deferred = self.deferred
        final_base = self.final_base
        content = self._content
        threads = range(nT)
        big = 1 << 62
        perf = time.perf_counter
        pops = 0
        while stack:
            pops += 1
            if not (pops & 1023):
                if perf() > deadline:
                    return False
                if len(visited) > STATE_CAP:
                    self.capped = True
                    return False
            s = stack.pop()
            m = s[mi]
            active = [t for t in threads if s[t]]
            if not active:
                for b in range(M):
                    key = final_base + b * VMUL + s[mem0 + b]
                    if m:
                        ms = mset.get(key)
                        if ms is None:
                            mset[key] = {m}
                        else:
                            ms.add(m)
                    elif lmin.get(key, big) > 1:
                        lmin[key] = 1
                continue
            L = 1
            if not m:
                for t in active:
                    if counted[t] and isb[t][s[t]]:
                        i = s[nT + t] + 1
                        if i > L:
                            L = i
            if len(active) == 1:
                expand = active
            else:
                fr = {}
                fw = {}
                for t in active:
                    loc = s[t]
                    if m and isb[t][loc] and s[nT + t] + 1 == m:
                        fr[t] = frl[t][loc]
                        fw[t] = fwl[t][loc]
                    else:
                        fr[t] = frf[t][loc]
                        fw[t] = fwf[t][loc]
                expand = active
                for t in active:
                    orr = 0
                    ow = 0
                    for u in active:
                        if u != t:
                            orr |= fr[u]
                            ow |= fw[u]
                    loc = s[t]
                    if not (er[t][loc] & ow) and not (ew[t][loc] & (ow | orr)):
                        expand = (t,)
                        break
            for t in expand:
                loc = s[t]
                clr = clear[t]
                for is_read, mpos, ref, fbase, target in trans[t][loc]:
                    new = list(s)
                    if is_read:
                        v = s[mpos]
                        key = fbase + v
                        if m:
                            ms = mset.get(key)
                            if ms is None:
                                mset[key] = {m}
                            else:
                                ms.add(m)
                        elif lmin.get(key, big) > L:
                            lmin[key] = L
                        new[ref] = v
                    else:
                        new[mpos] = content(ref, s)
                    if target >= 0:
                        new[t] = target
                        for p in clr[target]:
                            new[p] = -1
                        tup = tuple(new)
                        if tup not in visited:
                            visited.add(tup)
                            stack.append(tup)
                        continue
                    # end of a body iteration: continue or leave the body
                    c1 = s[nT + t] + 1
                    new[nT + t] = c1
                    if m:
                        do_cont = c1 < m
                        do_exit = c1 == m
                    else:
                        do_cont = True
                        do_exit = True
                        for u in active:
                            if u != t and counted[u] and isb[u][s[u]] and s[nT + u] + 1 > c1:
                                do_exit = False
                                break
                    if do_exit:
                        ex = list(new)
                        tgt = suffix_start[t]
                        ex[t] = tgt
                        for p in clr[tgt]:
                            ex[p] = -1
                        if not m:
                            ex[mi] = c1
                        tup = tuple(ex)
                        if tup not in visited:
                            visited.add(tup)
                            stack.append(tup)
                    if do_cont:
                        tgt = body_start[t]
                        new[t] = tgt
                        for p in clr[tgt]:
                            new[p] = -1
                        tup = tuple(new)
                        if not m and c1 + 1 > level:
                            lst = deferred.get(c1 + 1)
                            if lst is None:
                                deferred[c1 + 1] = [tup]
                            else:
                                lst.append(tup)
                        elif tup not in visited:
                            visited.add(tup)
                            stack.append(tup)
        return True

    def advance(self, n, t0):
        deadline = t0 + HARD
        target = n if n <= NMAX else NMAX
        soft = SOFT_EXACT if n <= NMAX else SOFT_LARGE
        while not self.complete and not self.capped:
            if not self.stack:
                if self.Nc >= target:
                    return
                now = time.perf_counter()
                if self.Nc >= 1:
                    if now - t0 > soft or now + 1.7 * self.last_level_time > deadline - 1.0:
                        return
                level = self.Nc + 1
                self.cur_level = level
                items = [self.init] if level == 1 else self.deferred.pop(level, [])
                for tup in items:
                    if tup not in self.visited:
                        self.visited.add(tup)
                        self.stack.append(tup)
            ls = time.perf_counter()
            ok = self._explore(self.cur_level, deadline)
            if not ok:
                return
            self.last_level_time = time.perf_counter() - ls
            self.Nc = self.cur_level
            if not self.deferred:
                self.complete = True

    # ------------------------------------------------------------------ answers

    def _holds(self, key, n):
        lo = self.lmin.get(key)
        if lo is not None and n >= lo:
            return True
        ms = self.mset.get(key)
        if ms is not None and n in ms:
            return True
        if n <= self.Nc or self.complete:
            return False
        nc = self.Nc
        seq = [False] * (nc + 1)
        for k in range(1, nc + 1):
            seq[k] = (lo is not None and k >= lo) or (ms is not None and k in ms)
        return _extrapolate(seq, n)

    def answer(self, n):
        R = len(self.read_list)
        res = {rid: set() for rid in self.read_list}
        fin = {b: set() for b in range(self.M)}
        for key in set(self.lmin) | set(self.mset):
            kind, v = divmod(key, VMUL)
            if self._holds(key, n):
                term = self.terms[v]
                if kind < R:
                    res[self.read_list[kind]].add(term)
                else:
                    fin[kind - R].add(term)
        return LoopOutcomes(results=res, final=fin)


def _setup_key(setup):
    threads = []
    for th in setup.threads:
        segs = []
        for name in SEG_NAMES:
            segs.append(tuple((s.kind, s.target, s.id, s.data, s.expect) for s in th.segment(name)))
        threads.append((th.id, tuple(segs)))
    return (setup.blocks, setup.sync_points, setup.loop_sync_points, tuple(setup.init), tuple(threads))


_CACHE: dict = {}


@register
class ExploreLoopSolver(LoopSolver):
    name = "opus55_1-b-explore"
    description = "state exploration over all n at once, level by level, with periodic extension past the explored n"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)

    def solve(self, setup, n):
        t0 = time.perf_counter()
        n = int(n)
        key = _setup_key(setup)
        eng = _CACHE.get("eng")
        if eng is None or _CACHE.get("key") != key:
            _CACHE.clear()
            eng = _Engine(setup)
            _CACHE["key"] = key
            _CACHE["eng"] = eng
        eng.advance(n, t0)
        return eng.answer(n)
