Final y always equals A1's value, and B6 and B7 can only return 0, 1, 2 or 3. Below, a is A1's value and c is C1's value.

**What A1 and C1 can read.** Only B2 and B4 can write x before P, so A1 and C1 each return 0 or 1.
- B2 writes 1.
- B3 runs before P, but A3 runs after P. So B3 reads 1, or 0 from B4 echoing an earlier 0, and B4 writes that back.

**Final y.** A5 writes a to y after R. Every other write to y happens before R:
- C6 is before R.
- A4 is before Q, and Q is before R.

So A5 is the last write to y, and the final y is a.

**C7 returns 0.** C7 runs after C5, which writes 3. So a write of 0 must take effect after C5 and before C7. Only two writes can do that:
- C6, which writes c. C6 is before R, and C7 may also be before R.
- A5, which writes a. This needs C7 to fall after R.

So a = 0 or c = 0. This rules out a = 1 together with c = 1.

**B6 and B7.** Both reads happen after B5 (writes 2) and before P. The writes to y that can land in that window are:
- B5 writes 2.
- C2 writes c.
- C3 writes 3, then C5 writes 3. C5 can take effect before P.

C2, C3 and C5 come in that order, and no other write of 2 can come after B5. So the possible (B6, B7) pairs are:
- (2,2), (2,c), (2,3), (c,c), (c,3), (3,3).

These are impossible:
- (c,2): no second write of 2 exists.
- (3,2): same reason.
- (3,c): C2 comes before C3, and B1's 3 is overwritten by B5.

**A2 and C4 return 3.** A2 can read B1's 3 before B5 takes effect. C4 can read C3's 3. So both known results fit every case above.

**Combining.**
- Pairs that do not involve c work with any allowed (a, c), so the final y can be 0 or 1.
- Pairs with c = 0 work with a = 0 or a = 1.
- Pairs with c = 1 force a = 0, so the final y is 0.

BEGIN
2 2 0
2 2 1
2 3 0
2 3 1
3 3 0
3 3 1
2 0 0
2 0 1
0 0 0
0 0 1
0 3 0
0 3 1
2 1 0
1 1 0
1 3 0
END