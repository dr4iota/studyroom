"""Counter of |Lin(P_n)| for loop setups with sync points (task looplin, case s).

Outline (details in SOURCES.md):

* Threads linked through a sync point form a group. Groups and the unused (isolated)
  sync points are independent, so their counts combine with a multinomial coefficient.
* A group's poset is split recursively into connected components (multinomial) and
  ordinal-sum pieces (product). Isomorphic pieces are counted once (memo by a canonical
  key built from iteration-relative labels).
* An irreducible piece is counted by a dynamic program over its down-sets, with special
  handling for sync nodes that are not on any thread's chain.
* For large ``n`` the decomposition of a few small unrollings is extrapolated (the
  multiplicities and sizes of the pieces must be affine in ``n`` on four consecutive
  values); otherwise ``P_n`` is built and decomposed directly.

Write data never matters for ``Lin(P_n)``, so it is ignored.
"""

from __future__ import annotations

import math

from harness.capabilities import Capabilities
from harness.loop.api import LoopCounter
from harness.registry import register

_MEMO_LIMIT = 4096  # pieces larger than this are not memoized


# ---------------------------------------------------------------------- poset building


class _Poset:
    """The trace poset of one thread group of ``P_m``.

    pred/succ: edge lists (deduplicated); tch: thread chain the node is assigned to
    (``-1`` for a sync node that is on no thread's chain); tpos: position in that
    thread's program order; lab: interned label of the base step; it: iteration (body
    nodes) or 0; body: whether the node belongs to a body iteration.
    """

    __slots__ = ("pred", "succ", "tch", "tpos", "lab", "it", "body")

    def __init__(self) -> None:
        self.pred: list[list[int]] = []
        self.succ: list[list[int]] = []
        self.tch: list[int] = []
        self.tpos: list[int] = []
        self.lab: list[int] = []
        self.it: list[int] = []
        self.body: list[bool] = []


def _build(setup, threads, m: int, labid: dict) -> _Poset:
    P = _Poset()
    lab, it, body, tch, tpos = P.lab, P.it, P.body, P.tch, P.tpos
    syncs: dict = {}
    edges: set = set()

    def new(label, i, isb) -> int:
        lid = labid.get(label)
        if lid is None:
            lid = len(labid)
            labid[label] = lid
        lab.append(lid)
        it.append(i)
        body.append(isb)
        tch.append(-1)
        tpos.append(0)
        return len(lab) - 1

    def sync(isb, k, i) -> int:
        key = ("j", k, i) if isb else ("h", k)
        u = syncs.get(key)
        if u is None:
            u = new(("j", k) if isb else ("h", k), i if isb else 0, isb)
            syncs[key] = u
        return u

    for t in threads:
        th = setup.threads[t]
        chain: list[int] = []
        segs = [("prefix", th.prefix, 0, False)]
        segs += [("body", th.body, i, True) for i in range(1, m + 1)]
        segs.append(("suffix", th.suffix, 0, False))
        for segname, steps, i, isb in segs:
            for si, s in enumerate(steps):
                kind = s.kind
                if kind == "at":
                    u = sync(isb, s.target, i)
                    if tch[u] == -1:
                        tch[u] = t
                        tpos[u] = len(chain)
                else:
                    u = new(("s", t, segname, si), i, isb)
                    tch[u] = t
                    tpos[u] = len(chain)
                    if kind == "before":
                        edges.add((u, sync(isb, s.target, i)))
                    elif kind == "after":
                        edges.add((sync(isb, s.target, i), u))
                if chain:
                    edges.add((chain[-1], u))
                chain.append(u)

    V = len(lab)
    pred: list[list[int]] = [[] for _ in range(V)]
    succ: list[list[int]] = [[] for _ in range(V)]
    for u, v in edges:
        succ[u].append(v)
        pred[v].append(u)
    P.pred, P.succ = pred, succ
    return P


# ---------------------------------------------------------------------- helpers


def _key(P: _Poset, nodes) -> tuple:
    """Canonical description of the sub-poset on ``nodes`` (equal keys: isomorphic)."""
    if len(nodes) == 1:
        return ("single",)
    lab, it, body = P.lab, P.it, P.body
    base = None
    for u in nodes:
        if body[u] and (base is None or it[u] < base):
            base = it[u]
    sig = {}
    for u in nodes:
        sig[u] = (lab[u], it[u] - base) if body[u] else (lab[u], 0)
    order = sorted(nodes, key=sig.__getitem__)
    rank = {u: r for r, u in enumerate(order)}
    succ = P.succ
    edges = []
    for u in order:
        ru = rank[u]
        for v in succ[u]:
            rv = rank.get(v)
            if rv is not None:
                edges.append((ru, rv))
    edges.sort()
    return (tuple(sig[u] for u in order), tuple(edges))


def _components(P: _Poset, nodes) -> list[list[int]]:
    inset = set(nodes)
    seen: set = set()
    comps = []
    pred, succ = P.pred, P.succ
    for s0 in nodes:
        if s0 in seen:
            continue
        seen.add(s0)
        comp = [s0]
        stack = [s0]
        while stack:
            x = stack.pop()
            for y in pred[x]:
                if y in inset and y not in seen:
                    seen.add(y)
                    comp.append(y)
                    stack.append(y)
            for y in succ[x]:
                if y in inset and y not in seen:
                    seen.add(y)
                    comp.append(y)
                    stack.append(y)
        comps.append(comp)
    return comps


def _local(P: _Poset, nodes):
    """Local adjacency and chain partition of the sub-poset on ``nodes``."""
    V = len(nodes)
    loc = {u: i for i, u in enumerate(nodes)}
    lp: list[list[int]] = [[] for _ in range(V)]
    ls: list[list[int]] = [[] for _ in range(V)]
    succ = P.succ
    for i, u in enumerate(nodes):
        for v in succ[u]:
            j = loc.get(v)
            if j is not None:
                ls[i].append(j)
                lp[j].append(i)
    tch, tpos = P.tch, P.tpos
    cmap: dict = {}
    members: list[list[int]] = []
    free: list[int] = []
    for i, u in enumerate(nodes):
        c = tch[u]
        if c < 0:
            free.append(i)
            continue
        ci = cmap.get(c)
        if ci is None:
            ci = len(members)
            cmap[c] = ci
            members.append([])
        members[ci].append(i)
    for mem in members:
        mem.sort(key=lambda i: tpos[nodes[i]])
    return lp, ls, members, free


def _ordinal_pieces(P: _Poset, nodes) -> list[list[int]]:
    """Split ``nodes`` into the finest ordinal sum ``Q1 ⊕ Q2 ⊕ …`` (in order)."""
    V = len(nodes)
    if V <= 1:
        return [list(nodes)]
    lp, ls, members, free = _local(P, nodes)
    isfree = [False] * V
    for i in free:
        isfree[i] = True
    C = len(members)
    cidx = [-1] * V
    cpos = [-1] * V
    for ci, mem in enumerate(members):
        for p, i in enumerate(mem):
            cidx[i] = ci
            cpos[i] = p

    # Topological order; a free node is emitted right after the node that enabled it.
    indeg = [len(x) for x in lp]
    fr = [i for i in range(V) if indeg[i] == 0 and isfree[i]]
    tr = [i for i in range(V) if indeg[i] == 0 and not isfree[i]]
    order: list[int] = []
    fgroups: dict = {}
    last = -1
    while fr or tr:
        if fr:
            x = fr.pop()
            fgroups.setdefault(last, []).append(x)
        else:
            x = tr.pop()
            last = x
        order.append(x)
        for y in ls[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                (fr if isfree[y] else tr).append(y)
    t = [0] * V
    for k, x in enumerate(order):
        t[x] = k

    # g[x][c]: smallest position on chain c of a chain node >= x (len(chain) if none).
    clen = [len(mem) for mem in members]
    g: list = [None] * V
    rc = range(C)
    for x in reversed(order):
        vec = clen[:]
        for y in ls[x]:
            gy = g[y]
            for c in rc:
                if gy[c] < vec[c]:
                    vec[c] = gy[c]
        if not isfree[x]:
            vec[cidx[x]] = cpos[x]
        g[x] = vec

    # far(a): last position in the order of a node that is not >= a.
    cover = [0] * (V + 1)
    for a in range(V):
        gv = g[a]
        best = -1
        xs = -1
        for c in rc:
            q = gv[c] - 1
            if q >= 0:
                node = members[c][q]
                if t[node] > best:
                    best = t[node]
                    xs = node
        grp = fgroups.get(xs)
        if grp:
            for s in reversed(grp):
                if s == a:
                    continue
                if t[s] <= best:
                    break
                inup = False
                for p in lp[s]:
                    if cpos[p] >= gv[cidx[p]]:
                        inup = True
                        break
                if not inup:
                    best = t[s]
                    break
        ta = t[a]
        if best > ta:
            cover[ta + 1] += 1
            cover[best + 1] -= 1

    pieces = []
    run = 0
    start = 0
    for k in range(1, V):
        run += cover[k]
        if run == 0:
            pieces.append([nodes[x] for x in order[start:k]])
            start = k
    pieces.append([nodes[x] for x in order[start:]])
    return pieces


def _multinomial(parts) -> int:
    """Number of interleavings of independent parts given as ``(size, multiplicity)``."""
    r = 1
    tot = 0
    for sz, mult in parts:
        if sz == 0 or mult == 0:
            continue
        if mult == 1:
            tot += sz
            r *= math.comb(tot, sz)
        elif sz == 1:
            r *= math.perm(tot + mult, mult)
            tot += mult
        else:
            add = sz * mult
            r *= math.perm(tot + add, add) // pow(math.factorial(sz), mult)
            tot += add
    return r


# ---------------------------------------------------------------------- down-set DP


def _dp_pure(lp, members, V: int) -> int:
    """Down-set DP when every node lies on a chain."""
    nc = len(members)
    ci_of = [-1] * V
    pi_of = [0] * V
    for ci, mem in enumerate(members):
        for p, i in enumerate(mem):
            ci_of[i] = ci
            pi_of[i] = p
    req = []
    for ci, mem in enumerate(members):
        row = []
        for x in mem:
            d: dict = {}
            for y in lp[x]:
                c = ci_of[y]
                if c == ci:
                    continue
                q = pi_of[y]
                if c not in d or q > d[c]:
                    d[c] = q
            row.append(tuple(d.items()))
        req.append(row)
    lens = tuple(len(m) for m in members)
    cur = {(0,) * nc: 1}
    for _ in range(V):
        nxt: dict = {}
        get = nxt.get
        for st, val in cur.items():
            for ci in range(nc):
                p = st[ci]
                if p == lens[ci]:
                    continue
                for c2, p2 in req[ci][p]:
                    if st[c2] <= p2:
                        break
                else:
                    ns = st[:ci] + (p + 1,) + st[ci + 1:]
                    nxt[ns] = get(ns, 0) + val
        cur = nxt
    return cur.get(lens, 0)


def _dp(P: _Poset, nodes) -> int:
    """Number of linear extensions of the sub-poset on ``nodes`` (any poset)."""
    V = len(nodes)
    lp, ls, members, free = _local(P, nodes)
    if not free:
        return _dp_pure(lp, members, V)

    # Off-chain nodes with no successors would need a counter in the state; nodes with no
    # predecessors are inserted lazily. Run in the direction that makes more of them lazy.
    nlazy = npend = 0
    for i in free:
        if lp[i] and not ls[i]:
            npend += 1
        elif ls[i] and not lp[i]:
            nlazy += 1
    if npend > nlazy:
        lp, ls = ls, lp
        for mem in members:
            mem.reverse()

    nc = len(members)
    ci_of = [-1] * V
    pi_of = [0] * V
    for ci, mem in enumerate(members):
        for p, i in enumerate(mem):
            ci_of[i] = ci
            pi_of[i] = p

    def cmin(lst):
        d: dict = {}
        for b in lst:
            c, p = ci_of[b], pi_of[b]
            if c not in d or p < d[c]:
                d[c] = p
        return tuple(d.items())

    def cmax(lst):
        d: dict = {}
        for b in lst:
            c, p = ci_of[b], pi_of[b]
            if c not in d or p > d[c]:
                d[c] = p
        return tuple(d.items())

    bp_at: list[list] = [[] for _ in range(V)]  # windowed nodes that must precede x
    en_at: list[list] = [[] for _ in range(V)]  # windowed nodes x may enable
    lz_at: list[list] = [[] for _ in range(V)]  # lazy nodes that must precede x
    tg_at: list[list] = [[] for _ in range(V)]  # successor-free nodes x may release
    cp0 = 0
    for s in free:
        a, b = lp[s], ls[s]
        if a and b:
            sc, pc = cmin(b), cmax(a)
            for x in b:
                bp_at[x].append((s, sc))
            for x in a:
                en_at[x].append((s, pc))
        elif b:
            sc = cmin(b)
            for x in b:
                lz_at[x].append(sc)
        elif a:
            pc = cmax(a)
            for x in a:
                tg_at[x].append(pc)
        else:
            cp0 += 1

    info = []
    for ci, mem in enumerate(members):
        row = []
        for x in mem:
            d: dict = {}
            for y in lp[x]:
                c = ci_of[y]
                if c < 0 or c == ci:
                    continue
                q = pi_of[y]
                if c not in d or q > d[c]:
                    d[c] = q
            row.append((tuple(d.items()), tuple(bp_at[x]), tuple(lz_at[x]), tuple(tg_at[x]), tuple(en_at[x])))
        info.append(row)

    lens = tuple(len(m) for m in members)
    empty: frozenset = frozenset()
    start = (0,) * nc
    openmap = {start: empty}  # positions -> windowed nodes enabled and not yet forced
    buckets: dict = {0: {(start, cp0, empty): 1}}
    for size in range(V + 1):
        cur = buckets.pop(size, None)
        if not cur:
            continue
        if size == V:
            return cur.get((lens, 0, empty), 0)
        n1 = buckets.get(size + 1)
        if n1 is None:
            n1 = buckets[size + 1] = {}
        for (pos, cp, PL), val in cur.items():
            if cp:
                k2 = (pos, cp - 1, PL)
                n1[k2] = n1.get(k2, 0) + val * cp
            op = openmap[pos]
            for s in op:
                if s not in PL:
                    k2 = (pos, cp, PL | {s})
                    n1[k2] = n1.get(k2, 0) + val
            for ci in range(nc):
                p = pos[ci]
                if p == lens[ci]:
                    continue
                req, bp, lz, tg, en = info[ci][p]
                ok = True
                for c2, p2 in req:
                    if pos[c2] <= p2:
                        ok = False
                        break
                if not ok:
                    continue
                for s, sc in bp:
                    if s in PL:
                        continue
                    for c2, p2 in sc:
                        if pos[c2] > p2:
                            break
                    else:
                        ok = False
                        break
                if not ok:
                    continue
                npl = PL
                if bp and PL:
                    rm = [s for s, _ in bp if s in PL]
                    if rm:
                        npl = PL.difference(rm)
                k = 0
                for sc in lz:
                    for c2, p2 in sc:
                        if pos[c2] > p2:
                            break
                    else:
                        k += 1
                w = val
                if k:
                    f = 1
                    for j in range(1, k + 1):
                        f *= size + j
                    w = val * f
                npos = pos[:ci] + (p + 1,) + pos[ci + 1:]
                ncp = cp
                for pc in tg:
                    for c2, p2 in pc:
                        if npos[c2] <= p2:
                            break
                    else:
                        ncp += 1
                if npos not in openmap:
                    if bp or en:
                        no = set(op)
                        for s, _ in bp:
                            no.discard(s)
                        for s, pc in en:
                            for c2, p2 in pc:
                                if npos[c2] <= p2:
                                    break
                            else:
                                no.add(s)
                        openmap[npos] = frozenset(no)
                    else:
                        openmap[npos] = op
                k2 = (npos, ncp, npl)
                tgt = n1 if k == 0 else buckets.setdefault(size + k + 1, {})
                tgt[k2] = tgt.get(k2, 0) + w
    return 0


# ---------------------------------------------------------------------- recursive count


def _count(P: _Poset, nodes, memo: dict, connected: bool = False) -> int:
    V = len(nodes)
    if V <= 1:
        return 1
    key = None
    if V <= _MEMO_LIMIT:
        key = _key(P, nodes)
        r = memo.get(key)
        if r is not None:
            return r
    comps = [nodes] if connected else _components(P, nodes)
    if len(comps) > 1:
        r = 1
        tot = 0
        for c in comps:
            tot += len(c)
            r *= math.comb(tot, len(c))
            if len(c) > 1:
                r *= _count(P, c, memo, True)
    else:
        segs = _ordinal_pieces(P, nodes)
        if len(segs) > 1:
            r = 1
            for s in segs:
                if len(s) > 1:
                    r *= _count(P, s, memo)
        else:
            r = _dp(P, nodes)
    if key is not None:
        memo[key] = r
    return r


# ---------------------------------------------------------------------- extrapolation


def _affine(vals, n: int, m0: int):
    d = vals[1] - vals[0]
    for a, b in zip(vals[1:], vals[2:]):
        if b - a != d:
            return None
    if d < 0:
        return None
    return vals[0] + (n - m0) * d


def _sym(items, n: int, m0: int, memo: dict):
    """Count at ``n`` from corresponding pieces of ``P_m0 … P_m0+3``; None if unsure."""
    keys = [_key(P, nd) for P, nd in items]
    if all(k == keys[0] for k in keys):
        P, nd = items[0]
        return _count(P, nd, memo)
    comps = [_components(P, nd) for P, nd in items]
    if all(len(c) == 1 for c in comps):
        parts = [_ordinal_pieces(P, nd) for P, nd in items]
        if any(len(p) == 1 for p in parts):
            return None
        par = False
    elif all(len(c) > 1 for c in comps):
        parts = comps
        par = True
    else:
        return None

    per = []
    for (P, _), ch in zip(items, parts):
        d: dict = {}
        for c in ch:
            d.setdefault(_key(P, c), []).append(c)
        per.append(d)
    allkeys: set = set()
    for d in per:
        allkeys.update(d)
    fixed = []
    rem: list[list] = [[] for _ in items]
    for k in allkeys:
        cnts = [len(d.get(k, ())) for d in per]
        mult = _affine(cnts, n, m0) if min(cnts) > 0 else None
        if mult is not None:
            rep = per[0][k][0]
            fixed.append((len(rep), mult, items[0][0], rep))
        else:
            for i, d in enumerate(per):
                rem[i].extend(d.get(k, ()))
    sigmaps = []
    for i, (P, _) in enumerate(items):
        sm: dict = {}
        for c in rem[i]:
            s = frozenset(P.lab[u] for u in c)
            if s in sm:
                return None
            sm[s] = c
        sigmaps.append(sm)
    base = set(sigmaps[0])
    for sm in sigmaps[1:]:
        if set(sm) != base:
            return None

    result = 1
    sizes = []
    for sz, mult, P, c in fixed:
        e = _count(P, c, memo)
        if e != 1:
            result *= pow(e, mult)
        sizes.append((sz, mult))
    for s in sigmaps[0]:
        seq = [(items[i][0], sigmaps[i][s]) for i in range(len(items))]
        sz = _affine([len(c) for _, c in seq], n, m0)
        if sz is None:
            return None
        v = _sym(seq, n, m0, memo)
        if v is None:
            return None
        result *= v
        sizes.append((sz, 1))
    if par:
        result *= _multinomial(sizes)
    return result


def _group_count(setup, g, n: int, labid: dict, memo: dict) -> int:
    m0 = 3 * len(g) + 6
    if n > m0 + 3:
        items = []
        for m in range(m0, m0 + 4):
            P = _build(setup, g, m, labid)
            items.append((P, list(range(len(P.lab)))))
        v = _sym(items, n, m0, memo)
        if v is not None:
            return v
    P = _build(setup, g, n, labid)
    return _count(P, list(range(len(P.lab))), memo)


def _count_loop(setup, n: int) -> int:
    T = len(setup.threads)
    K = setup.sync_points
    Kb = setup.loop_sync_points
    hm = [set() for _ in range(T)]  # plain sync points mentioned
    ha = [set() for _ in range(T)]  # plain sync points with an at-event
    jm = [set() for _ in range(T)]
    ja = [set() for _ in range(T)]
    fixn = [0] * T  # non-at steps in prefix and suffix
    bodyn = [0] * T  # non-at steps in the body
    for t, th in enumerate(setup.threads):
        for steps in (th.prefix, th.suffix):
            for s in steps:
                if s.kind in ("before", "after", "at"):
                    hm[t].add(s.target)
                    if s.kind == "at":
                        ha[t].add(s.target)
                if s.kind != "at":
                    fixn[t] += 1
        for s in th.body:
            if s.kind in ("before", "after", "at"):
                jm[t].add(s.target)
                if s.kind == "at":
                    ja[t].add(s.target)
            if s.kind != "at":
                bodyn[t] += 1

    parent = list(range(T))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for mention in (hm, jm):
        first: dict = {}
        for t in range(T):
            for k in mention[t]:
                if k in first:
                    a, b = find(t), find(first[k])
                    if a != b:
                        parent[a] = b
                else:
                    first[k] = t
    groups: dict = {}
    for t in range(T):
        groups.setdefault(find(t), []).append(t)

    allh: set = set()
    allj: set = set()
    for t in range(T):
        allh |= hm[t]
        allj |= jm[t]
    iso = (K - len(allh)) + (Kb - len(allj)) * n

    labid: dict = {}
    memo: dict = {}
    result = 1
    parts = []
    for g in groups.values():
        g.sort()
        hs: set = set()
        js: set = set()
        for t in g:
            hs |= hm[t]
            js |= jm[t]
        size = sum(fixn[t] + n * bodyn[t] for t in g) + len(hs) + n * len(js)
        if size == 0:
            continue
        if len(g) == 1 and hm[g[0]] <= ha[g[0]] and jm[g[0]] <= ja[g[0]]:
            c = 1  # a single chain
        else:
            c = _group_count(setup, g, n, labid, memo)
        result *= c
        parts.append((size, 1))
    if iso > 0:
        parts.append((1, iso))
    return result * _multinomial(parts)


@register
class DecompositionCounter(LoopCounter):
    name = "opus55_1-s-decomp"
    description = "decompose P_n into components and ordinal pieces, down-set DP on the rest, extrapolate in n"
    capabilities = Capabilities(rcw=False, sync=True, observed_reads=False)

    def count(self, setup, n: int) -> int:
        n = int(n)
        if n < 1:
            raise ValueError("n must be >= 1")
        return _count_loop(setup, n)
