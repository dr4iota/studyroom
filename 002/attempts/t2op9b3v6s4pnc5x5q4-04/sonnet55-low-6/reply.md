Every combination has B9 = 0 and final z = 0. Final x is 1 or 4, and final y is 1 or 6.

**Q1 (B9) and Q4 (final z).**
- Only A8 writes y, and A8 starts after Q. B2 ends before Q, so B2 reads y = 0.
- B8 starts after R, and A9 ends before R, so B8 comes after every A operation. B8 writes 0 to z.
- Only B1 and A1 write z before B8. B9 comes after B8, and the only z-writes after R are B8's, so B9 reads 0 and the final z is 0.

**Q2 (final x).**
- B7 writes 4 and is the last write in B. A2 writes 1 and has no ordering relative to B5–B7. P and S are independent, so A2 can come after B7.
- If B7 is last, x = 4. If A2 comes after B7, x = 1. B6 writes an earlier value, so it never decides the final x.

**Q3 (final y).**
- A8 is the only write to y, and it writes the value A7 read.
- A1 and B1 are the only writes to z before A4. Both end before A4: A1 precedes A2, and B1 ends before P, which precedes A2. Their order is free.
- A4 reads whichever of A1 and B1 came last. A6 writes that value to z, and A7 reads it back, because B8 is the only other z-write after B1 and it comes after all of A.
- If B1 comes after A1, y = 1. If A1 comes after B1, y = 6.

All four combinations of x ∈ {4, 1} and y ∈ {1, 6} are consistent with the constraints.

BEGIN
0 4 1 0
0 4 6 0
0 1 1 0
0 1 6 0
END