All 12 combinations are possible. The only writes to y are B3 (4) then B4 (2), so y goes 0, then 4, then 2 over time. A2, A3 and A4 read y in that order, so their values can never go backwards through that sequence. The possible (A3, A4) pairs are therefore (0,0), (0,4), (0,2), (4,4), (4,2) and (2,2).

B2 reads x, which is either 0 or 3.

- **B2 = 0:** B2 takes effect before A1, and B3 and B4 come after B2. A2 to A4 all come after A1. Every (A3, A4) pair above is still achievable by placing B3 and B4 around the A reads.
- **B2 = 3:** A1 takes effect before B2, and B3 and B4 come after B2. The A reads can fall before, between or after B3 and B4, so every pair is again achievable.

BEGIN
0 0 0
0 4 0
0 2 0
4 4 0
4 2 0
2 2 0
0 0 3
0 4 3
0 2 3
4 4 3
4 2 3
2 2 3
END