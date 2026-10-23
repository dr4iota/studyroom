Every possible combination follows from which ordering constraints the sync points force and which they leave free.

**Constraints from the sync points**
- A1 ends before S, and B5–B7 start after S.
- B1 ends before P, and A3–A8 start after P.
- B1 and B2 end before Q, and A9 starts after Q.
- A9 ends before R, and B8 and B9 start after R.

**Value of A4**
- z is written by A1 (6) and B1 (1) before A4 runs, and both orders are possible. So A4 reads a ∈ {1, 6}.
- A6 writes a to z, so A7 reads a. A8 then writes a to y, and A9 writes a to z.
- Only A8 writes y, so y ends as a.
- Everything in A finishes before R, so z holds a when B8 runs.

**B2, B8 and B9**
- B2 reads y, which is either 0 (before A8) or a (after A8).
- B8 writes B2's value v ∈ {0, a} to z. Nothing writes z after B8, so B9 reads v and z ends as v.

**Final x**
- B7 writes 4 and is B's last write to x. A2 writes 1 and may fall before or after B7.
- So x ends as 4 or 1.
- If x ends as 1, then B7 < A2 < A8. B2 comes before B7, so B2 < A8 and B2 reads 0. Then v = 0.
- If x ends as 4, v can be 0 or a.

**Combinations (B9, x, y, z)**
- x = 4: (0, 4, 1, 0), (1, 4, 1, 1), (0, 4, 6, 0), (6, 4, 6, 6).
- x = 1: (0, 1, 1, 0), (0, 1, 6, 0).

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
0 1 1 0
0 1 6 0
END