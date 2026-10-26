Everything in thread A happens after B1–B8 have finished, so only B9 can overlap with A.

**State after B1–B8**
- B2 reads y while it is still 0. A can't have written y yet, and B4 comes later. So B2 returns 0.
- B3 makes x = 4.
- B8 writes 0 to y, so y = 0.

**B9**
- B9 writes B2's value, which is 0, to x.
- It can take effect at any point after B8, before or during A's execution.
- Nothing else writes x after B3, so x is 4 until B9 and 0 from then on.

**Thread A**
- A1 reads y = 0, and A2 writes 0 to z.
- A3, A5, A6 and A8 are successive reads of x, so their values are non-increasing: some 4s, then 0s once B9 has taken effect.
- A4 writes A3's value to y. A4 comes after B8, so the final y equals A3's value.

**Cases**
- If A3 = 4, the final y is 4. The remaining reads (A5, A6, A8) can be 4 4 4, 4 4 0, 4 0 0 or 0 0 0, depending on when B9 lands.
- If A3 = 0, B9 has already taken effect. Then A5, A6 and A8 are all 0, and the final y is 0.

BEGIN
4 4 4 4
4 4 0 4
4 0 0 4
0 0 0 4
0 0 0 0
END