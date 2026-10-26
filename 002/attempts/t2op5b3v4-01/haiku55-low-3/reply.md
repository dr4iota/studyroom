Every possible outcome comes from one of the 252 interleavings of A's five operations with B's five, since no sync points constrain them. Each interleaving reduces to these facts:

- **Q1 (A1's read):** It sees the last z-write from B before it. Let k be the number of B operations before A1. Then k=0 gives 0, k=1 or 2 gives 3, k=3 or 4 gives 2, and k=5 gives 1.
- **Q2 (B4's read):** It sees B3's write of 2 unless an A z-write falls between B3 and B4. The last such A write is 3 (A3), 4 (A4), or 2 (A5), so Q2 is 2, 3, or 4.
- **Q3 (final z):** The last z-write is A5 (2) or B5 (1), whichever comes later. It is 1 only if all of A precedes B5, and 2 otherwise.

Checking which combinations each interleaving can realize gives 19 outcomes. For example, B1, B2, B3, A1, A2, A3, A4, B4, A5, B5 yields (2, 4, 1). Q1 is 1 only when all of B precedes A, which forces Q2=2 and Q3=2.

Outcomes as (Q1, Q2, Q3):

BEGIN
0 2 1
0 2 2
0 3 1
0 3 2
0 4 1
0 4 2
1 2 2
2 2 1
2 2 2
2 3 1
2 3 2
2 4 1
2 4 2
3 2 1
3 2 2
3 3 1
3 3 2
3 4 1
3 4 2
END