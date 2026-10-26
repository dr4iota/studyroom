**Key constraints:**
- B1 (write 1 to z) is before P; A2…A9 are after P, so A4 reads z after both A1 and B1 took effect. A1's only constraint is "before S", so A1 and B1 can be in either order → A4 returns 1 or 6.
- A7 reads z after A6 wrote A4's value and before any later z-write (A9, B8 come later), so A7 = A4, and A8 writes that value to y. A8 is the only write to y → final y = A4.
- B2 reads y before Q, while A8 happens after Q → B2 = 0. B8 writes 0 to z after R, and R is after A9, so B8 is the last z-write → B9 = 0, final z = 0.
- A2 < A9 < R < B7, so B7 (write 4) is the last x-write → final x = 4.

BEGIN
0 4 1 0
0 4 6 0
END