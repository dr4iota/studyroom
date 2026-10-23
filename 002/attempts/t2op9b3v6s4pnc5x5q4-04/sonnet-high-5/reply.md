Every possible outcome is listed in the block at the end; here is the reasoning.

**Ordering constraints**
- B1 ends before P, and A3 onward start after P, so B1 is before A4.
- A1 is also before A4. A4 is the first read of z by A, so it reads the later of A1 (6) and B1 (1). Call that value v, with v ∈ {6, 1}. Both orders of A1 and B1 are possible.
- A6, A7, A8 and A9 never see another write to z. A6 writes v and A7 reads v, so A8 writes v to y. A9 then writes v to z.
- y is only ever written by A8, so the final y is v.
- B2 reads y. It is before Q, and A8 has no constraint against Q, so B2 reads 0 (before A8) or v (after A8).
- B8 comes after R, which is after A9, so B8 is the last write to z. B8 writes B2's value, and B9 reads it. So B9 = final z = B2's value, which is 0 or v.

**Final x**
- B5, B6 and B7 come in that order, and B7 writes 4.
- A2 writes 1 and must be before A3 and after A1. A2 can fall before B7, giving final x = 4. It can also fall after B7, giving final x = 1.
- If A2 is after B7, then B2 < B3 < B4 < B5 < B6 < B7 < A2 < A8. That forces B2 to be before A8, so B2 = 0.
- If B2 = v (nonzero), A2 must be before B7 and x = 4.

**Combinations (B9, x, y, z)**
- x = 4: B2 = 0 with v = 1 or 6 gives (0, 4, 1, 0) and (0, 4, 6, 0). B2 = v gives (1, 4, 1, 1) and (6, 4, 6, 6).
- x = 1: B2 must be 0, so (0, 1, 1, 0) and (0, 1, 6, 0).

BEGIN
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
0 1 1 0
0 1 6 0
END