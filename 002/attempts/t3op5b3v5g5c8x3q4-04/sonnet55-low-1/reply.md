Working through the constraints:

**Q2 (B2).** B4 reads x after B3 has written, and it returns 0. So B3 must have written 0, which means B2 read 0.

**Q1 (A4).** The writes to z are B1 (5), C2 (5) and C3 (1), with C2 before C3. A4 can read 0 (before any z write), 5, or 1. Reading 1 needs C3 to have taken effect first.

The x reads don't rule any of these out. If A1 read a nonzero value, A3 writes that value to x. A3 can then be placed between B2 and B3, where B3 overwrites it with 0, or after B4. C4 must be placed where x is still 0. If A1 read 0, A3 writes 0 and nothing is constrained.

**Q3 (final y).** The y writes are C1 (4) and A5 (3). The final value is 3 if A5 comes after C1, and 4 if C1 comes after A5.

- If A4 = 1, then C3 took effect before A4, so C1 took effect before that. A5 comes after A4, so A5 is last and y = 3.
- If A4 = 0 or A4 = 5, either order of C1 and A5 is possible. For A4 = 5, B1 alone can supply the 5, so C1 can still come after A5.

**Combinations (A4, B2, y):** (0,0,3), (0,0,4), (5,0,3), (5,0,4), (1,0,3).

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END