**Ordering constraints from the sync points:**
- B1 < P < A3, so B1 comes before A3 through A9.
- B2 < Q < A9.
- A1 < S < B5, so A1 comes before B5, B6 and B7.
- A9 < R < B8, so all of thread A finishes before B8 and B9.

**Values of z and y:**
- A4 reads z. The only writes that can come before it are A1 (6) and B1 (1). Both happen before A4, in either order. So A4 returns 1 or 6.
- B8 comes after R, so no other thread can write z between A6 and A7. Therefore A7 returns A4's value, and A8 writes that value to y.
- A8 is the only write to y, so the final y equals A4's value: 1 or 6.
- B2 runs before Q, and A8 also runs before Q, in either order. So B2 returns 0 or A4's value.
- B8 writes B2's value to z after all of thread A is done. Nothing writes z after B8, so B9 returns that value and it is also the final z.

**Final x:**
- B5, B6 and B7 run in that order, so B7 (4) is the last write to x unless A2 (1) comes after B7.
- A2 can come after B7 because nothing forces it earlier: B5–B7 only need to follow S, and S only needs to follow A1.
- If B2 returned A8's value, then A2 < A8 < B2 < B7, so the final x must be 4.
- If B2 returned 0, the final x can be 1 or 4. For example, A1, B1, B2…B7, A2, … works, as does the order with B1 before A1.

So the final y is 1 or 6, and B9 equals the final z. If B9 is 0, the final x is 1 or 4; if B9 equals y, the final x is 4.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END