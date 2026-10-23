Every possible combination of (Q1, Q2, Q3, Q4) is listed between BEGIN and END below. These are the constraints that decide them.

**Ordering constraints**
- B1 < P < A3. So A4 starts after both A1 and B1 have taken effect.
- B2 < Q < A9 < R < B8. The sync points force this chain.
- A1 < S < B5 < B6 < B7 < B8.
- A2 is only forced to come after A1 and before A3, so it can fall after B7.

**Value of v (what A4 reads)**
- A1 writes 6 to z and B1 writes 1 to z, and both happen before A4.
- A4 returns the later of the two, so v is 6 or 1.
- Nothing else writes z between A6 and A7, so A7 also returns v.
- A8 writes v to y. No other thread writes y, so the final y is v.

**Value of w (what B2 reads)**
- If B2 runs before A8, it reads 0.
- If A8 runs before B2, it reads v. This is possible because A8 only needs to be after P, and B2 only needs to be before Q.
- B8 writes w to z, and B9 reads it back. Nothing writes z after B8, because A9 comes before R. So Q1 = Q4 = w.

**Final x**
- B7 writes 4, so x is 4 unless A2 (write 1) lands after B7, which gives 1.
- If w = v, then A8 comes before B2, and B2 comes before B7. A2 comes before A3, which comes before A8, so A2 comes before B7 and x = 4.
- If w = 0, x can be 1 or 4.

**Combinations** (Q1 Q2 Q3 Q4)
- v = 6: w = 0 with x = 1 or 4, and w = 6 with x = 4.
- v = 1: w = 0 with x = 1 or 4, and w = 1 with x = 4.

BEGIN
0 1 6 0
0 4 6 0
6 4 6 6
0 1 1 0
0 4 1 0
1 4 1 1
END