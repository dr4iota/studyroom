Final y is always A's A8 value, which equals A4's read of z. B9 and the final z both equal B2's read of y.

**Ordering constraints**
- A1 ends before S, and B5 starts after S, so A1 comes before B5.
- B1 ends before P and A2 starts after P, so B1 comes before A2. A1 also comes before A2.
- B2 ends before Q and A9 starts after Q, so B2 comes before A9.
- A9 ends before R and B8 starts after R, so A9 comes before B8.

**A4 and A7**
- Before A4, z has been written by A1 (6) and B1 (1), in either order, and nothing else.
- A9 and B8 both come after A4, so A4 reads whichever of A1 and B1 wrote last. That gives v = 6 or v = 1.
- A6 rewrites z with v, and B8 comes after A9, so A7 also reads v.

**y**
- A8 writes v to y, and it is the only write to y. The final y is therefore v.
- B2 reads y before Q. It sees 0 if it precedes A8, or v if A8 has already happened. So B2 is 0 or v.

**z, B9 and x**
- B8 writes B2's value to z after A9, so the final z is B2's value.
- B9 follows B8, and nothing else writes z afterwards, so B9 equals B2's value.
- The writers of x are A2 (1) and B5, B6, B7 (B7 writes 4). A2 can fall after B7 or before it, so the final x is 1 or 4.
- If B2 = v, A8 precedes B2. Then A2 precedes A8, which precedes B2, B3, B5 and B7, so the final x is 4.
- If B2 = 0, both final values of x are possible.

**Combinations**
- B2 = 0 gives B9 = 0 and z = 0. Then x is 4 or 1, and y is 6 or 1.
- B2 = v gives x = 4, and B9, y and z all equal v, with v = 6 or 1.

BEGIN
0 4 6 0
0 1 6 0
0 4 1 0
0 1 1 0
6 4 6 6
1 4 1 1
END