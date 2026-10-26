**Constraints from the sync points**

Each sync point links one thread's earlier steps to the other thread's later steps:
- B1 < P < A3, so B1 takes effect before A3.
- B2 < Q < A9, so B2 takes effect before A9.
- A1 < S < B5, so A1 takes effect before B5.
- A9 < R < B8, so all of thread A takes effect before B8 and B9.

**z and B9**
- B8 writes B2's value to z. Every z-write by thread A happens before R, which is before B8.
- So B9 returns B2's value, and the final z equals B2's value.

**A4, A7 and y**
- A4 comes after A1 (6 to z) and after B1 (1 to z, since B1 < P < A3 < A4). So A4 returns 6 or 1, depending on which of A1 and B1 took effect later. Call this value v.
- A6 writes v to z. No other write to z can take effect between A6 and A7, so A7 returns v.
- A8 is the only write to y, so the final y is v (6 or 1).

**B2**
- B2 reads y, which is written only by A8.
- B2 returns 0 if it takes effect before A8.
- It returns v if A8 < B2. This is allowed because B2 only has to come before Q, which is before A9.

**Final x**
- The last write to x is either B7 (4) or A2 (1).
- A2 can come after B7. A2 has no lower bound from B, and B5..B7 only need to come after S, which comes after A1.
- If B2 returned v, then A2 < A8 < B2 < B5..B7, so the final x must be 4.
- If B2 returned 0, the order B2 < B5 < B6 < B7 < A2 < A8 works, so the final x can be 1 or 4.

**Combinations** (B9, final x, final y, final z):
- B2 = 0: x is 1 or 4, and y is 1 or 6. This gives four combinations.
- B2 = v: x is 4, and the result is 1 4 1 1 or 6 4 6 6.

BEGIN
0 4 1 0
0 1 1 0
0 4 6 0
0 1 6 0
1 4 1 1
6 4 6 6
END