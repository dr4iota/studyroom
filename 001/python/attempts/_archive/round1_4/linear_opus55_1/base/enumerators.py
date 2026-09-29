"""Linearization enumerators for the base problem (Read/Write only, ``K = 0``).

Without sync the trace poset is a disjoint union of the thread chains, so ``Lin(P)`` is
the set of interleavings of those chains. An interleaving is determined by its *thread
word*: the sequence of thread labels, a permutation of the multiset
``{0^{n_0}, 1^{n_1}, ...}`` (the ``j``-th occurrence of label ``t`` is node
``thread_chains[t][j]``). Every algorithm below enumerates multiset permutations in
some way and maintains the node array alongside the word.

All algorithms emit a fresh ``tuple`` per output, which alone costs ``O(n)`` (in C).
The "time per output" quoted in each docstring is the cost of *moving from one
linearization to the next* (the combinatorial work), excluding that copy.

Algorithms (all registered with the ``opus-`` prefix):

``opus55-b-lex``       iterative lexicographic successor of the thread word (Knuth 7.2.1.2 L)
``opus55-b-coollex``   Williams' loopless cool-lex order (prefix shifts, O(1) variables)
``opus55-b-vr``        Varol–Rotem iterative scheme (Knuth 7.2.1.2 V) specialised to chains
``opus55-b-neargray``  new recursive near-Gray code: consecutive outputs differ by ONE OR TWO
                   adjacent transpositions (one element moves by 1 or 2 positions)
``opus55-b-multinomial`` (counter) closed form ``n! / prod n_t!``

Why no ``gray_code = True``: the adjacent-transposition graph on multiset permutations
is bipartite (parity of the inversion count), and a Hamilton path needs the two colour
classes to differ in size by at most one. Already for two chains of length 2 there are 4
even and 2 odd words (0011, 0110, 1001, 1100 vs. 0101, 1010), so no enumeration in which
every consecutive pair differs by exactly one adjacent transposition exists in general.
One or two adjacent transpositions is the best possible uniform guarantee (as in
Pruesse–Ruskey), and that is what ``opus55-b-neargray`` provides.
"""

from __future__ import annotations

from math import factorial
from typing import Iterator

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.model import Setup
from harness.poset import Linearization
from harness.registry import register

BASE = Capabilities(rcw=False, sync=False, observed_reads=False)


def _chains(setup: Setup) -> list[list[int]]:
    """Non-empty thread chains; refuses posets that are not a disjoint union of chains."""
    P = setup.poset
    if P.sync_nodes:
        raise ValueError("opus enumerators handle the base problem only (K = 0)")
    chains = [list(c) for c in P.thread_chains if c]
    if sum(len(c) for c in chains) != len(P) or sum(len(p) for p in P.preds) != len(P) - len(chains):
        raise ValueError("opus enumerators need a disjoint union of chains (no sync edges)")
    return chains


# --------------------------------------------------------------------------------------
# 1. Lexicographic order (iterative)
# --------------------------------------------------------------------------------------


def lex(chains: list[list[int]]) -> Iterator[Linearization]:
    """Thread words in lexicographic order, via the multiset next-permutation step.

    Step: find the last ascent ``w[j] < w[j+1]``, swap ``w[j]`` with the last larger
    letter, reverse the suffix; then rebuild the node array on the suffix only (the
    nodes of label ``t`` in a suffix are the last ``#t`` nodes of chain ``t``).
    Time: ``O(r)`` for a suffix of length ``r``; measured amortized ``O(1)``
    per output (the changed window averages about 3 positions on 2-6 chains). Memory ``O(n)``. Non-recursive.
    """
    w = [t for t, c in enumerate(chains) for _ in c]
    arr = [x for c in chains for x in c]
    n = len(w)
    lens = [len(c) for c in chains]
    yield tuple(arr)
    cnt = [0] * len(chains)
    while True:
        j = n - 2
        while j >= 0 and w[j] >= w[j + 1]:
            j -= 1
        if j < 0:
            return
        k = n - 1
        wj = w[j]
        while w[k] <= wj:
            k -= 1
        w[j], w[k] = w[k], wj
        w[j + 1 :] = w[: j : -1]
        for i in range(j, n):
            cnt[w[i]] += 1
        for i in range(j, n):
            t = w[i]
            arr[i] = chains[t][lens[t] - cnt[t]]
            cnt[t] -= 1
        yield tuple(arr)


# --------------------------------------------------------------------------------------
# 2. Cool-lex (loopless prefix shifts)
# --------------------------------------------------------------------------------------


def coollex(chains: list[list[int]]) -> Iterator[Linearization]:
    """Williams' cool-lex order of multiset permutations (SODA 2009), loopless.

    The thread word is a singly linked list; each step is a *prefix shift* (one letter
    moves to the front) found with O(1) pointer operations and a constant number of
    variables: loopless, ``O(1)`` worst case per word. The node array follows the
    shift: ``arr[0:k+1] = [head of chain t] + (arr[0:k] with each node of chain t
    replaced by its chain successor)``, done with a precomputed per-thread map at C
    speed but ``O(k)`` element moves (measured: the changed window averages 3-4
    positions). Memory ``O(N n)`` for the maps, ``O(n)`` otherwise.
    Letters are ordered by decreasing thread label (the algorithm starts from the
    non-increasing word).
    """
    n = sum(len(c) for c in chains)
    T = len(chains)
    # Word letters: value v = thread label; start list in non-increasing order.
    vals = [t for t in range(T - 1, -1, -1) for _ in chains[t]]
    arr = [x for t in range(T - 1, -1, -1) for x in chains[t]]
    yield tuple(arr)
    if n < 2:
        return
    shift = []
    for t in range(T):
        m = list(range(max(arr) + 1))
        for a, b in zip(chains[t], chains[t][1:]):
            m[a] = b
        shift.append(m.__getitem__)
    heads = [c[0] for c in chains]
    nxt = list(range(1, n)) + [-1]  # node ids 0..n-1 of the linked word
    v = vals
    h, i, j = 0, n - 2, n - 1
    ipos = n - 2  # position of i in the word
    while nxt[j] != -1 or v[j] < v[h]:
        if nxt[j] != -1 and v[i] >= v[nxt[j]]:
            s, spos = j, ipos + 1
        else:
            s, spos = i, ipos
        t = nxt[s]
        nxt[s] = nxt[t]
        nxt[t] = h
        if v[t] < v[h]:
            i, ipos = t, 0
        else:
            ipos += 1
        j = nxt[i]
        h = t
        k = spos + 1  # t moved from position k to the front
        lab = v[t]
        arr[0 : k + 1] = [heads[lab], *map(shift[lab], arr[0:k])]
        yield tuple(arr)


# --------------------------------------------------------------------------------------
# 3. Varol–Rotem (Knuth's Algorithm V), specialised to chains
# --------------------------------------------------------------------------------------


def varol_rotem(chains: list[list[int]]) -> Iterator[Linearization]:
    """Varol–Rotem: elements are moved left one step at a time, or rotated home.

    Elements are ranked 1..n in the initial extension (chains concatenated). The
    largest-rank element ``k`` that can move left past its left neighbour does so
    (one adjacent transposition); elements that are blocked (by a predecessor, which
    for chains means the same thread) are rotated back to their home position.
    Non-recursive. ``O(n)`` worst case per output (a rotation); measured amortized
    ``O(1)`` (the changed window averages about 3 positions). Memory ``O(n)``. Most steps are single adjacent transpositions, but
    not all, so this is not a Gray code.
    """
    order = [x for c in chains for x in c]
    n = len(order)
    thr = [0] * (n + 1)  # thread of rank r; rank 0 is a sentinel preceding everything
    thr[0] = -1
    r = 1
    for t, c in enumerate(chains):
        for _ in c:
            thr[r] = t
            r += 1
    a = list(range(n + 1))  # a[pos] = rank at position pos
    ai = list(range(n + 1))  # inverse
    node = [0] + order
    out = order[:]  # out[pos-1] = node at pos
    yield tuple(out)
    while True:
        k = n
        while k > 0:
            j = ai[k]
            l = a[j - 1]
            if l != 0 and thr[l] != thr[k]:
                a[j - 1], a[j] = k, l
                ai[k], ai[l] = j - 1, j
                out[j - 2], out[j - 1] = out[j - 1], out[j - 2]
                yield tuple(out)
                break
            # rotate k back from position j to its home position k
            if j < k:
                a[j:k] = a[j + 1 : k + 1]
                for p in range(j, k):
                    ai[a[p]] = p
                out[j - 1 : k - 1] = out[j:k]
                a[k] = ai[k] = k
                out[k - 1] = node[k]
            k -= 1
        else:
            return


# --------------------------------------------------------------------------------------
# 4. Near-Gray code (one or two adjacent transpositions), CAT
# --------------------------------------------------------------------------------------
#
# Moves on the node array, relative to an offset p:
#   0: swap p, p+1                  [x, y]    -> [y, x]
#   1: rotate left  p..p+2          [x, y, z] -> [y, z, x]   (x jumps right by two)
#   2: rotate right p..p+2          [x, y, z] -> [z, x, y]   (z jumps left by two)
_INV = (0, 2, 1)


def _comb_moves(m: int, c: int, rev: bool) -> Iterator[tuple[int, int]]:
    """Moves of the path H(m, c, c): from 1^c 0^m to 0^m 1^c (reversed if ``rev``).

    H(m, c, a) is a Hamilton path, in the graph "a letter moves by 1 or 2 positions",
    on the binary words with m zeros and c ones, from 1^a 0^m 1^(c-a) to 0^m 1^c
    (1 <= a <= c). Split on the first letter:

        a >= 2:        1.H(m, c-1, a-1)      swap(0,1)   0.H(m-1, c, 1)
        a = 1, c = 1:  1 0^m                 swap(0,1)   0.H(m-1, 1, 1)
        a = 1, c >= 2: 1.rev H(m, c-1, 1)    rotR(0)     0.H(m-1, c, 2)

    (the rotR turns 1 1 0^m 1^(c-2) into 0 1 1 0^(m-1) 1^(c-2)). Base: m = 0 or c = 0
    is a single word. Iterative with an explicit task stack: every expanded task emits
    one move and has at most two sub-tasks, so the cost is O(1) amortized per move and
    the stack holds O(m + c) tasks.
    """
    stack: list[tuple] = [(1, 0, m, c, c, rev)]
    pop, push = stack.pop, stack.append
    while stack:
        task = pop()
        if task[0] == 0:
            yield task[1], task[2]
            continue
        _, off, m_, c_, a, r = task
        if m_ == 0 or c_ == 0:
            continue
        if a >= 2:
            first = (1, off + 1, m_, c_ - 1, a - 1, r)
            mv = 0
            second = (1, off + 1, m_ - 1, c_, 1, r)
        elif c_ == 1:
            first = None
            mv = 0
            second = (1, off + 1, m_ - 1, 1, 1, r)
        else:
            first = (1, off + 1, m_, c_ - 1, 1, not r)
            mv = 2
            second = (1, off + 1, m_ - 1, c_, 2, r)
        if r:  # reversed: rev(second), inverse move, rev(first)
            first, second, mv = second, first, _INV[mv]
        if second is not None:
            push(second)
        push((0, mv, off))
        if first is not None:
            push(first)


def _word_moves(lens: list[int]) -> Iterator[tuple[int, int]]:
    """Moves of the near-Gray sequence of all words over labels 0..len(lens)-1.

    Level k interleaves thread k (c = lens[k] ones) into the level k-1 word (m zeros),
    SJT style: for each level-(k-1) word, sweep the combination path, alternately
    forward (1^c 0^m -> 0^m 1^c) and backward. Both endpoints keep the level-(k-1)
    letters contiguous, so a level-(k-1) move (<= 2 adjacent transpositions in its own
    word) is still one in the level-k word, shifted by 0 or c.
    """
    K = len(lens)
    if K <= 1:
        return
    m = sum(lens[:-1])
    c = lens[-1]
    inner = _word_moves(lens[:-1])
    rev = False
    while True:
        yield from _comb_moves(m, c, rev)
        shift = c if rev else 0
        mv = next(inner, None)
        if mv is None:
            return
        yield mv[0], mv[1] + shift
        rev = not rev


def near_gray(chains: list[list[int]]) -> Iterator[Linearization]:
    """Near-Gray enumeration: consecutive outputs differ by one or two adjacent transpositions.

    Every step moves one node by one or two positions (a swap, or a 3-rotation which is
    two adjacent transpositions). Word order: thread labels are nested SJT-style, the
    last thread changing fastest (see :func:`_word_moves` and :func:`_comb_moves`).
    Time: O(1) amortized per output for the moves (CAT: each level's sweep has at
    least one move, so carries to lower levels are geometric), plus O(N) generator
    delegation. Memory O(n + N).
    """
    lens = [len(c) for c in chains]
    arr = [x for t in range(len(chains) - 1, -1, -1) for x in chains[t]]
    # initial word: the last thread first, then the previous ones (1^c 0^m at every level)
    yield tuple(arr)
    for kind, p in _word_moves(lens):
        if kind == 0:
            arr[p], arr[p + 1] = arr[p + 1], arr[p]
        elif kind == 1:
            arr[p], arr[p + 1], arr[p + 2] = arr[p + 1], arr[p + 2], arr[p]
        else:
            arr[p], arr[p + 1], arr[p + 2] = arr[p + 2], arr[p], arr[p + 1]
        yield tuple(arr)


# --------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------


@register
class OpusLex(LinEnumerator):
    name = "opus55-b-lex"
    description = "lexicographic thread words, iterative next-permutation (base only)"
    capabilities = BASE

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return lex(_chains(setup))


@register
class OpusCoolLex(LinEnumerator):
    name = "opus55-b-coollex"
    description = "Williams' loopless cool-lex prefix shifts (base only)"
    capabilities = BASE

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return coollex(_chains(setup))


@register
class OpusVarolRotem(LinEnumerator):
    name = "opus55-b-vr"
    description = "Varol-Rotem iterative left moves / rotations (base only)"
    capabilities = BASE

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return varol_rotem(_chains(setup))


@register
class OpusNearGray(LinEnumerator):
    name = "opus55-b-neargray"
    description = "CAT near-Gray code: 1 or 2 adjacent transpositions per step (base only)"
    capabilities = BASE
    gray_code = False  # exactly-one-transposition Gray codes do not exist in general

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return near_gray(_chains(setup))


@register
class OpusMultinomial(LinCounter):
    name = "opus55-b-multinomial"
    description = "closed form n! / prod(n_t!) for the base problem"
    capabilities = BASE

    def count(self, setup: Setup) -> CountResult:
        chains = _chains(setup)
        r = factorial(sum(len(c) for c in chains))
        for c in chains:
            r //= factorial(len(c))
        return CountResult(r, None, "multinomial")
