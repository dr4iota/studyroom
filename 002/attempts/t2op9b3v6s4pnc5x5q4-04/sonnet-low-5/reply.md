Of the four sync points, only the orderings the rules force matter here, and they pin down almost everything.

**Ordering constraints**
- B8 and B9 start after R, and R comes after A9 ends. So all of thread A finishes before B8 and B9.
- B5 to B7 come before B8 by program order, so they also finish before B8.

**z and y**
- A1 and B1 are the only writers of z before A4 reads it. Both come before A3, so A4 reads v ∈ {6, 1}, depending on which of A1 and B1 came last.
- A6 writes v to z, A7 reads v, and A8 writes v to y. A9 writes v to z.
- B never writes y, so the final y is v.
- B2 reads y before Q. It sees 0, or v if A8 has already happened. A8 can precede B2 because Q is not constrained to come after A8.
- B8 writes B2's value to z. B9 reads it straight back, since nothing else writes z by then. So B9 equals B2's value, and the final z equals B2's value.

**x**
- B7 writes 4, and A2 writes 1. The final x is 4, or 1 if A2 comes after B7.
- If A2 comes after B7, then B2 comes before A2, because B2 precedes B7 in thread B. A8 comes after A2, so A8 is after B2. That forces B2 = 0.
- If x = 4, B2 can be 0 or v.

**Combinations (B9, x, y, z)**
- x = 4, B2 = 0: v = 1 gives (0, 4, 1, 0), and v = 6 gives (0, 4, 6, 0).
- x = 4, B2 = v: (1, 4, 1, 1) and (6, 4, 6, 6).
- x = 1, B2 = 0: (0, 1, 1, 0) and (0, 1, 6, 0).

BEGIN
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
0 1 1 0
0 1 6 0
END

Each line gives B9, final x, final y, final z. In the block above, x comes second in the Q1 to Q4 order, so each line is Q1 Q2 Q3 Q4 as asked.