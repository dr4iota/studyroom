Possible outcomes for (Q1, Q2) are (0, 0), (1, 0), and (1, 1).

**Key facts**

- **y is always 0.** Only A2 writes y, and it writes the value A1 read. Starting from 0, the only value that can ever appear is 0. So A1 reads 0, A2 writes 0, and B3's result of 0 is consistent.
- **A4 always writes 0 to x**, and B1 always writes 1 to x. So final x is 0 or 1, namely whichever of A4 and B1 takes effect later.
- **C2 reads 3 from z**, so the last z-write before C2 must be a 3-write (B2 or B4). That forces C1 < C2 < C3 and rules out C1, C3, or A5 falling in the window between that 3-write and C2.
- **B1 < B2 < C2 < C3 < C4**, because of thread order and the z constraint. So B1 always takes effect before C4.

**Consequences**

- Since B1 is always before C4, C4 can only read 0 if A4 is after B1 and before C4. It can only read 1 if A4 is not the last x-write before C4, which means B1 is the last one.
- (0, 1) is impossible. It needs A4 < B1, which makes B1 the last x-write before C4, so C4 would read 1.

**Witnesses for the three remaining outcomes**

- **(1, 0):** C1, B1, B2, C2, C3, C4, B3, B4, A1–A4, A5 in that order. C2 sees 3, C4 sees 1 from B1, and A4 later makes final x = 0.
- **(1, 1):** A1–A4, B1, C1, B2, C2, B3, B4, C3, C4, A5 in that order. C2 sees 3, C4 sees 1 from B1, and B1 is last, so final x = 1.
- **(0, 0):** C1, B1, B2, C2, C3, A1–A4, C4, B3, B4, A5 in that order. C2 sees 3, C4 sees 0 from A4, and A4 is last, so final x = 0.

BEGIN
0 0
1 0
1 1
END