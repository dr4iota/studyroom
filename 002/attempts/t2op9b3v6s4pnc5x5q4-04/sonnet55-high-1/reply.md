Every outcome has B9 = 0 and final z = 0. The final x is 1 or 4, and the final y is 1 or 6.

**Constraints from the sync lines**
- B1 comes before P, and A3 through A9 come after P.
- B2 comes before Q, and A9 comes after Q. A8 follows A7 in thread order, so A8 and A9 both come after B2.
- All of A comes before R, and B8 and B9 come after R.
- A1 comes before S, and B5 through B9 come after S.

**y and z**
- The only write to y is A8, and it happens after Q. B2 happens before Q, so B2 reads 0.
- B8 therefore writes 0 to z.
- B8 and B9 come after every A operation, and B1 comes before P, so B8 is the last write to z. B9 reads 0 and the final z is 0.
- A4 reads z after both A1 and B1 have written. Those two writes can happen in either order, so A4 returns 6 or 1.
- A6 writes A4's value to z. No other write to z can fall between A6 and A7, because B1 and A1 are already done and B8 comes after R. So A7 equals A4.
- A8 writes A7's value to y, and it is the only write to y. The final y is 6 or 1.

**x**
- B7 writes 4 and A2 writes 1. A2 has no constraint tying it to B5 through B7, so it can happen after B7.
- The final x is therefore 4, or 1 if A2 comes after B7.
- This choice is independent of the choice for y.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
END