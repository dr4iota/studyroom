**Fixed by the ordering rules**

- **B3 returns 0.** Thread B's steps before the S line come before S, so B4 < S. Thread A's steps after the S line come after S, so S < A2. Together that gives B3 < B4 < S < A2. Every write to x (A2, B5, B6, B7) takes effect after B3, so B3 reads 0. B6 therefore writes 0.
- **B2 returns 0.** The only write to y is A8, which comes after A2. A2 comes after B4, which comes after B2. So no write to y happens before B2, and B6… likewise B8 writes 0.
- **B9 returns 0 and final z is 0.** All of thread A comes before R, and B8 comes after R. So B8 is the last write to z, and B9 reads the 0 it wrote.

**What can vary**

- **Final x is 1 or 4.** B5, B6 and B7 write 3, 0 and 4 in that order. A2 writes 1, and it may take effect before or after B7, since both only need to lie between S and R.
- **Final y is 1 or 6.** A4 reads z after both A1 (writes 6) and B1 (writes 1). A1 and B1 may take effect in either order, so A4 returns 6 or 1. No other write to z can land between A6 and A7, so A7 returns the same value as A4. A8 writes that value to y.

The two varying values are independent, giving four combinations.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
END