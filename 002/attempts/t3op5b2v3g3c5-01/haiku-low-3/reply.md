Final x always equals the value B1 read, since B2 and B3 both write that value. The possible outcomes, with Q1 = A4, Q2 = C3, Q3 = final x:

- **B1 reads 0** (before any y-write): x stays 0, so C3 = 0 and final x = 0. A4 can be 0, 1, or 2.
- **B1 reads 1** (C5 is the last y-write before B1): C5 comes after C3 in program order, so C3 always reads 0. A3 must precede B2, and A4 can be 0, 1, or 2. Final x = 1.
- **B1 reads 2** (C2 is the last y-write before B1, and C5 comes after B1): C3 can read 0 or 2 independently of A4, which can be 0, 1, or 2. Final x = 2.

BEGIN
0 0 0
1 0 0
2 0 0
0 0 1
1 0 1
2 0 1
0 0 2
0 2 2
1 0 2
1 2 2
2 0 2
2 2 2
END