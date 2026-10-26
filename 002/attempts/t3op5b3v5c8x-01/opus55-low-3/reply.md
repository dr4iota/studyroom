No two operations take effect at the same instant, so every execution is a single total order that respects each thread's program order. No sync points are used, so there are no other constraints.

**Values each operation can see**
- Let `a` be the value returned by A1. Then A2 and A3 both write `a` to z, and A4 writes `a` to y.
- The other writes to z are B1 (writes 1) and C1 (writes 2).
- B2 returns 0 or 1, depending on whether it comes before or after C2. Call that value `b`; B3 writes `b` to y.
- The final y is `a` if A4 is the later of A4 and B3, and `b` otherwise.
- B5 comes after B1, and C4 comes after C1.

**Case a = 0 (A1 takes effect before both B1 and C1)**
- B5 and C4 can each see the value of B1, C1 or the A writes. That gives 0, 1 or 2.
- The pair B5 = 2, C4 = 1 is impossible:
  - B5 returning 2 needs C1 to be the last write to z before B5, so C1 comes after B1.
  - C4 returning 1 needs B1 to be the last write to z before C4, so B1 comes after C1.
  - These contradict each other.
- Every other (B5, C4) pair is reachable. Here is the hardest one, B5 = 1 and C4 = 2 with y = 1:
  - Order: A1 (returns 0), C1, C2, C3, C4 (returns 2), A2, A3, A4, B1, B2 (returns 1), B3, B4, B5 (returns 1), C5.
  - B3 comes last among the writes to y, so y = 1.
- For each pair, y can be 0 (put A4 last, or B2 before C2) or 1 (B2 after C2 and B3 after A4).

**Case a = 1 (C1 before B1, and A1 after B1)**
- Every write to z after C1 writes 1, so B5 returns 1.
- C4 returns 2 or 1.
- y is 0 or 1. These combinations were already found in the case above.

**Case a = 2 (A1 reads C1's value)**
- B5 and C4 each return 1 or 2.
- B5 = 2 with C4 = 1 is impossible:
  - C4 returning 1 needs B1 to come after C1, A2 and A3.
  - Then nothing writes 2 to z after B1, so B5 cannot return 2.
- The pairs (1,1), (1,2) and (2,2) are all reachable with A4 last, which makes y = 2. Example for (1,2):
  - Order: C1, C2, C3, C4 (returns 2), A1 (returns 2), A2, A3, B1, B2, B3, B4, B5 (returns 1), A4, C5.
  - A4 is the last write to y, so y = 2.

**Result:** every (B5, C4) pair except (2, 1), with y = 0 or 1. In addition, y = 2 for the pairs (1,1), (1,2) and (2,2).

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 0 1
2 2 0
2 2 1
2 2 2
END