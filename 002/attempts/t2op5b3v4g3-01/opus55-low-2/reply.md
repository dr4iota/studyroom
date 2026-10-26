No sync points constrain this problem, so only program order and A3's known result limit the outcomes. All 12 combinations are possible.

**Q1 (A1).** Before A3, the only write to y is B1, which writes 4. A3 returned 4, so B1 took effect before A3.
- If A1 takes effect before B1, A1 returns 0.
- If A1 takes effect after B1, A1 returns 4.

Both orders are allowed, so A1 can return 0 or 4.

**Q2 and Q3 (B2 and B3).** The writes to z are A2 (3), A4 (4) and B5 (1).
- B5 comes after B3 in thread B, so neither read can see 1.
- Thread A writes 3 and then 4, and B2 comes before B3. So the value z holds when the reads happen only moves forward through 0, then 3, then 4.
- That leaves six possible (B2, B3) pairs: (0,0), (0,3), (0,4), (3,3), (3,4), (4,4).

**Combining the two.** Each pair can occur with either value of A1:
- **A1 = 0:** A1 goes before B1. A2 and A4 can then be placed anywhere relative to B2 and B3. A4 must still follow A3, which follows B1. That is compatible with B2 reading 4, because B2 also follows B1.
- **A1 = 4:** B1 goes before A1. B2 and B3 can still be placed before, between or after A2 and A4.

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END