# Sources — `looplin_b_fable51_1`

One algorithm, `fable51_1-b-chains` (`counter.py`).

## Reduction: `|Lin(P_n)|` is a multinomial coefficient

**Own derivation** from the spec. Without sync points (§6, case `b`) the order of the
trace poset is the transitive closure of program order alone (§3), so there is no
relation between steps of different threads and `P_n` is a disjoint union of `N` chains,
one per thread. A linearization is then an interleaving of the chains, and the number
of interleavings of chains of lengths `L_1..L_N` is `T!/(L_1!…L_N!)`, `T = ΣL_t`
(standard counting: choose the positions of each chain in turn). The chain length of a
thread in `P_n` is `|prefix| + n·|body| + |suffix|` steps (every start and done is a
node; §8 unrolls the body `n` times). Write data (§4, §8) creates no edge, since it
refers only to earlier steps of the same thread, so it does not affect the count.

A declared sync point no event mentions is an isolated node (§2); I count each as a
chain of length 1. Case `b` has none, so this only matters if a setup declares unused
sync points.

## Computing the multinomial exactly

**From memory, folklore methods:**

- Legendre's formula `v_p(x!) = Σ_k ⌊x/p^k⌋` (A.-M. Legendre, *Essai sur la théorie des
  nombres*, 1808).
- Computing binomial/multinomial coefficients as `Π p^{v_p(T!) − Σ v_p(L_t!)}` over the
  primes `p ≤ T`, so no big-integer division is needed. I recall this from
  P. Goetgheluck, "Computing binomial coefficients", *American Mathematical Monthly*
  (1987), and from Peter Luschny's notes on fast factorial algorithms ("prime swing").
- Balanced (pairwise) product trees for multiplying many integers, and the bytearray
  sieve of Eratosthenes: standard techniques.

**Own adaptation** — the "stripping" regime for `T ≫ S = T − max L_t` (e.g. only one
thread loops and `n` is around `10^9` or `10^18`): write the multinomial as
`[Π_{x ∈ (L_max, T]} x] / Π_{other t} L_t!`. The denominator has only primes `≤ S`, so
for every prime `p ≤ S` I take its net exponent by Legendre's formula and divide `p`
out of the `S` consecutive integers (slice by slice, one pass per power of `p`, like a
segmented sieve); the leftovers are coprime to the denominator and are multiplied in
unchanged. This needs primes up to `S` only, and the work is proportional to `S`, not
`T`. The regime switch (`T ≤ 10·S` and `T ≤ 10^8` → sieve regime) is a rough cost
estimate of my own.

## Uncertainties

- I could not run anything; the arithmetic was checked by hand on small cases
  (`[3,2] → 10`, `[4,4] → 70`, `[2,2,2] → 90`, `[1,1,1] → 6`) in both regimes.
- The answer has about `T·H` bits (`H` the entropy of the chain-length proportions), so
  when two or more threads have bodies the output itself grows linearly with `n`. For
  `T − max L_t > 8·10^6` the counter raises `ValueError` rather than exhausting memory;
  such answers are out of reach inside the time limit anyway. The caps and the regime
  threshold are estimates, not measurements.
- Isolated sync nodes are counted as singleton chains; with any `before`/`after`/`at`
  event the count would be wrong, but the declared capabilities exclude sync setups.
