Every A operation finishes before B8 starts, and B5–B7 also come before B8. The ordering constraints are:
- A1 ends before S, and B5 starts after S.
- B1 ends before P, and A2 starts after P.
- B2 ends before Q, A9 starts after Q and ends before R, and B8 starts after R.

**Value of v.**
- A4 runs after A2, so it runs after P and after B1.
- A1 also ends before A2 starts. So both z-writes of 1 (B1) and 6 (A1) happen before A4, in either order.
- Nothing else writes z before A4, because B8 comes after R. So A4 reads v, which is 1 or 6.
- A6 writes v to z, A7 reads v, and A8 writes v to y.
- A8 is the only writer of y, so the final y is v.
- A9 writes v to z.

**Final z and B9.**
- B8 is the last write to z, and it writes the value B2 read. So the final z is B2's value, and B9 reads that same value.
- B2 reads y, which is 0 unless A8 has already happened.
- B2 can read v only if A8 happens before B2, which is before B5. That is possible, since A9 only needs to start after Q.
- So B2 is either 0 or v.

**Final x.**
- If B2 = v, then A2 comes before B2 and so before B5–B7. The last write to x is then B7, so x = 4.
- If B2 = 0, A2 can happen after B7, which gives x = 1. Otherwise x = 4.

Cases:
- B2 = 0: B9 = 0, z = 0, x is 1 or 4, and y is 1 or 6.
- B2 = v: B9 = v, z = v, y = v, and x = 4.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END