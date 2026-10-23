Every operation takes effect at one instant, so the run is a single total order of operations, consistent with each thread's program order.

**Constraints**

- **B1 reads 1:** some write of 1 must come before B1. That is A1, A3, or a C write that copies a 1.
- **B2 can return 0, 1, 2 or 3.**
  - It returns 0 only if C1 read 0, which needs C1 before A1. Then C2 or C3 writes 0, and B2 reads it after B1 has read 1.
  - Otherwise B2 reads a value written by A, or a copy of one.
- **C1 can return 0, 1, 2 or 3.** It reads whatever is in x when it takes effect.
- **B2 and C1 cannot both read each other's copy.** That would need B3 < C1 < C2 < B2 < B3, which is a cycle.
- **Final x** is the value of the last write among A4 (2), B3 (B2's value) and C3 (C1's value). C3 always comes after C2.

**Cases by C1 (Q2)**

- **C1 = 0** (C1 before A1):
  - B2 can return 0 by reading C2 or C3.
  - B2 can return 1, 2 or 3 by reading an A write.
  - The final value can be 2 (A4 last), B2's value (B3 last) or 0 (C3 last).
- **C1 = 1:** no 0 is ever written, so B2 returns 1, 2 or 3. The final value can be 2, B2's value or 1.
- **C1 = 3** (C1 between A2 and A3):
  - If B2 = 1, the final value can be 1, 2 or 3.
  - If B2 = 3, the final value can be 2 or 3.
  - If B2 = 2, the final value can be 2 or 3 (C3 written after A4 and B3).
- **C1 = 2** (C1 after A4, or after B3 copies a 2):
  - If B2 = 1, the final value can be 1 (B2 before A2, B3 last) or 2.
  - If B2 = 3, the final value can be 3 or 2.
  - If B2 = 2, the final value is 2.

The combinations below list B2, C1 and the final value of x, in that order.

BEGIN
0 0 0
0 0 2
1 0 0
1 0 1
1 0 2
2 0 0
2 0 2
3 0 0
3 0 2
3 0 3
1 1 1
1 1 2
2 1 1
2 1 2
3 1 1
3 1 2
3 1 3
1 3 1
1 3 2
1 3 3
3 3 2
3 3 3
2 3 2
2 3 3
1 2 1
1 2 2
3 2 2
3 2 3
2 2 2
END