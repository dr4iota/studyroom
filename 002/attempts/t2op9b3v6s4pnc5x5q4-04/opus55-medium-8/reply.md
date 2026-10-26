Of the 8 possible combinations of the four values, 6 can occur. The reasoning traces which write each read sees, then checks which choices can happen together.

**Ordering facts from the sync points**
- B1 happens before P, and P happens before A3.
- B2 happens before Q, and Q happens before A9.
- A1 happens before S, and S happens before B5.
- All of A1–A9 happen before R, and R happens before B8.

**Reads of z by Thread A (A4 and A7)**
- Both A1 and B1 take effect before A4, and they are the only earlier writes to z.
- So A4 returns 6 if B1 came before A1, or 1 if A1 came before B1. Either order is allowed. Call this value v, so v is 6 or 1.
- A6 writes v to z, and nothing else writes z between A6 and A7. So A7 returns v.
- A8 then writes v to y. No other write touches y, so the final y is v.

**B2 (read y)**
- B2 returns 0 if it runs before A8, or v if it runs after A8.
- Running after A8 is allowed, because A8 has no sync constraint relative to Q.

**B8, B9 and the final z**
- B8 runs after every step of Thread A, so it is the last write to z.
- So B9 returns B2's value, and the final z equals B2's value.

**Final x**
- The writes to x are A2 (1), B5 (3), B6 and B7 (4).
- B7 always comes after B5 and B6, so the final x is 4, unless A2 takes effect after B7, which makes it 1.
- A2 after B7 is allowed: A1, S, B5, B6, B7, A2 is a valid order.
- However, if B2 returns v, then A2 happens before A8, A8 before B2, and B2 before B7. So A2 is before B7 and the final x must be 4.

**Combinations (B9, x, y, z)**
- When B2 returns 0, the final x can be 1 or 4, with v equal to 6 or 1.
- When B2 returns v, the final x is 4.

BEGIN
0 1 6 0
0 4 6 0
6 4 6 6
0 1 1 0
0 4 1 0
1 4 1 1
END