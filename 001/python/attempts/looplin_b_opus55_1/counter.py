"""Counter of |Lin(P_n)| for loop setups without sync points (case b).

Without sync points the trace poset P_n is a disjoint union of chains, one per thread
(its program order), plus one isolated virtual step per sync point (there are none in
case b, but they are handled anyway). Thread t has

    L_t = len(prefix_t) + n * len(body_t) + len(suffix_t)

elements, so |Lin(P_n)| is the multinomial coefficient (sum L_t)! / prod L_t!.

For large totals the multinomial is built from its prime factorisation (exponents by
Legendre's formula), multiplying primes of equal exponent together with a balanced
product before raising to the exponent. This avoids huge divisions.
"""

from __future__ import annotations

import math
from itertools import compress

from harness.capabilities import Capabilities
from harness.loop.api import LoopCounter
from harness.loops import LoopSetup
from harness.registry import register

_SMALL = 1500  # below this total, direct factorial arithmetic is used


class _Prod:
    """Balanced product of many factors of similar size (binary-counter merging)."""

    __slots__ = ("st",)

    def __init__(self) -> None:
        self.st: list[tuple[int, int]] = []

    def push(self, x: int) -> None:
        st = self.st
        c = 1
        while st and st[-1][1] == c:
            v, _ = st.pop()
            x *= v
            c *= 2
        st.append((x, c))

    def value(self) -> int:
        r = 1
        for v, _ in reversed(self.st):  # smallest first
            r *= v
        return r


def _tree_product(xs: list[int]) -> int:
    if not xs:
        return 1
    xs = sorted(xs, key=lambda v: v.bit_length())
    while len(xs) > 1:
        nxt = [xs[i] * xs[i + 1] for i in range(0, len(xs) - 1, 2)]
        if len(xs) % 2:
            nxt.append(xs[-1])
        xs = nxt
    return xs[0]


def _range_product(lo: int, hi: int) -> int:
    """Product of the integers lo..hi (inclusive); 1 if empty."""
    if hi < lo:
        return 1
    if hi - lo < 16:
        r = 1
        for k in range(lo, hi + 1):
            r *= k
        return r
    mid = (lo + hi) // 2
    return _range_product(lo, mid) * _range_product(mid + 1, hi)


def _primes_upto(m: int):
    if m < 2:
        return iter(())
    sieve = bytearray([1]) * (m + 1)
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, math.isqrt(m) + 1):
        if sieve[i]:
            start = i * i
            sieve[start::i] = bytes((m - start) // i + 1)
    return compress(range(m + 1), sieve)


def multinomial(parts: list[int]) -> int:
    """(sum parts)! / prod(part!) for non-negative integer parts."""
    parts = [p for p in parts if p > 0]
    if len(parts) <= 1:
        return 1
    parts.sort()
    total = sum(parts)
    if total <= _SMALL:
        r = math.factorial(total)
        for p in parts:
            r //= math.factorial(p)
        return r
    root = math.isqrt(total)
    tparts = tuple(parts)
    groups: dict[int, _Prod] = {}
    for p in _primes_upto(total):
        if p <= root:
            e = 0
            q = p
            while q <= total:
                s = total // q
                for L in tparts:
                    s -= L // q
                e += s
                q *= p
        else:
            e = total // p
            for L in tparts:
                e -= L // p
        if e:
            g = groups.get(e)
            if g is None:
                g = groups[e] = _Prod()
            g.push(p)
    factors = []
    for e, g in groups.items():
        v = g.value()
        factors.append(v if e == 1 else pow(v, e))
    return _tree_product(factors)


def count_lin(setup: LoopSetup, n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    parts = []
    for th in setup.threads:
        for seg in (th.prefix, th.body, th.suffix):
            for s in seg:
                if s.is_event:
                    raise ValueError("sync events are not supported by this counter (case b)")
        parts.append(len(th.prefix) + n * len(th.body) + len(th.suffix))
    result = multinomial(parts)
    # Unreferenced virtual sync steps are isolated elements; each multiplies the count by
    # the number of positions it can take among the elements already placed.
    isolated = setup.sync_points + n * setup.loop_sync_points
    if isolated:
        t0 = sum(parts)
        result *= _range_product(t0 + 1, t0 + isolated)
    return result


@register
class MultinomialLoopCounter(LoopCounter):
    name = "opus55_1-b-multinomial"
    description = "Exact |Lin(P_n)| as a multinomial of per-thread chain lengths, via prime factorisation"
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)

    def count(self, setup: LoopSetup, n: int) -> int:
        return count_lin(setup, int(n))
