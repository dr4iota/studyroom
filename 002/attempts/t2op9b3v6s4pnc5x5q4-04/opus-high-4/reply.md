**Constraints from the sync points**

- B1 happens before P, and P is before A3. So B1 comes before A3.
- B1 and B2 happen before Q, and Q is before A9. So B2 comes before A9.
- A1 happens before S, and S is before B5. So A1 comes before B5.
- A1 to A9 all happen before R, and R is before B8. So B8 and B9 come after every operation of A.

**Final z and B9**

The writes to z are A1, B1, A6, A9 and B8. B8 comes after all of A's operations, so B8 is the last write to z. B9 reads z right after B8, so B9 returns B8's value. Therefore B9 = final z = the value read by B2.

**Final y**

The only write to y is A8. A8 writes the value read by A7.

- Between A6 and A7, no other write to z can take effect. B1 and A1 are already done, and B8 comes later. So A7 returns what A6 wrote, which is the value A4 read.
- A4 comes after both A1 (6) and B1 (1). These two can take effect in either order, so A4 returns 6 or 1.

So final y is 6 or 1.

**B2**

B2 reads y, and the only write to y is A8. Both B2 and A8 come before Q, in either order.

- If B2 comes before A8, B2 returns 0.
- If B2 comes after A8, B2 returns A4's value, which is 1 or 6, and that equals final y.

**Final x**

The writes to x are A2 (1), B5 (3), B6 (B3's value) and B7 (4).

- Normally B7 is the last write, so final x is 4.
- A2 can take effect after B7: the order B7 < A2 < A3 < … < A9 < R < B8 breaks no constraint. Then final x is 1.
- In that case B2 comes before B7, which comes before A2 and A8. So B2 returns 0.

**Combinations**

- B2 = 0: z = 0 and B9 = 0. Final y is 1 or 6, and final x is 1 or 4. That gives four outcomes.
- B2 = final y (1 or 6): A8 must come before B2, so A2 cannot follow B7. Final x is 4, and z = B9 = final y. That gives two outcomes.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END