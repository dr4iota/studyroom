Each thread's operations take effect in program order, and no sync points constrain the threads further. Every execution is therefore an interleaving of the two threads' operations.

**A5 (Q1).** The only write to z is B4, which writes 1. A5 returns 0 if it takes effect before B4, and 1 if it takes effect after B4. B5 always returns 1, since B4 precedes it, so that known result excludes nothing.

**B1 and B2 (Q2, Q3).** Both reads precede B3, because B3 comes after them in thread B. Before B3 takes effect, the only writes to y are A2 (writes 1) and then A3 (writes 3). So y goes 0, then 1, then 3, and B1 ≤ B2 in time means the pair must be non-decreasing along that progression. The possible pairs are (0,0), (0,1), (0,3), (1,1), (1,3) and (3,3).

**Combining.**
- **A5 = 0:** Place B1 and B2 wherever the pair needs. Then run the rest of A (A2 to A4, then A5), and only afterwards B3 and B4. This works for every pair, including (3,3), where A3 is placed before B1.
- **A5 = 1:** Run all of B up to B4 with B1 and B2 reading the chosen pair, then run A5 last. A's writes to y can be interleaved before B3 as needed. This also works for every pair.

All 2 × 6 = 12 combinations are possible.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 1
0 1 3
0 3 3
1 0 0
1 0 1
1 0 3
1 1 1
1 1 3
1 3 3
END