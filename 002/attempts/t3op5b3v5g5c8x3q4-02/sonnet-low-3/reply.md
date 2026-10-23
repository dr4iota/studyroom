A2 always returns 0, A4 can return 0, 3 or 4, and C3 returns 0 or 4. The combinations are below.

**A2.** The only write to y anywhere is A3 (value 4), and A2 comes before A3 in thread A. So A2 always returns 0.

**C3.** C3 reads y, which is either 0 (before A3) or 4 (after A3). C4 writes C3's value to x, so C4 writes either 0 or 4.

**Constraints from the known reads.** A1 returns 3, so C1 (the only write of 3 that can come first) must take effect before A1, with no other write to x in between. C2 returns 3, and C3 comes after C2.

**Case C3 = 0.** C3 is before A3, and A4 is after A3.
- A4 = 3: order B1, C1, A1, C2, C3, A2, A3, A4, then C4. C1 is the last write to x before A4.
- A4 = 4: order C1, A1, C2, B1, then A4, with C4 after A4 or at least before nothing that overwrites 4. B1 is the last write to x before A4.
- A4 = 0: order C1, A1, C2, B1, C3, C4, A2, A3, A4. C4 writes 0 and is the last write to x before A4.

**Case C3 = 4.** A3 comes before C3, so C1, A1, A2, A3, C3, C4 are in that order, and C4 writes 4.
- A4 = 3: A4 is before C4, with B1 before C1. C1 is the last write to x before A4.
- A4 = 4: B1 (or C4) is the last write to x before A4.
- A4 = 0: impossible, because no write of 0 to x can take effect before A4 here.

BEGIN
0 3 0
0 4 0
0 0 0
0 3 4
0 4 4
END