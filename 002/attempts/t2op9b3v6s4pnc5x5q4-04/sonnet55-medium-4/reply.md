Only some of the orderings the rules allow can actually occur. The reasoning below fixes each value in turn.

**Constraints that fix the order**
- B1 ends before P and A2 starts after P, so B1 finishes before A2. Every B write to z (B1) therefore happens before A4 reads z.
- A9 ends before R and B8 starts after R, so A9 comes before B8. The only write to z after A9 is B8.
- Only A1 and B1 write z before A4. So A4 returns 6 or 1, depending on which write is later. Call that value v.

**Values of y and z**
- A6 writes v to z, so A7 reads v and A8 writes v to y. A9 writes v to z.
- y is written only by A8, so the final y is v, which is 6 or 1.
- A5 runs before A8, so it reads 0. It does not affect the answer.
- B2 can read y before A8 (returns 0) or after A8 (returns v). Call B2's value r, so r is 0 or v.
- B8 writes r to z after everything else on z. So B9 reads r, and the final z is r.

**Final value of x**
- A2 writes 1, B5 writes 3, B6 writes B3's value, and B7 writes 4. B7 is the last B write to x.
- A2 can come after B7, which makes the final x equal to 1. That requires B2 to read y before A8, because A8 comes after A2. So r = 0.
- Otherwise B7 is last and the final x is 4. This works with either r = 0 or r = v. For r = v, A2 and A8 happen before B2 and B7.

The final x is always 1 or 4, never 3.

**Combinations**
- r = 0: B9 = 0 and z = 0, with x = 1 or 4 and y = 6 or 1.
- r = v: B9 = v and z = v, with x = 4 and y = v.

BEGIN
0 1 6 0
0 4 6 0
6 4 6 6
0 1 1 0
0 4 1 0
1 4 1 1
END