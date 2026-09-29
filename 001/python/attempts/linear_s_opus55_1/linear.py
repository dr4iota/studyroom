"""Linear extensions of the trace poset: an enumerator and an exact counter (case s)."""

from __future__ import annotations

from math import factorial
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

_CAPS = Capabilities(rcw=False, sync=True, observed_reads=False)


@register
class BacktrackEnumerator(LinEnumerator):
    name = "opus55_1-s-backtrack"
    description = "Iterative backtracking over minimal elements (lexicographic by node index)"
    capabilities = _CAPS

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        P = setup.poset
        n = len(P)
        if n == 0:
            yield ()
            return
        succs = [tuple(s) for s in P.succs]
        indeg = [len(p) for p in P.preds]
        avail = set(x for x in range(n) if indeg[x] == 0)
        prefix: list[int] = []
        cands: list[tuple[int, ...]] = [()] * n
        idx = [0] * n
        cands[0] = tuple(sorted(avail))
        d = 0
        last = n - 1
        while True:
            c = cands[d]
            i = idx[d]
            if i == len(c):
                # Exhausted this level: undo the choice made one level up.
                d -= 1
                if d < 0:
                    return
                x = prefix.pop()
                for y in succs[x]:
                    if indeg[y] == 0:
                        avail.discard(y)
                    indeg[y] += 1
                avail.add(x)
                idx[d] += 1
                continue
            x = c[i]
            if d == last:
                prefix.append(x)
                yield tuple(prefix)
                prefix.pop()
                idx[d] = i + 1
                continue
            # Apply x.
            avail.discard(x)
            prefix.append(x)
            for y in succs[x]:
                k = indeg[y] - 1
                indeg[y] = k
                if k == 0:
                    avail.add(y)
            d += 1
            cands[d] = tuple(sorted(avail))
            idx[d] = 0


@register
class DecompositionCounter(LinCounter):
    name = "opus55_1-s-decomp"
    description = "Exact |Lin(P)| via component/cut-node decomposition and downset DP"
    capabilities = _CAPS

    def count(self, setup: Setup) -> CountResult:
        P = setup.poset
        n = len(P)
        if n == 0:
            return CountResult(linearizations=1, method="decomposition")
        topo = P.topological_order()
        desc = [0] * n
        anc = [0] * n
        for x in reversed(topo):
            m = 0
            for y in P.succs[x]:
                m |= (1 << y) | desc[y]
            desc[x] = m
        for x in topo:
            m = 0
            for y in P.preds[x]:
                m |= (1 << y) | anc[y]
            anc[x] = m
        comp = [anc[x] | desc[x] | (1 << x) for x in range(n)]
        # Position in a topological order, to sort cut nodes.
        tpos = [0] * n
        for i, x in enumerate(topo):
            tpos[x] = i

        def bits(S: int) -> list[int]:
            out = []
            while S:
                low = S & -S
                out.append(low.bit_length() - 1)
                S ^= low
            return out

        def count_set(S: int) -> int:
            nodes = bits(S)
            size = len(nodes)
            if size <= 1:
                return 1
            # Connected components of the comparability graph restricted to S.
            comps = []
            rest = S
            while rest:
                low = rest & -rest
                seen = low
                frontier = low
                while frontier:
                    nf = 0
                    for x in bits(frontier):
                        nf |= comp[x] & S
                    nf &= ~seen
                    seen |= nf
                    frontier = nf
                comps.append(seen)
                rest &= ~seen
            if len(comps) > 1:
                total = factorial(size)
                for C in comps:
                    k = bin(C).count("1")
                    total = total // factorial(k) * count_set(C)
                return total
            # Connected: split at cut nodes (comparable to every node of S).
            cuts = [x for x in nodes if comp[x] & S == S]
            if cuts:
                cuts.sort(key=lambda x: tpos[x])
                total = 1
                prev = None
                for c in cuts:
                    seg = S & anc[c]
                    if prev is not None:
                        seg &= desc[prev]
                    if seg:
                        total *= count_set(seg)
                    prev = c
                seg = S & desc[prev]
                if seg:
                    total *= count_set(seg)
                return total
            return downset_dp(S, nodes)

        def downset_dp(S: int, nodes: list[int]) -> int:
            pm = [(x, 1 << x, anc[x] & S) for x in nodes]
            cur = {0: 1}
            for _ in range(len(nodes)):
                nxt: dict[int, int] = {}
                get = nxt.get
                for mask, c in cur.items():
                    for x, bx, px in pm:
                        if not (mask & bx) and (px & ~mask) == 0:
                            m2 = mask | bx
                            nxt[m2] = get(m2, 0) + c
                cur = nxt
            return cur.get(S, 0)

        full = (1 << n) - 1
        return CountResult(linearizations=count_set(full), method="decomposition")
