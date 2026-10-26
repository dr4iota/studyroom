Every write to x stores a value read from x, and x starts at 0, so x never holds anything but 0. That fixes B1 = 0 (consistent with B4 = 0).

**Q2 (B2).** The only write of 1 to y is B5, and B5 comes after B2, so B2 cannot return 1. The other values are possible:
- 0: B2 takes effect before C1.
- 2: B2 takes effect after C1 and before any later write.
- 3: B2 takes effect after A4.

**Q3 (C3).** C3 comes after C1. Each value is possible:
- 0: A5 writes 0, since A1 read 0.
- 1: B5 writes 1.
- 2: C1 is the last write before C3.
- 3: A4 is the last write before C3.

**Combinations of Q2 and Q3.** Any B2 in {0, 2, 3} can pair with any C3 in {0, 1, 2, 3}. The case that needs the most care is B2 = 3 with C3 = 2: C3 takes effect after C1 and before A4, while B2 takes effect after A4.

The known result A2 = 2 is satisfiable alongside all of these, because C1 can write 2 before A2 reads.

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END