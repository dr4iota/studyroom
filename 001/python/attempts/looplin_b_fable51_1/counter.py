"""Counter of ``|Lin(P_n)|`` for loop setups without sync points (task ``looplin``, case ``b``).

Without sync points the trace poset has no edge between two threads: the order is
exactly program order within each thread.  ``P_n`` is therefore a disjoint union of
chains, one per thread, and a linearization is an interleaving of those chains.  With
chain lengths ``L_1, ..., L_N`` (every start and every done step of the prefix, the
``n`` body copies and the suffix) the number of interleavings is the multinomial

    T! / (L_1! * ... * L_N!),        T = L_1 + ... + L_N.

Write data never adds an edge (a reference always points at an earlier step of the same
thread), so data is irrelevant to the count.  A declared sync point that no event
mentions is one more isolated node (spec §2) and counts as a chain of length 1.

The multinomial is computed exactly, without dividing big integers:

* its exponent at a prime ``p`` is ``v_p(T!) - sum v_p(L_t!)``, by Legendre's formula;
* the factors ``p**e`` are multiplied with a balanced product tree.

Two regimes keep the work proportional to the size of the answer rather than to ``T``:

* **sieve** (``T`` not much larger than ``S = T - max L_t``): primes up to ``T``;
* **stripping** (``T >> S``, e.g. only one thread has a body and ``n`` is huge): primes
  up to ``S`` only.  The ratio ``T!/max(L)!`` is the product of the ``S`` consecutive
  integers in ``(max L, T]``; every prime ``<= S`` is divided out of them (its net
  exponent comes from Legendre's formula), what remains is coprime to the denominator
  and is multiplied in as is.
"""

from __future__ import annotations

from bisect import bisect_right
from itertools import compress
from math import isqrt

from harness.capabilities import Capabilities
from harness.loop.api import LoopCounter
from harness.loops import LoopSetup
from harness.registry import register

# Largest total for which primes up to T are sieved (memory: one byte per number).
SIEVE_CAP = 100_000_000
# Largest S = T - max(L) accepted by the stripping regime (memory: one int per number).
MAX_SMALL = 8_000_000
# Prefer the sieve regime while T <= RATIO * S.
RATIO = 10


# ----------------------------------------------------------------------------- arithmetic


def _primes_upto(n: int) -> list[int]:
    """All primes ``<= n``, ascending (sieve of Eratosthenes on a bytearray)."""
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytes(len(range(i * i, n + 1, i)))
    return list(compress(range(n + 1), sieve))


def _vp_factorial(x: int, p: int) -> int:
    """Exponent of the prime ``p`` in ``x!`` (Legendre: sum of floor(x / p^k))."""
    e = 0
    while x:
        x //= p
        e += x
    return e


def _product(factors: list[int]) -> int:
    """Product of a list of integers by pairwise (balanced) multiplication."""
    if not factors:
        return 1
    while len(factors) > 1:
        nxt = [factors[i] * factors[i + 1] for i in range(0, len(factors) - 1, 2)]
        if len(factors) & 1:
            nxt.append(factors[-1])
        factors = nxt
    return factors[0]


def _multinomial_by_sieve(total: int, parts: list[int]) -> int:
    """``total! / prod(L! for L in parts)`` from the exponents of all primes ``<= total``.

    ``parts`` are positive and sum to at most ``total``.
    """
    primes = _primes_upto(total)
    desc = sorted(parts, reverse=True)
    root = isqrt(total)
    factors: list[int] = []

    # Primes p <= sqrt(total): full Legendre sums.
    i = 0
    while i < len(primes) and primes[i] <= root:
        p = primes[i]
        i += 1
        e = _vp_factorial(total, p)
        for L in desc:
            if L < p:
                break
            e -= _vp_factorial(L, p)
        if e > 0:
            factors.append(p**e)

    # Primes p > sqrt(total): v_p(x!) = x // p, and L // p = 0 once p > L.  Walk the
    # prime ranges (desc[k], desc[k-1]] where exactly the k largest parts matter.
    bounds = [total] + desc + [0]
    for k in range(len(desc) + 1):
        hi = bounds[k]
        lo = max(bounds[k + 1], root)
        if hi <= lo:
            continue
        a = bisect_right(primes, lo)
        b = bisect_right(primes, hi)
        if k == 0:
            # No part reaches p: e = total // p, which is 1 for p > total // 2.
            c = bisect_right(primes, max(lo, total // 2))
            for p in primes[a:c]:
                factors.append(p ** (total // p))
            factors.extend(primes[c:b])
        else:
            sub = desc[:k]
            for p in primes[a:b]:
                e = total // p
                for L in sub:
                    e -= L // p
                if e > 0:
                    factors.append(p if e == 1 else p**e)
    return _product(factors)


def _multinomial_by_stripping(total: int, largest: int, rest: list[int]) -> int:
    """``total! / (largest! * prod(L! for L in rest))`` using primes ``<= total - largest``.

    Every ``L`` in ``rest`` is at most ``S = total - largest`` (they sum to ``S``), so the
    denominator ``prod L!`` only has primes ``<= S``.  The quotient ``total!/largest!`` is
    the product of the ``S`` integers in ``(largest, total]``.  For each prime ``p <= S``
    the net exponent is found by Legendre's formula and ``p`` is divided out of those
    integers; the leftovers have only prime factors ``> S`` and enter the product as is.
    """
    small = total - largest
    base = largest + 1
    xs = list(range(base, total + 1))  # the S consecutive integers
    desc = sorted(rest, reverse=True)
    factors: list[int] = []
    for p in _primes_upto(small):
        e = _vp_factorial(total, p) - _vp_factorial(largest, p)
        for L in desc:
            if L < p:
                break
            e -= _vp_factorial(L, p)
        if e > 0:
            factors.append(p**e)
        # Divide p out of every integer in the range, once per power of p dividing it.
        pk = p
        while True:
            start = -(-base // pk) * pk - base  # index of the first multiple of pk
            if start >= small:
                break
            xs[start::pk] = [q // p for q in xs[start::pk]]
            pk *= p
    factors.extend(q for q in xs if q > 1)
    return _product(factors)


def multinomial(parts: list[int], singletons: int = 0) -> int:
    """Number of interleavings of chains of the given lengths plus ``singletons`` isolated nodes.

    Equals ``T! / prod(L!)`` with ``T = sum(parts) + singletons``.  Raises ``ValueError``
    when the answer is far too large to be produced (its size in bits is at least
    ``T - max(parts)``).
    """
    parts = [L for L in parts if L > 0]
    total = sum(parts) + singletons
    largest = max(parts, default=0)
    small = total - largest
    if small <= 0:
        return 1
    if total <= RATIO * small and total <= SIEVE_CAP:
        return _multinomial_by_sieve(total, parts)
    if small > MAX_SMALL:
        raise ValueError(
            f"|Lin(P_n)| has more than {small} bits (T={total}, max chain {largest}); too large to compute"
        )
    rest = list(parts)
    rest.remove(largest)
    return _multinomial_by_stripping(total, largest, rest)


# ----------------------------------------------------------------------------- the counter


def chain_lengths(setup: LoopSetup, n: int) -> list[int]:
    """Number of poset nodes of each thread in ``P_n``: every step of prefix, n bodies, suffix."""
    return [len(th.prefix) + n * len(th.body) + len(th.suffix) for th in setup.threads]


@register
class ChainInterleavingCounter(LoopCounter):
    name = "fable51_1-b-chains"
    description = "Multinomial of the per-thread chain lengths of P_n, via prime exponents (Legendre) and a product tree."
    capabilities = Capabilities(rcw=False, sync=False, observed_reads=False)

    def count(self, setup: LoopSetup, n: int) -> int:
        if n < 1:
            raise ValueError("n must be >= 1")
        lengths = chain_lengths(setup, n)
        # Sync points no event mentions are isolated nodes (none in case b, kept for safety).
        singletons = setup.sync_points + n * setup.loop_sync_points
        return multinomial(lengths, singletons)
