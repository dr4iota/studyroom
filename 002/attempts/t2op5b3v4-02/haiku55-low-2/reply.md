Each thread's operations take effect in program order, and every read sees the latest write that took effect before it. Since y is written only by B3 (value 4) and then B4 (value 2), y's value over time goes 0, then 4, then 2. A3 and A4 are in order, so their phases never decrease. That gives six possible (A3, A4) pairs: (0,0), (0,4), (0,2), (4,4), (4,2), (2,2).

x is written only by A1 (value 3), and B2 precedes B3, so B2 returns 3 if A1 takes effect before B2, and 0 otherwise. Both cases can be combined with any of the six pairs, because A's reads can be placed before or after B2 without breaking any ordering. That gives 6 × 2 = 12 combinations.

Values are listed as Q1 (A3), Q2 (A4), Q3 (B2).

BEGIN
0 0 0
0 0 3
0 4 0
0 4 3
0 2 0
0 2 3
4 4 0
4 4 3
4 2 0
4 2 3
2 2 0
2 2 3
END