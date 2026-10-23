Every thread's operations take effect in program order, so the outcome depends only on a few values.

**Reads of z and the value written to y**
- A4 reads z after B1 has written 1, because B1 ends before P and A2 starts after P. So A4 is never 0.
- A1 and B1 can be in either order, so A4 returns 6 or 1. Call this value v.
- A6 writes v to z. Nothing else writes z before A7 reads it, since B8 comes after R and R comes after A9. So A7 returns v.
- A8 writes v to y, and y is written only by A8. The final y is therefore v, which is 6 or 1.

**B2 and the final z**
- B2 reads y before Q. A8 may or may not have taken effect by then, so B2 returns 0 or v.
- A9 writes v to z before R. B8 writes B2's value to z after R, and nothing writes z after that.
- So B9 returns B2's value, and the final z equals B2's value too.

**Final x**
- B5, B6 and B7 all start after S, and B7 writes 4. The only other write to x is A2, which writes 1.
- If A2 takes effect after B7, the final x is 1. Otherwise it is 4.
- If B2 returned v, then A8 took effect before B2. A2 came before A8, and B7 comes after B2, so B7 is last and x is 4.
- If B2 returned 0, either order of A2 and B7 is possible, so x is 1 or 4.

**Combinations (Q1 Q2 Q3 Q4)**
- B2 = 0: Q1 = 0, Q4 = 0, Q2 ∈ {1, 4}, Q3 ∈ {6, 1}.
- B2 = v: Q2 = 4, and Q1 = Q3 = Q4 = v with v ∈ {6, 1}.

BEGIN
0 1 6 0
0 4 6 0
0 1 1 0
0 4 1 0
6 4 6 6
1 4 1 1
END