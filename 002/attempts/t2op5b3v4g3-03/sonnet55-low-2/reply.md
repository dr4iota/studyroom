Operations take effect one at a time, and there are no sync points. So the possible outcomes are the interleavings of each thread's operations in program order.

**Q1 (A5).** Only B writes z, and it writes 1 in B4. So A5 returns 0 if it takes effect before B4, and 1 if it takes effect after. Both are possible, and neither restricts B1 or B2.

**Q2 and Q3 (B1, B2).** B3 is the only write to y in B, and it comes after B1 and B2. So B1 and B2 can only see values written by A2 and A3, in the order those writes take effect. The value of y over time is therefore 0, then 1 (A2), then 3 (A3). B1 reads before B2, so B2 sees the same stage or a later one. The possible (B1, B2) pairs are (0,0), (0,1), (0,3), (1,1), (1,3), (3,3).

**Combining.** Every (B1, B2) pair can be made to occur with A5 reading 0 or with A5 reading 1:
- For A5 = 0, B1 and B2 can take effect at any point before B4, so any pair works.
- For A5 = 1, B can run its reads at any stage of A's writes, and A5 then runs after B4.

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