I found 17 possible outcomes for (Q1, Q2, Q3). The key constraints:

- **y and C1:** D1 reads y = 2, so B5 takes effect before D1. Since A6 must read x = 0 after R, and B2 and B4 write nonzero values to x before B5, the only way A6 can see 0 is for C1 to read 0. So C1 reads 0, and C2/C5 write 0 to x.
- **x and A6:** C3 (writes 1 to x) always precedes A6, so C5 (writes 0) must be the last write to x before A6. That forces D3 to be either before C5 (final x = 0) or after A6 (final x = 3). No other final value is possible.
- **z and A2/A3:** Only B1 (3), B3 (2), D2 (3), and D5 (1) can be visible to A2 or A3. D5 comes after D3 in thread D, so D5 can only be before A3 when D3 is before A3. That excludes final x = 3 with A3 reading 1, and excludes A2 or A3 reading 0 when a z-write precedes them.

Combining these, the feasible outcomes are the 17 below.

BEGIN
0 0 0
0 0 3
0 1 0
0 2 0
0 2 3
0 3 0
0 3 3
2 1 0
2 2 0
2 2 3
2 3 0
2 3 3
3 1 0
3 2 0
3 2 3
3 3 0
3 3 3
END