Because the operations have no sync points, every execution is an interleaving that keeps each thread's order. Each operation takes effect at one instant.

**Q1 (A5).** The only write to z is B4, which writes 1. So A5 returns 0 if it takes effect before B4, and 1 if it takes effect after B4. Both are possible.

**Q2 and Q3 (B1, B2).** B1 and B2 both take effect before B3. The writes to y are A2 (1), A3 (3) and B3 (1).

Since B1 and B2 come before B3, they can only see values written by A2 and A3. Only A2 and A3 matter, and A2 comes before A3. So y goes 0, then 1, then 3 as seen by B1 and B2. B2 comes after B1, so the pair (B1, B2) is non-decreasing along that sequence. The possible pairs are (0,0), (0,1), (0,3), (1,1), (1,3) and (3,3).

**Combining with Q1.**
- **A5 = 0:** A1 through A5 all take effect before B4. B1 and B2 only need to come before B3, so they can fall anywhere relative to A2 and A3. All six pairs are possible.
- **A5 = 1:** B3 and B4 come before A5, but A2 and A3 can still come before or after B1 and B2. For example, A2 and A3 can both take effect before B1, which gives (3,3). Or B1 and B2 can both come first, giving (0,0). All six pairs are possible again.

That gives 2 × 6 = 12 combinations.

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