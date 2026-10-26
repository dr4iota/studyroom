Only B1 writes y, and it writes 4. A3 returned 4, so B1 takes effect before A3. A1 comes before A3, so it can read 0 (A1 before B1) or 4 (B1 before A1). Both are possible, since B1 only has to precede A3.

For z, B5 writes after B2 and B3, so it cannot affect their results. The writes A2 (3) and A4 (4) happen in that order, so z holds 0, then 3, then 4. B2 and B3 read in order, so B3's value is never earlier in that sequence than B2's. The possible pairs are (0,0), (0,3), (0,4), (3,3), (3,4) and (4,4).

The ordering constraints are B1 < A3, A1 < A2 < A3 < A4 and B1 < B2 < B3. Each pair is achievable with either value of A1:
- If A1 reads 0, then A1 < B1 < A3. B2 and B3 can be placed anywhere relative to A2 and A4, as long as they come after B1.
- If A1 reads 4, then B1 < A1 < A2. B2 and B3 are again free relative to A2 and A4, as long as they come after B1.

That gives 2 × 6 = 12 combinations.

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END