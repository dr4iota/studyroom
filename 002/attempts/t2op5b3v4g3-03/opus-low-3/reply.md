**Approach.** There are no sync points, so any interleaving that keeps each thread's own order is allowed.

**B5 is consistent.** B4 is the only write to z, and it comes before B5 in thread B. So B5 always returns 1, and every interleaving agrees with the known result.

**Q1 (A5).** A5 returns 1 if B4 takes effect before A5, and 0 otherwise. Both orders are possible, so A5 is 0 or 1.

**Q2, Q3 (B1, B2).** Both reads come before B3, so they can only see 0 or A's writes. A writes y = 1 (A2) and then y = 3 (A3). Over time, B therefore sees y as 0, then 1, then 3. Since B1 comes before B2, B2 can never see an earlier value than B1. That gives six pairs: (0,0), (0,1), (0,3), (1,1), (1,3), (3,3).

**Independence.** Each of the six pairs works with A5 = 0 or A5 = 1:
- **A5 = 1:** run B4 just before A5. B1 and B2 can still read y at any point in A's writes.
- **A5 = 0:** let A finish completely, including A5, before B3 and B4. B1 and B2 can still be placed anywhere among A2 and A3 before that.

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