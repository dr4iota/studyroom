Every possible outcome (B9, final x, final y, final z) is one of these six: (0, 1, 1, 0), (0, 1, 6, 0), (0, 4, 1, 0), (0, 4, 6, 0), (1, 4, 1, 1), (6, 4, 6, 6).

**Ordering constraints from the sync points**
- B1 happens before P, and P before A2. So B1 < A2 < A3 < … < A9.
- A1 happens before S, and S before B5. So A1 < B5 < B6 < B7.
- B1 and B2 happen before Q, and Q before A9. So B2 < A9.
- A1 through A9 happen before R, and R before B8. So A9 < B8 < B9.

**Final z and B9**
- B8 is the last write to z, because it comes after A9 and every other write to z.
- Nothing writes z between B8 and B9. So B9 = final z = the value B2 read from y.

**Final y**
- Only A8 writes y, so final y equals what A7 read.
- B1 and A1 both take effect before A4. The only other writes to z (A9 and B8) come after A7.
- So A4 reads 6 if B1 came before A1, or 1 if A1 came before B1. Either order is allowed.
- A6 writes that value to z, and A7 reads it back. So final y is 6 or 1 and equals A4's value.

**What B2 reads**
- B2 reads 0 if it happens before A8.
- B2 reads A8's value (equal to A4's) if it happens after A8. This is allowed because A8 has no tie to Q, and only A9 must come after Q.

**Final x**
- The writes to x are A2 (1), B5 (3), B6 and B7 (4). B6 is always overwritten by the later B7, so B3's value never matters.
- If B7 happens before A2, the final x is 1. This is possible: A1 < S < B5 < B6 < B7 < A2, with P placed after B1 and before A2.
- Otherwise the final x is 4.

**How the choices interact**
- Final x = 1 needs B2 < B7 < A2 < A8, so B2 must read 0.
- If B2 reads A4's value, then B2 comes after A8, which comes after A2. B7 then comes after A2, so the final x is 4.
- All other combinations are independent of each other.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END