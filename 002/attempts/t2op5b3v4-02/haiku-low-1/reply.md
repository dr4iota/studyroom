Only y-reads and the x-read at B2 matter. z is never written, so its reads always return 0.

- **y over time:** starts at 0, becomes 4 after B3, then 2 after B4. A3 and A4 come in program order, so their phases are nondecreasing. That allows six pairs: (0,0), (0,4), (0,2), (4,4), (4,2), (2,2).
- **x for B2:** B2 returns 3 if A1 took effect before B2, otherwise 0. Both are possible because B2 is only constrained to come before B3, and A1 is only constrained to come before A2.
- **Independence:** B2's value depends only on A1's position, and each y-phase pair can be arranged without conflicting with that choice. So all 6 × 2 = 12 combinations are achievable.

The asked values are Q1 = A3, Q2 = A4, Q3 = B2.

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