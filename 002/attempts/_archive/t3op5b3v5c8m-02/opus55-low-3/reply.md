No sync points are given, so any interleaving that keeps each thread's own order is allowed.

**Q2 (B3, read of y).** The writes to y are A1 (4), A2 (1) and B2 (1). B3 comes after B2, so it cannot return 0.
- B3 returns 1 if the last write to y before it is B2 or A2.
- B3 returns 4 if A1 falls between B2 and B3, and A2 comes after B3. That order is B2 < A1 < B3 < A2.
- So B3 is 1 or 4.

**Q1 (A3, read of x).** The writes to x are C2 (2), C3 (1) and B4. B4 writes whatever B3 returned.
- A3 returns 0 if it takes effect before every write to x.
- A3 returns 2 or 1 if C2 or C3 is the last write to x before it.
- A3 returns 4 only if B4 writes 4, which needs B3 = 4. That order is B2 < A1 < B3 < A2 < A3, with B4 between B3 and A3. This order is valid.
- When B3 = 4, A3 can still return 0, 1 or 2 by placing the x writes accordingly.

**Q3 (final z).** The writes to z are B1 (4), A4 (A3's value), C4 (C1's value) and C5 (4). C4 comes before C5, so C4 can never be the last write.
- The last write is A4, B1 or C5.
- So the final z is either 4 or A3's value.
- A4 can always be placed last, for example after C5 and B1.

**Combinations**
- With B3 = 1: A3 is 0, 1 or 2, and z is 4 or equal to A3.
- With B3 = 4: A3 is 0, 1, 2 or 4, and z is 4 or equal to A3.

BEGIN
0 1 0
0 1 4
1 1 1
1 1 4
2 1 2
2 1 4
0 4 0
0 4 4
1 4 1
1 4 4
2 4 2
2 4 4
4 4 4
END