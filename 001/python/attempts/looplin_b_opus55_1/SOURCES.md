# Sources

## `opus55_1-b-multinomial` (counter.py)

- **Structure of the poset:** own derivation. With no sync points, the only order is
  program order, so `P_n` is a disjoint union of chains (one per thread, of length
  `len(prefix) + n*len(body) + len(suffix)`). Linearizations of disjoint chains are the
  interleavings, counted by the multinomial coefficient. Read-dependent data does not
  affect the order.
- **Multinomial via prime factorisation:** from memory. Legendre's formula for the
  exponent of a prime in `m!` (A.-M. Legendre, *Essai sur la théorie des nombres*,
  1798/1808), applied to `T! / prod L_t!`; primes from a sieve of Eratosthenes; balanced
  (binary-split) products of primes grouped by equal exponent, a standard technique for
  fast factorials/binomials (e.g. P. Luschny's notes on fast factorial algorithms, and
  P. B. Borwein, "On the complexity of calculating factorials", J. Algorithms, 1985).
  Small totals use direct `math.factorial` division.

## Unsure about

- Whether a case-b setup can have `loop_sync_points > 0` with no events. The spec says
  an unmentioned sync point is still an (isolated) virtual step, so such steps are
  counted as isolated elements; with no sync points at all this term is 1.
- Setups that do contain events are outside case b; the counter raises `ValueError`.
- Very large `n` (e.g. `10^9`): the answer itself has billions of bits, so only
  moderate `n` can finish in the time limit.
