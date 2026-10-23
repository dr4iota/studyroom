Q2 is always 0, and Q3 can be 3 or 4. Q1 can be 0, 5, or 1, but 1 forces Q3 = 3.

**Q2 (B2's read) is always 0.** If A3 wrote a nonzero value v before B2, then B3 would write v to x after A3, and nothing later would overwrite it before B4. B4 would then read v, not 0. So B2 reads 0.

**Q3 (final y).** The only writes to y are C1 (4) and A5 (3), and no x or z constraint touches them. The final value is whichever of the two takes effect later.
- Final y = 3: C1 before A5, which is easy to arrange.
- Final y = 4: A5 before C1. Since C1 precedes C2, C3, and C4, this requires A4 < A5 < C1 < C2 < C3.

**Q1 (A4's read of z).** The values of z are 0, 5 (from B1 or C2), and 1 (from C3).
- **0:** A4 occurs before B1 and C2. Example order: A1, A2, A3, A4, A5, C1, B1, B2, B3, B4, C2, C3, C4. Final y = 4 is possible, and final y = 3 also works by moving A5 after C1.
- **5:** A4 occurs after B1 or C2, with C3 after A4. Example: A1, A2, A3, B1, A4, A5, B2, B3, B4, C1, C2, C3, C4 gives final y = 4. Moving A5 after C1 gives final y = 3.
- **1:** C3 must precede A4. Then C1 < C2 < C3 < A4 < A5, so C1 is before A5 and final y = 3 is forced. Example: A1, A2, A3, C1, C2, C3, A4, A5, B1, B2, B3, B4, C4.

All x writes in these examples are 0, so B4 and C4 read 0 and the constraints hold.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END