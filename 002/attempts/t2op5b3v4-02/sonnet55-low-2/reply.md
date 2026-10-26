Thread A's three reads of y happen in order, and y takes the values 0, then 4 (B3), then 2 (B4) over time. A3 and A4 therefore see a non-decreasing position in that sequence 0, 4, 2.

Possible (A3, A4) pairs: (0,0), (0,4), (0,2), (4,4), (4,2), (2,2).

B2 reads x, which is either 0 (B2 before A1 takes effect) or 3 (A1 before B2). The threads have no sync points, so either value of B2 can occur with any (A3, A4) pair:
- B2 = 3: run A1 first, then B1 and B2, and place A2 to A4 around B3 and B4 as needed.
- B2 = 0: run B1 and B2 before A1. A2 to A4 can then still see any part of the y sequence, because they can run before B3 or after B4 as the pair requires.

So all 6 × 2 = 12 combinations are possible.

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