**Answer: four asked values, three possible combinations.** A2 always reads 0, the final y is always 2, and C4 and the final x can each be 2 or 3, but not (C4=3, final x=2).

**Key constraints**

- **B5 reads y=2.** The only write of 2 to y is C3, which can only write 2 if C2 read 2. So C3 must be the last y-write before B5, and C1 must be the last x-write before C2, with B2 and B4 not between them.
- **B3 reads y=4.** The only write of 4 to y is B1, so B1 is the last y-write before B3.
- **A3 reads y=4.** A1 precedes A3 in program order, so A1 must come before B1. C3 must come after A3.

These force the order A1 < B1 < A3 < C3 < B5, with B1 < B3 < C3 and C1 < C2 < C3.

**Asked values**

- **Q1 (A2):** z is only written by C5, which comes after C3 and therefore after A2. So A2 always reads 0.
- **Q4 (final y):** C3 is the last y-write, since A1 and B1 both precede it. So the final y is always 2.
- **Q2 (C4) and Q3 (final x):** the x-writes are C1 (2), B2 (3) and B4 (3), with B2 < B3 < B4. C4 can read 2 or 3, and the final x can be 2 or 3. Feasible schedules:
  - (2, 2): A1 B1 A2 A3 B2 B3 B4 C1 C2 C3 C4 C5 B5
  - (2, 3): A1 B1 A2 A3 B2 B3 C1 C2 C3 C4 B4 C5 B5
  - (3, 3): A1 B1 A2 A3 B2 B3 C1 C2 B4 C3 C4 C5 B5
- **(3, 2) is impossible.** C4 reading 3 needs B4 or B2 after C2, which means C1 cannot be the last x-write overall.

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END