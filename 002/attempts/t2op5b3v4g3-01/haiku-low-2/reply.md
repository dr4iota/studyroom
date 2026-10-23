Let a1..a5 and b1..b5 be the instants at which each operation takes effect. Within each thread these instants are increasing. The only writes to y come from B1, and the only writes to z come from A2 (value 3), A4 (value 4), and B5 (value 1). The writes to x are never read, so they don't matter.

**Constraints:**
- A3 returns 4, so b1 < a3 and B1 is the last write to y before A3.
- A1 reads y. If b1 < a1, it returns 4. If a1 < b1, it returns 0. Both are feasible, because A1 can be placed before or after B1 and still precede a3.
- B5 comes after B2 and B3 in program order, so the value 1 is never seen by either read.
- B2 can read 0, 3, or 4. It reads 0 if b2 < a2, 3 if a2 < b2 < a4, and 4 if a4 < b2.
- B3 can read 0, 3, or 4 in the same way, using b3. Since b2 < b3, some pairs are impossible:
  - (B2, B3) = (3, 0) requires a2 < b2 < b3 < a2, which is a contradiction.
  - (4, 0) and (4, 3) require a4 < b2 < b3, which contradicts a4 > b3 or a4 > a2 > b3 (for 0 and 3 respectively).
  - The six remaining pairs (0,0), (0,3), (0,4), (3,3), (3,4), (4,4) each have a valid ordering.
- Each of the six pairs can be combined with either value of A1. Placing a1 and b1 at the start of the schedule (in either order) makes both A1 outcomes compatible with every pair, while b1 < a3 still holds.

That gives 2 × 6 = 12 combinations, in the order Q1 Q2 Q3:

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END