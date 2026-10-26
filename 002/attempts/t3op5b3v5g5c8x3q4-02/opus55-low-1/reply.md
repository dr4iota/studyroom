**Q1 (A2).** Only A3 ever writes to y. A2 runs before A3 in thread A, so no write to y can come before A2. A2 therefore returns 0.

**Q3 (C3).** Block y is either still 0 or holds the 4 written by A3.
- If C3 takes effect before A3, it returns 0.
- If C3 takes effect after A3, it returns 4.
C4 then writes that same value (0 or 4) to x.

**Constraints from the known results.**
- A1 returns 3, so C1 (which writes 3 to x) takes effect before A1. No other write to x can fall between C1 and A1. B1 writes 4 and C4 writes 0 or 4, so neither may fall between them.
- C2 also returns 3, so B1 cannot fall between C1 and C2.
- C4 comes after C2 in thread C, so C4 is never the last write to x before A1.

**Q2 (A4).** A4 returns the last write to x before it. That can be C1 (3), B1 (4) or C4 (the value C3 read).

**Case C3 = 0** (C3 before A3):
- A4 = 3: order B1, C1, C2, A1, C3, A2, A3, A4, C4.
- A4 = 4: order C1, C2, A1, C3, A2, A3, B1, A4.
- A4 = 0: order B1, C1, C2, A1, C3, C4, A2, A3, A4.

**Case C3 = 4** (A3 before C3):
- A4 = 3: order B1, C1, C2, A1, A2, A3, A4, C3, C4.
- A4 = 4: order C1, C2, A1, A2, A3, C3, C4, A4 (C4 writes 4).
- A4 = 0 is impossible. The only write of 0 to x is C4, and here C4 writes 4.

BEGIN
0 3 0
0 4 0
0 0 0
0 3 4
0 4 4
END