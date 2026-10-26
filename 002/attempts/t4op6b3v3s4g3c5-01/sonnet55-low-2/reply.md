Q3 is fixed first, then the possible (A2, A3) pairs follow from the ordering constraints.

**Final value of x (Q3)**
- C5 ends before Q, D1 starts after Q, D1 ends before R, A5 ends after R, and A6 comes after A5. So C5's write to x takes effect before A6.
- C3 writes 1 to x before C5's write. A6 returned 0, so the last write to x before A6 must have written 0. That write is C5's, so C1 read y = 0. C1 therefore ran before B5's write of 2 to y.
- B2 and B4 come before B5, and C1 reads before B5, so B2 and B4 are written before C5's write. Their values are overwritten.
- D3 comes after D1, which is after C5's write. D3 must therefore take effect after A6, so that A6 still sees 0.
- D3 is then the last write to x, so the final value of x is 3.

**A2 and A3 (reads of z)**
- A1 read 0, so every write to z comes after A1.
- A2 ends before P. D5 starts after P, so A2 cannot see D5's write of 1. A4 and A5 come after A2 in thread A.
- A2 can therefore read 0, 3 (B1 or D2) or 2 (B3, after B1).
- A3 comes after A2 and before A4, so it can read:
  - 0, 3 or 2 if A2 read 0.
  - 1 (from D5, which can take effect once P has passed) if A2 read 0, 2 or 3.
  - 2 or 3 if A2 read 2. If A2 read 2, A3 cannot read 0, because B3's write of 2 is already in place. A3 can read 3 from D2, which comes after B5 and so after B3.
  - 2 or 3 if A2 read 3, again not 0. A3 reads 2 from B3 after B1.

All of these combinations are consistent with the other constraints.

BEGIN
0 0 3
0 1 3
0 2 3
0 3 3
2 1 3
2 2 3
2 3 3
3 1 3
3 2 3
3 3 3
END