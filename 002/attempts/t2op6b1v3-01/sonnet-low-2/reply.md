Because A5 comes after A4 in thread A, reads A1–A4 can only see values written by thread B. Those writes land in the order 1, 2, 3, 1 (B2, B3, B4, B5). So the value of x over time runs 0, 1, 2, 3, 1.

**A2 and A4.** A2 takes effect before A4, so their values come from positions i ≤ j in the sequence 0, 1, 2, 3, 1. This gives these (A2, A4) pairs: 00, 01, 02, 03, 11, 12, 13, 22, 23, 21, 33, 31.

**B1.** B1 takes effect before B2, so it can only see 0 or A5's write of 1.
- B1 = 0 is possible with every pair above. B1 can take effect early, and A's reads can fall anywhere later.
- B1 = 1 needs A5 to take effect before B1, and so before B2. That forces A1–A4 to run before any write by B, so A2 = 0 and A4 = 0. Only (0, 0, 1) is possible.

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 2 0
2 3 0
2 1 0
3 3 0
3 1 0
0 0 1
END