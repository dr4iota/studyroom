Every outcome has final x = 3, and A2 can be 0, 2 or 3.

**Final value of x (Q3).** A6 returns 0 and takes effect after R. R is after D1, which is after Q, which is after C5 ends. So C5 has already written before A6, and the last write to x before A6 must be C5's write of 0.

- C5 writes the value C1 read, so C1 read y = 0 and C5 wrote 0.
- D1 returned 2, so B5 (write 2 to y) happened before D1, which is before R and before A6. B2 and B4 come before B5, so they happened before A6. They must therefore have taken effect before C5's write, or x would not read 0 at A6.
- D3 comes after D1, so it can take effect after A6, and it does. It is the last write to x, so the final x is always 3.

**A2 (Q1).** A2 ends before P, and A1 read 0, so no z write precedes A1.

- A2 can read 0.
- A2 can read 3 from B1 or from D2. D2 can come before P because only D5 must start after P.
- A2 can read 2 from B3.
- A2 cannot read 1. A4 comes after A2, and D5 starts after P, which is after A2.

**A3 (Q2).** A3 comes after A2 and before A4, so it can read 0, 3, 2 or 1.

- 3 comes from B1 or D2, 2 from B3, and 1 from D5 (which can take effect after P).
- A3 = 0 requires A2 = 0, because once a z write has happened z is never 0 again.
- Every other pairing is achievable. For example, A2 = 2 and A3 = 3 works with B3 and then D2, and A2 = 3 and A3 = 2 works with B1 then B3.

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