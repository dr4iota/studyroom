The possible outcomes are 21 combinations of (Q1, Q2, Q3).

**Approach.** Each operation takes effect at a distinct instant, so the question reduces to which interleavings of the threads respect program order. The writes that matter are z=1 (B1), z=2 (C1), z=a and z=a (A2, A3), where a is the value A1 read, and y=a (A4) and y=b (B3), where b is the value B2 read. B2 reads 1 exactly when C2 precedes it.

- **Q3 (final y)** is the value of whichever of A4 or B3 takes effect later. If A4 is last, y=a. If B3 is last, y=b.
- **Q1 (B5)** and **Q2 (C4)** read the most recent z-write before them, and a can be 0, 1 or 2 depending on whether A1 falls before, between, or after B1 and C1.

Enumerating the orderings of B1, C1, A1, A2, A3 and checking where B5, C4, B2, C2, A4 and B3 can fall gives:

- **a = 0 or 1 or 2** cases allow the following final-y values: final y = 0 (9 pairs), final y = 1 (8 pairs), and final y = 2 (4 pairs, only when a = 2, which forces Q1 and Q2 to be 1 or 2).
- Some pairs are excluded, e.g. (Q1, Q2, Q3) = (2, 0, 1), because Q2 = 0 needs a = 0 while Q1 = 2 with Y = 1 needs B5 to see a later write of value 2, which conflicts with that.

Spot-checked witnesses include: (2, 0, 0) with A1 first, then B1, C1, A2, A3, C4 reading 0; (0, 1, 1) with A1, C1, C2, B1, C4 reading 1, then A2, A3, A4, B2, B3; and (2, 1, 1) with C1, A1, C2, B1, C4 reading 1, then B2, A2, A3, A4, B3, B5 reading 2.

BEGIN
0 0 0
0 1 0
0 2 0
1 0 0
1 1 0
1 2 0
2 0 0
2 1 0
2 2 0
0 0 1
0 1 1
0 2 1
1 0 1
1 1 1
1 2 1
2 1 1
2 2 1
1 1 2
1 2 2
2 1 2
2 2 2
END