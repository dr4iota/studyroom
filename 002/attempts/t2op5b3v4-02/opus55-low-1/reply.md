All 12 combinations are possible: any of the 6 (A3, A4) pairs can occur with B2 returning either 0 or 3. There are no sync points and no known read results, so only the order rules within each thread limit the outcomes.

**B2 (read x).** Only A1 writes x, so B2 returns 0 or 3.
- B2 returns 0 when B2 takes effect before A1.
- B2 returns 3 when B2 takes effect after A1.

**A3 and A4 (read y).** y moves from 0 to 4 (B3) to 2 (B4), and never goes back. A3 runs before A4, so A4's value is at the same point in that sequence as A3's, or later. That gives 6 possible pairs:
- (0, 0), (0, 4), (0, 2), (4, 4), (4, 2), (2, 2)

**Combining the two.** The value of B2 does not restrict A3 and A4:
- **If B2 returns 0:** the order is B1, B2, A1, A2, and then A3 and A4 can be placed anywhere relative to B3 and B4. For example, A3 can still read 0 with the order B2, A1, A2, A3, B3.
- **If B2 returns 3:** B2, B3 and B4 all come after A1. A3 and A4 also come after A1, so they can be interleaved freely with B3 and B4.

BEGIN
0 0 0
0 4 0
0 2 0
4 4 0
4 2 0
2 2 0
0 0 3
0 4 3
0 2 3
4 4 3
4 2 3
2 2 3
END