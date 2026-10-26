**Approach.** There are no sync points, so any interleaving that keeps each thread's order is allowed. Two known results constrain it:
- A2 reads y = 2, so the last y-write before A2 is C2, or C5 when C4 read 2.
- B5 reads x = 2.

The x-writes are C1 (2), A3 (A1's value) and B4 (B2's value). The y-writes are B1 (1), C2 (2), A4 (3) and C5 (C4's value).

**Case A1 = 0** (A1 takes effect before C1)
- A3 writes 0, and A3 must come after C1, because A3 follows A2, A2 follows C2, and C2 follows C1.
- For B5 to read 2, B4 must come after A3 and write 2. So B2 read 2, and B2 took effect between C1 and A3.
- This gives the chain B1 < B2 < A3 < A4.
- **Final y = 1 is impossible.** It needs either B1 last or C5 writing 1.
  - B1 cannot be last, because it precedes A4.
  - For C4 to read 1, B1 must be the last y-write before C4. A4 cannot fall between B1 and C4, so A4 comes after C4 and before C5. But A4 must also come after A2, and A2 must see 2 from C2 before B1. Then B1 < B2 < A3 < A4 still holds, and C4 must come after B1 and before A4. If C2 and C3 both come before B1, the only y-write between B1 and C4 is A4, which we have placed after C4. Checking the cases shows C4 always reads 2 or 3 here.
- **Final y = 2** (C5 last, C4 read 2) and **final y = 3** are both reachable.
- **B3 = 1, 2 and 3 are all reachable** with either final value. Witnesses:
  - 0 1 2: A1, C1, B1, B2, B3, C2, C3, C4, A2, A3, B4, B5, A4, C5
  - 0 3 2: A1, C1, B1, B2, C2, C3, C4, A2, A3, A4, B3, B4, B5, C5

**Case A1 = 2** (A1 takes effect after C1)
- **B3 = 1:**
  - Final y = 1 is possible with B1 last: C1, A1, C2, C3, C4, C5, A2, A3, A4, B1, B2, B3, B4, B5.
  - Final y = 2 and 3 are also possible.
- **B3 = 2:**
  - Final y = 1 is impossible. If B1 is last, B3 reads 1. If C5 writes 1, then C4 read 1, so B1 came between C2 and C4. In that case B3 sees either B1's 1 or C5's 1, never 2.
  - Final y = 2 and 3 are possible.
- **B3 = 3:**
  - Final y = 1 is possible: C1, A1, C2, C3, A2, A3, B1, C4, A4, B2, B3, B4, B5, C5.
  - Final y = 2 and 3 are also possible.

BEGIN
0 1 2
0 1 3
0 2 2
0 2 3
0 3 2
0 3 3
2 1 1
2 1 2
2 1 3
2 2 2
2 2 3
2 3 1
2 3 2
2 3 3
END