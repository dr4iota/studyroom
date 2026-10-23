Four combinations of x, y and z are possible, plus the B9 value. They follow from the ordering constraints below.

**Ordering constraints**
- B1 ends before P, and every A operation from A2 to A8 starts after P. So B1 precedes A2 through A8.
- A1 and B1 are not ordered relative to each other, so either can come first.
- B2 ends before Q, and A9 starts after Q. A9 ends before R, and B8 and B9 start after R. So B2 < A9 < B8 < B9.
- B5, B6 and B7 start after S. S comes after A1, but A2 through A8 are not ordered against S.

**z and y**
- A4 reads z after both A1 and B1 and before any other z-write. The last of those two writes decides what it sees, so A4 returns a = 6 (B1 then A1) or a = 1 (A1 then B1).
- A6 writes a to z, and A7 reads a, because B8 comes after A9 and so after A7. A8 then writes a to y, and A9 writes a to z.
- The only write to y is A8, so the final y = a, which is 1 or 6.
- B2 reads y and returns b ∈ {0, a}. It returns a only if A8 takes effect before B2, which is allowed because B2 only has to precede Q.
- B8 writes b to z after A9. B9 reads that value, since no write to z follows B8. So Q1 = Q4 = b.

**x**
- The writes to x are A2 (1), B5 (3), B6 (the value B3 read) and B7 (4).
- B7 is the last write in thread B. The final x is 4 if B7 comes after A2, or 1 if A2 comes after B7.
- If A2 comes after B7, then A8 comes after B7, which comes after B2. B2 then reads y before A8 has written it, so b = 0.

**Cases**
- x = 4: b = 0 with a = 1 or 6, or b = a with a = 1 or 6. This gives (B9, x, y, z) = (0,4,1,0), (0,4,6,0), (1,4,1,1), (6,4,6,6).
- x = 1: b = 0 with a = 1 or 6. This gives (0,1,1,0), (0,1,6,0).

BEGIN
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
0 1 1 0
0 1 6 0
END