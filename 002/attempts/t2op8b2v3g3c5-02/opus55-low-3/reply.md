**Setup.** A1 must return 0. The only writes to x are A3 and A6, and both come after A1 in thread A. So A3 and A6 each write 0, and A5 writes 0 to y.

**Ordering facts.**
- A2 returns 2, so B4 (or B7 copying B5's value of 2) takes effect before A2.
- That gives B3 < B4 < A2 < A4 < A5 < A7.
- Within thread B, B4 < B5 < B6 < B7.
- On y, A4 writes 3 and then A5 writes 0.

Let r0 be the time before A4, r1 the time between A4 and A5, and r2 the time after A5. A read in r0 sees 2, in r1 sees 3, and in r2 sees 0, unless B7 has written in between.

**Rules for the three answers.**
- **Q1 (A7):** A7 returns B5's value if B7 takes effect between A5 and A7. Otherwise A7 returns 0.
- **Q3 (final y):** final y is B5's value if B7 takes effect after A5. Otherwise it is 0.
- **Q2 (B6):** B6 is determined by its region, because B7 comes after B6.

**Cases.**

| B5 (value) | B6 (value) | Where B7 takes effect | Result (Q1 Q2 Q3) |
|---|---|---|---|
| r0 (2) | r0 (2) | r0 or r1 | 0 2 0 |
| r0 (2) | r0 (2) | r2, before A7 | 2 2 2 |
| r0 (2) | r0 (2) | r2, after A7 | 0 2 2 |
| r0 (2) | r1 (3) | r1 | 0 3 0 |
| r0 (2) | r1 (3) | r2, before A7 | 2 3 2 |
| r0 (2) | r1 (3) | r2, after A7 | 0 3 2 |
| r0 (2) | r2 (0) | r2, before A7 | 2 0 2 |
| r0 (2) | r2 (0) | r2, after A7 | 0 0 2 |
| r1 (3) | r1 (3) | r1 | 0 3 0 |
| r1 (3) | r1 (3) | r2, before A7 | 3 3 3 |
| r1 (3) | r1 (3) | r2, after A7 | 0 3 3 |
| r1 (3) | r2 (0) | r2, before A7 | 3 0 3 |
| r1 (3) | r2 (0) | r2, after A7 | 0 0 3 |
| r2 (0) | r2 (0) | r2 (writes 0) | 0 0 0 |

Removing the duplicate "0 3 0" leaves 13 combinations.

BEGIN
0 2 0
2 2 2
0 2 2
0 3 0
2 3 2
0 3 2
2 0 2
0 0 2
3 3 3
0 3 3
3 0 3
0 0 3
0 0 0
END