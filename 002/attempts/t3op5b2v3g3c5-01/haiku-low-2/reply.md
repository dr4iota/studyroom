Every possible outcome comes from one of three values of B1's read, v ∈ {0, 1, 2}. In each case the final value of x is v, since B2 and B3 both write v and B3 is last. Each case is confirmed by an explicit interleaving that satisfies A3 = 0:

- **v = 0:** B1 precedes every write to y, so x stays 0 throughout. A4 can be 0, 1, or 2.
- **v = 2:** C2 precedes B1, and C5 comes after B1. A4 can be 0, 1, or 2. C3 can be 0 (before B2) or 2 (after B2).
- **v = 1:** C5 precedes B1, so C3 is always 0. A4 can be 0, 1, or 2.

This gives 12 combinations of (Q1, Q2, Q3), with no duplicates.

BEGIN
0 0 0
1 0 0
2 0 0
0 0 1
1 0 1
2 0 1
0 0 2
0 2 2
1 0 2
1 2 2
2 0 2
2 2 2
END