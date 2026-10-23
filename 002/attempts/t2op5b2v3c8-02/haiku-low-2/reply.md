Each thread's operations take effect in program order, and any interleaving of the two threads is allowed. The only writes to x are B1 (1), B2 (3), and A4 (the value A1 read). Let r1 be A1's result, which is 0, 1, or 3 depending on how many B writes precede A1.

- **B3** always comes after B2, so it reads either 3 (B2 is the latest write) or r1 (A4 landed between B2 and B3). It can never read 1 unless r1 = 1.
- **B4** reads the same as B3, unless A4 lands between B3 and B4, in which case it reads r1 while B3 reads 3.
- **A3** reads whatever the B writes have left in x at that point, so it can be 0, 1, or 3.

Enumerating the placements of A1, A3, and A4 among B1 through B4 gives these 13 combinations of (A3, B3, B4):

BEGIN
0 0 0
0 3 0
0 3 3
1 0 0
1 1 1
1 3 0
1 3 1
1 3 3
3 0 0
3 1 1
3 3 0
3 3 1
3 3 3
END