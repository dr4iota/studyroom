I found 17 possible combinations of (Q1, Q2, Q3), listed in the block below.

Key constraints:
- **A1 returns 0**, so no z-write precedes A1. A6 returns 0, which forces the last x-write before A6 to write 0. The only 0-writer that can land after C3 is C5, so C1 must read 0 (B5 comes after C1), and C5 must take effect between S and A6.
- **Final x** is 0 (C5 is last) or 3 (D3 is last, after A6). It cannot be 1 (C3 precedes C5) or 2 (B4 always follows B2).
- **A2** can see B1 and B3, so it can be 0, 2, or 3.
- **A3** can also see D2 (3) and D5 (1). The value 1 requires D5 to land before A3, which places A3 after Q and rules out Q3=3. The value 0 forces A2 to be 0.

BEGIN
0 0 0
0 0 3
0 1 0
2 1 0
3 1 0
0 2 0
0 2 3
2 2 0
2 2 3
3 2 0
3 2 3
0 3 0
0 3 3
2 3 0
2 3 3
3 3 0
3 3 3
END