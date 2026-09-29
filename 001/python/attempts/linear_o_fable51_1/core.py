"""Core of the case-``o`` linearizer (spec v1: ``K = 0``, observed reads allowed).

With no sync points the trace poset is a disjoint union of chains, one per thread, so
``Lin(P)`` is the set of interleavings of the chains.  Observed reads restrict this to
``LinFeas(P)``.

Feasibility of a linearization ``L`` (spec §5)
----------------------------------------------
A full schedule ``(L, pi)`` only matters through the order ``sigma`` in which actions
take effect.  ``sigma`` is realisable by some ``pi`` iff it extends the *interval order*
of ``L`` (``a`` before ``b`` whenever ``end(a)`` precedes ``start(b)`` in ``L``); the
greedy assignment ``pi(a_i) = max(start(a_i), pi(a_{i-1}) + eps)`` shows this.

Such a ``sigma`` can be produced by walking ``L`` from left to right: at each ``done(a)``
node, if ``a`` has not taken effect yet, take an ordered subset of the pending
(started, not yet effected) actions, let them take effect, then let ``a`` take effect.
Effects never need to happen anywhere else (postponing an effect to just before the next
``done`` node never changes ``sigma``).  So a linearization is feasible iff this walk
can be completed without an observed read ever returning the wrong term.

The walk is turned into a state machine.  A *state* is
``(pending bitmask, block contents, referenced read values)``; every prefix of ``L``
is mapped to the set of states reachable by some choice of effects.  The prefix is dead
when that set is empty.  Actions that can never influence an observed read are left
out of the state entirely (their effect points are free).

Enumeration is a depth-first search over interleavings that carries the state set along
and prunes dead prefixes.  Counting is the same search with memoisation on
``(position in each chain, state set)``.
"""

from __future__ import annotations

import sys
from math import factorial
from typing import Iterator

from harness import terms as T
from harness.model import Setup

Lin = tuple[int, ...]

State = tuple  # (pending: int, mem: tuple[Term, ...], vals: tuple[Term | None, ...])


# --------------------------------------------------------------------------- plain chains


def thread_chains(setup: Setup) -> list[list[int]]:
    """The non-empty chains of the poset: the program order of each thread's nodes."""
    return [list(c) for c in setup.poset.chains if c]


def has_observations(setup: Setup) -> bool:
    return any(a.observed is not None for a in setup.actions.values())


def count_interleavings(chains: list[list[int]]) -> int:
    """``|Lin(P)|`` for a disjoint union of chains: a multinomial coefficient."""
    n = sum(len(c) for c in chains)
    r = factorial(n)
    for c in chains:
        r //= factorial(len(c))
    return r


def interleavings(chains: list[list[int]]) -> Iterator[Lin]:
    """Every interleaving of the chains, lexicographic in the sequence of chain indices.

    The sequence of chain indices is a multiset permutation; it is advanced with the
    classic next-permutation step (find the last ascent, swap, reverse the suffix), which
    works unchanged for multisets when the comparisons are strict as below.
    """
    N = len(chains)
    lens = [len(c) for c in chains]
    n = sum(lens)
    if n == 0:
        yield ()
        return
    seq = [t for t in range(N) for _ in range(lens[t])]
    while True:
        ptr = [0] * N
        out: list[int] = []
        app = out.append
        for t in seq:
            k = ptr[t]
            app(chains[t][k])
            ptr[t] = k + 1
        yield tuple(out)
        k = n - 2
        while k >= 0 and seq[k] >= seq[k + 1]:
            k -= 1
        if k < 0:
            return
        l = n - 1
        while seq[l] <= seq[k]:
            l -= 1
        seq[k], seq[l] = seq[l], seq[k]
        seq[k + 1:] = seq[:k:-1]


# --------------------------------------------------------------------------- the state machine


class Model:
    """Static data of a setup plus the state transitions of the feasibility walk."""

    def __init__(self, setup: Setup) -> None:
        poset = setup.poset
        acts = list(setup.actions.values())
        self.acts = acts
        A = len(acts)
        aidx = {a.id: i for i, a in enumerate(acts)}
        self.aidx = aidx
        self.n = len(poset)
        self.chains = thread_chains(setup)
        self.node_action = [aidx[poset.action[x]] for x in range(self.n)]
        self.node_is_start = [poset.kind[x] == "start" for x in range(self.n)]
        self.is_write = [a.kind != "read" for a in acts]

        # tr[w]: the reads whose values the content of write w depends on, following
        # references through earlier writes of the same thread.
        tr: dict[int, frozenset[int]] = {}

        def tr_reads(i: int) -> frozenset[int]:
            got = tr.get(i)
            if got is not None:
                return got
            out: set[int] = set()
            a = acts[i]
            if a.data is not None:
                for rid in T.refs(a.data):
                    j = aidx[rid]
                    if acts[j].kind == "read":
                        out.add(j)
                    else:
                        out |= tr_reads(j)
            got = frozenset(out)
            tr[i] = got
            return got

        self.tr = [tr_reads(i) if self.is_write[i] else frozenset() for i in range(A)]
        self.tr_list = [sorted(s) for s in self.tr]
        # Content of a write that depends on no read; None when it does depend on one.
        self.static = [
            setup.static_content(a.id) if self.is_write[i] and not self.tr[i] else None
            for i, a in enumerate(acts)
        ]

        # Relevance: observed reads; writes to a block with a relevant read; reads those
        # writes depend on; and so on to a fixpoint.  Everything else is ignored.
        observed = [i for i, a in enumerate(acts) if a.kind == "read" and a.observed is not None]
        rel_reads: set[int] = set(observed)
        rel_writes: set[int] = set()
        changed = True
        while changed:
            changed = False
            blocks = {acts[r].block for r in rel_reads}
            for i in range(A):
                if self.is_write[i] and i not in rel_writes and acts[i].block in blocks:
                    rel_writes.add(i)
                    changed = True
                    for r in self.tr[i]:
                        if r not in rel_reads:
                            rel_reads.add(r)
                            changed = True
        self.relevant = [i in rel_reads or i in rel_writes for i in range(A)]

        rel_blocks = sorted({acts[i].block for i in rel_reads})  # covers every relevant write too
        bidx = {b: k for k, b in enumerate(rel_blocks)}
        self.abidx = [bidx.get(a.block, -1) for a in acts]
        self.init_mem = tuple(setup.init[b] for b in rel_blocks)

        ref_reads = sorted({r for w in rel_writes for r in self.tr[w]})
        self.vidx: dict[int, int] = {r: k for k, r in enumerate(ref_reads)}
        self.nvals = len(ref_reads)
        # needed_mask[r]: relevant writes whose content depends on read r.  Once all of
        # them took effect the value of r is dropped from the state.
        self.needed_mask: dict[int, int] = {r: 0 for r in ref_reads}
        for w in rel_writes:
            for r in self.tr[w]:
                self.needed_mask[r] |= 1 << w

        self.obs_term = [a.observed if a.kind == "read" else None for a in acts]
        # For each observed read r: (r, block slot, observed term, mask of writes that
        # could still be the writer r sees and could carry the observed term).
        info = []
        for r in observed:
            a = acts[r]
            wm = 0
            for w in rel_writes:
                b = acts[w]
                if b.block != a.block:
                    continue
                if b.thread == a.thread and b.start > a.done:
                    continue  # starts after r ends in program order: can never precede r
                if self.static[w] is not None and self.static[w] != a.observed:
                    continue
                wm |= 1 << w
            info.append((r, bidx[a.block], a.observed, wm))
        self.obs_info = info

    # ------------------------------------------------------------------ states

    def initial_state(self) -> State | None:
        st: State = (0, self.init_mem, (None,) * self.nvals)
        return st if self.alive(st, 0) else None

    def content(self, w: int, vals: tuple) -> T.Term:
        """Content of write ``w`` given the values of the reads it depends on."""
        s = self.static[w]
        if s is not None:
            return s
        aidx = self.aidx
        is_write = self.is_write
        vidx = self.vidx

        def look(rid: str) -> T.Term:
            j = aidx[rid]
            if is_write[j]:
                return self.content(j, vals)
            return vals[vidx[j]]

        return T.substitute(self.acts[w].data, look)

    def effect(self, st: State, x: int, started: int) -> State | None:
        """State after action ``x`` takes effect; None if an observation is violated."""
        pending, mem, vals = st
        pending2 = pending & ~(1 << x)
        bi = self.abidx[x]
        if self.is_write[x]:
            c = self.content(x, vals)
            mem2 = mem[:bi] + (c,) + mem[bi + 1:]
            trl = self.tr_list[x]
            if trl:
                effected = started & ~pending2
                vl = list(vals)
                for r in trl:
                    if not (self.needed_mask[r] & ~effected):
                        vl[self.vidx[r]] = None
                vals = tuple(vl)
            return (pending2, mem2, vals)
        v = mem[bi]
        obs = self.obs_term[x]
        if obs is not None and v != obs:
            return None
        vi = self.vidx.get(x)
        if vi is not None:
            vals = vals[:vi] + (v,) + vals[vi + 1:]
        return (pending2, mem, vals)

    def alive(self, st: State, started: int) -> bool:
        """Necessary condition: every observed read that has not taken effect can still
        find its term (already in its block, or from a write that has not taken effect,
        can precede it, and may carry the term)."""
        pending, mem, _ = st
        effected = started & ~pending
        for r, bi, t, wm in self.obs_info:
            if (effected >> r) & 1:
                continue
            if mem[bi] == t:
                continue
            if not (wm & ~effected):
                return False
        return True

    def _expand(self, st: State, x: int, started: int, out: set) -> None:
        """All states reachable from ``st`` by letting some pending actions take effect,
        in some order, and then ``x``."""
        seen = {st}
        stack = [st]
        effect = self.effect
        alive = self.alive
        xbit = 1 << x
        while stack:
            s = stack.pop()
            ns = effect(s, x, started)
            if ns is not None and alive(ns, started):
                out.add(ns)
            others = s[0] & ~xbit
            while others:
                b = others & -others
                others ^= b
                ns = effect(s, b.bit_length() - 1, started)
                if ns is not None and ns not in seen and alive(ns, started):
                    seen.add(ns)
                    stack.append(ns)

    def step(self, states: frozenset, node: int, started: int) -> frozenset:
        """State set after appending ``node`` to the prefix.

        ``started`` is the mask of relevant actions started in the new prefix (so it
        already includes ``node``'s action when ``node`` is a start).
        """
        x = self.node_action[node]
        if not self.relevant[x]:
            return states
        bit = 1 << x
        if self.node_is_start[node]:
            return frozenset((p | bit, m, v) for p, m, v in states)
        out: set = set()
        for st in states:
            if st[0] & bit:
                self._expand(st, x, started, out)
            else:
                out.add(st)  # already took effect earlier
        return frozenset(out)

    def start_bit(self, node: int) -> int:
        x = self.node_action[node]
        if self.relevant[x] and self.node_is_start[node]:
            return 1 << x
        return 0


# --------------------------------------------------------------------------- enumeration


_DEAD_CAP = 1 << 16  # bound on remembered dead (chain positions, state set) pairs


def feasible_linearizations(m: Model) -> Iterator[Lin]:
    """Every feasible linearization, lexicographic in the sequence of chain indices."""
    init = m.initial_state()
    if init is None:
        return
    n = m.n
    if n == 0:
        yield ()
        return
    chains = m.chains
    N = len(chains)
    lens = [len(c) for c in chains]
    step = m.step
    start_bit = m.start_bit

    seq = [0] * n  # node placed at each level
    seq_t = [0] * n  # chain of the node placed at each level
    ptr = [0] * N  # next position in each chain
    states: list = [None] * (n + 1)
    states[0] = frozenset([init])
    started = [0] * (n + 1)
    cands: list = [None] * (n + 1)
    ci = [0] * (n + 1)
    found = [False] * (n + 1)  # did level d yield anything below it
    dead: set = set()  # (ptr tuple, state set) pairs with no feasible completion

    d = 0
    cands[0] = list(range(N))
    while True:
        if d == n:
            yield tuple(seq)
            found[n - 1] = True
            d = n - 1
            ptr[seq_t[d]] -= 1
            continue
        i = ci[d]
        if i == len(cands[d]):
            if d == 0:
                return
            if found[d]:
                found[d - 1] = True
            elif len(dead) < _DEAD_CAP:
                dead.add((tuple(ptr), states[d]))
            d -= 1
            ptr[seq_t[d]] -= 1
            continue
        ci[d] = i + 1
        t = cands[d][i]
        node = chains[t][ptr[t]]
        st2 = started[d] | start_bit(node)
        ns = step(states[d], node, st2)
        if not ns:
            continue
        ptr[t] += 1
        if dead and (tuple(ptr), ns) in dead:
            ptr[t] -= 1
            continue
        seq[d] = node
        seq_t[d] = t
        d += 1
        states[d] = ns
        started[d] = st2
        cands[d] = [u for u in range(N) if ptr[u] < lens[u]]
        ci[d] = 0
        found[d] = False


# --------------------------------------------------------------------------- counting


def count_feasible(m: Model) -> int:
    """``|LinFeas(P)|`` by the same walk, memoised on (chain positions, state set)."""
    init = m.initial_state()
    if init is None:
        return 0
    chains = m.chains
    N = len(chains)
    full = tuple(len(c) for c in chains)
    if m.n == 0:
        return 1
    step = m.step
    start_bit = m.start_bit
    memo: dict = {}
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * m.n + 1000))

    def rec(ptr: tuple, states: frozenset, started: int) -> int:
        if ptr == full:
            return 1
        key = (ptr, states)
        v = memo.get(key)
        if v is not None:
            return v
        total = 0
        for t in range(N):
            k = ptr[t]
            if k < full[t]:
                node = chains[t][k]
                st2 = started | start_bit(node)
                ns = step(states, node, st2)
                if ns:
                    total += rec(ptr[:t] + (k + 1,) + ptr[t + 1:], ns, st2)
        memo[key] = total
        return total

    return rec((0,) * N, frozenset([init]), 0)
