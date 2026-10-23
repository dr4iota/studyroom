Neither thread has sync points, so any interleaving that keeps each thread's own order is allowed.

**Reads of y (Q1, Q2).** The writes to y are B3 (4) then B4 (2), so y goes 0, then 4, then 2 over time. A3 and A4 are consecutive reads of y in thread A, so A3 cannot see a later stage than A4. The possible (A3, A4) pairs are (0,0), (0,4), (0,2), (4,4), (4,2) and (2,2).

**Read of x (Q3).** B2 returns 0 if it takes effect before A1, and 3 if it takes effect after A1.

**Combining them.** B3 and B4 come after B2 in thread B, and A2 to A4 come after A1 in thread A. That leaves enough freedom for every pair of y values with either value of B2:
- If B2 returns 0, then B2 comes before A1. B3 and B4 can still be placed anywhere relative to A3 and A4. For example, (4,2) works as B2, A1, A2, B3, A3 reads 4, B4, A4 reads 2.
- If B2 returns 3, then A1 comes before B2. A3 and A4 can still fall before B3 (giving 0,0), between B3 and B4, or after B4.

So all 6 pairs combine with both values of B2, which gives 12 outcomes.

BEGIN
0 0 0
0 0 3
0 4 0
0 4 3
0 2 0
0 2 3
4 4 0
4 4 3
4 2 0
4 2 3
2 2 0
2 2 3
END