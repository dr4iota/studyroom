Only B2 writes y (value 4). B1 therefore always returns 0, and A1 returns 0 or 4 depending on whether it takes effect before or after B2.

**Q1 (A1):** A1 can run before B2 and return 0. It can also run after B2 and return 4.

**Q2 (B3):** B3 returns the latest of A's writes to x that took effect before it. B5 comes after B3 in B's order, so it cannot affect B3.
- It returns 0 if no A write has happened yet.
- It returns 2 if A2 has happened but not A3, or if A5 has happened.
- It returns 4 if A3 has happened but not A5.

**Q3 (final x):** The final value is set by whichever of A5 (writes 2) and B5 (writes 4) takes effect last. B5 must come after B3 but can fall before or after A5, so either result is possible.

Each of these choices can be made independently of the others:
- If A1 returns 4, then B2 < A1 < A2 < … < A5. B3 follows B2 and can land at any point among A's writes. B5 follows B3 and can land before or after A5.
- If A1 returns 0, then A1 < B2 < B3 < B5. A's later steps can be placed freely around B3 and B5.

All 2 × 3 × 2 = 12 combinations are therefore achievable.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END