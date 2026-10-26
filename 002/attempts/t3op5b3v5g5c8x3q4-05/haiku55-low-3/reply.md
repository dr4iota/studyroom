**Key deductions**

- **C2 = 2 is forced.** B5 reads y = 2, and the only write of 2 to y is C3, which writes C2's value. So C2 must return 2.
- **Y-order is forced.** A3 reads 4, B3 reads 4, and B5 reads 2. Together with thread order, these force A1 < B1 < B3 < C3 < B5 and A3 < C3. So the last write to y is C3, and **final y = 2**.
- **A2 = 0.** A2 precedes A3, which precedes C3, which precedes C5 (the only write to z). So A2 always reads z before it is written, and **A2 returns 0**.
- **x-writes.** C2 = 2 means no 3-write (B2 or B4) can fall between C1 and C2. So each of B2 and B4 is either before C1 or after C2.
  - Both before C1: C4 = 2, final x = 2. Feasible.
  - B2 before C1, B4 after C2: final x = 3. B4 can fall before C4 (C4 = 3) or after C4 (C4 = 2). Both feasible.
  - Both after C2: final x = 3. B2 < B3 < C3 < C4 forces C4 = 3. Feasible.
  - C4 = 3 with final x = 2 is impossible, because any 3-write after C2 comes after C1 and so would be the final x.

**Possible (Q1 Q2 Q3 Q4) combinations:** (0, 2, 2, 2), (0, 2, 3, 2), (0, 3, 3, 2).

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END