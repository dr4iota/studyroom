**Q1 (value returned by B4) can be 3 or 5.**

**Constraints from y = 0 at the end**
- y is written by A1 (3), C1 (3) and B2 (the value B1 read).
- For y to end at 0, B2 must be the last write to y, and B1 must have read 0.
- So B1 takes effect before A1 and C1, and B2 takes effect after both.

**Constraints from x = 3 at the end**
- x is written by C2 (5) and C5 (the value C3 read).
- C5 comes after C2 in thread C, so it is the last write to x. Therefore C3 must have read 3.
- C3 follows C1 in thread C. To read 3, C3 must take effect before B2 overwrites y with 0.

**What B4 can see**
- B4 follows B2, and C3 takes effect before B2. Since C2 precedes C3, C2 takes effect before B4.
- So when B4 reads x, x holds either 5 (from C2) or 3 (from C5).

**Witness orders**
- B1, C1, A1, C2, C3, B2, B3, B4, C4, C5 gives B4 = 5. A2, A3, A4 and A5 fit in anywhere after A1.
- B1, C1, A1, C2, C3, B2, C4, C5, B3, B4 gives B4 = 3.

BEGIN
3
5
END