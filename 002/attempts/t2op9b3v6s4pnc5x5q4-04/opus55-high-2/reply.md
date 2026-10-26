**Ordering constraints from the sync points**
- A1 < S < B5, so A1 comes before B5.
- B1 < P < A3, so B1 comes before A3.
- B2 < Q < A9, so B2 comes before A9.
- A9 < R < B8, so all of thread A comes before B8.

**Values of z**
- A4 reads z after A1 (program order) and after B1 (since B1 < A3). The only z writes that can come before A4 are A1 (6) and B1 (1). B8 comes later.
  - If B1 is before A1, A4 returns 6.
  - If A1 is before B1, A4 returns 1.
- A6 writes the A4 value to z. A6 comes after both A1 and B1. So A7 returns the same value as A4, call it v.
- B8 is the last write to z. B9 comes after B8. So B9 returns the B2 value, and the final z equals the B2 value.

**Value of y**
- The only write to y is A8, which writes v. So the final y is v.
- B2 returns either 0 (if it comes before A8) or v (if it comes after A8). Both are allowed, because B2 only needs to come before A9.

**Value of x**
- B7 writes 4 last in thread B.
- A2 (x=1) can come after B7, because nothing forces A2 earlier than B5. In that case the final x is 1. Otherwise it is 4.
- If B2 returned v, then A2 < A8 < B2 < B7. So A2 is before B7, and the final x must be 4.
- If B2 returned 0, both final values of x are possible. Example orders:
  - B1, A1, B2–B7, A2, A3–A9, B8, B9 gives v = 6 and final x = 1.
  - A1, B1, B2–B7, A2, … gives v = 1 and final x = 1.

**Possible combinations** (Q1, Q2, Q3, Q4):
- v = 1: (0, 4, 1, 0), (0, 1, 1, 0), (1, 4, 1, 1)
- v = 6: (0, 4, 6, 0), (0, 1, 6, 0), (6, 4, 6, 6)

BEGIN
0 4 1 0
0 1 1 0
1 4 1 1
0 4 6 0
0 1 6 0
6 4 6 6
END