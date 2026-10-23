All 12 combinations are possible: Q1 can be 0 or 1, and (Q2, Q3) can be any of six pairs, in any mix.

**Q1 (value returned by A5).** Only B4 ever writes z, and it writes 1.
- If A5 takes effect before B4, it returns 0.
- If A5 takes effect after B4, it returns 1.

Both orders are allowed, so Q1 is 0 or 1. B5 always comes after B4 in thread B, so it always returns 1, which matches its known result.

**Q2 and Q3 (values returned by B1 and B2).** Both reads take effect before B3, which is B's only write to y. So they can only see 0 or values written by thread A. A writes 1 to y (A2) and then 3 to y (A3). Over time y therefore goes 0 → 1 → 3. B1 comes before B2, so B2 never sees an earlier value than B1. That gives six pairs:
(0,0), (0,1), (0,3), (1,1), (1,3), (3,3).

**Q1 does not restrict the pairs.** A5 returning 0 only requires A5 to come before B4. That fits with every pair:
- **Q1 = 0:** run A2–A5 at the point that gives the chosen B1/B2 values, and finish thread A before B3.
- **Q1 = 1:** delay A5 until after B4.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 1
0 1 3
0 3 3
1 0 0
1 0 1
1 0 3
1 1 1
1 1 3
1 3 3
END