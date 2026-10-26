Only thread A can write y, and only thread B can write z after the sync constraints settle. This leaves four independent choices to work through.

**Ordering constraints.**
- A1 < S < B5.
- B1 < P < A3.
- B2 < Q < A9 < R < B8.

**A4, A7 and A8.**
- A4 reads z after P, so B1 has already happened. A1 has also happened, because it precedes A2 and A3.
- Nothing else can write z before A4. The remaining writers are A6, A9 and B8, and all of them come after A4. So A4 returns v, where v is 6 or 1 depending on whether B1 or A1 wrote z last.
- A6 rewrites v to z. A7 reads z and gets v. A8 writes v to y.
- So the final y is v, which is 6 or 1.

**B2, B8 and B9 (Q1, Q4).**
- B2 reads y before Q. A8 may or may not have happened by then, so B2 returns 0 or v.
- Every write to z by thread A, ending with A9, comes before R and so before B8. B8 then writes B2's value to z.
- B9 reads z right after B8, so B9 returns B2's value. The final z is the same value.

**Final x (Q2).**
- The last write by B is B7 (value 4), and thread A writes x only in A2 (value 1).
- B7 has no constraint relative to R, so A2 can fall either before or after B7. The final x is therefore 4 or 1, independent of the other values.

Combinations (B9, final x, final y, final z):

BEGIN
0 1 6 0
0 4 6 0
6 1 6 6
6 4 6 6
0 1 1 0
0 4 1 0
1 1 1 1
1 4 1 1
END