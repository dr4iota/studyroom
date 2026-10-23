Six outcomes are possible: B9 and the final z both equal whatever B2 read (0 or v), final y is v (6 or 1), and final x is 1 only when B2 read 0.

**Ordering constraints from the sync points**
- B1 < P < A3, so B1 and A1 both take effect before A4. (A1 < A2 < A3.)
- B2 < Q < A9.
- A1 < S < B5.
- All of thread A (through A9) < R < B8, so B8 and B9 come after every write by A.

**z and y**
- A4 reads z after both A1 (writes 6) and B1 (writes 1). So A4 returns v = 6 if B1 took effect before A1, and v = 1 if A1 took effect before B1. Both orders are allowed.
- A6 writes v to z. No other z write can fall between A6 and A7, so A7 reads v. A8 then writes v to y, which makes the final y = v.
- The only write to y is A8. B2 can take effect before A8 (reads 0) or after A8 (reads v); both fit, since A8 < A9 and only B2 < Q < A9 is required.
- B8 writes B2's value to z after all of A's writes. So B9 returns B2's value, and that is also the final z.

**x**
- B7 writes 4 to x. A2 writes 1 to x and has no ordering constraint against B5–B7.
- If A2 takes effect after B7, the final x is 1. Otherwise it is 4.
- When A2 is after B7, we have B2 < B7 < A2 < A8. B2 then must read 0, so final x = 1 forces B2 = 0.

**Combinations (B9, final x, final y, final z)**
- v = 6: (0, 4, 6, 0), (0, 1, 6, 0), (6, 4, 6, 6)
- v = 1: (0, 4, 1, 0), (0, 1, 1, 0), (1, 4, 1, 1)

BEGIN
0 4 6 0
0 1 6 0
6 4 6 6
0 4 1 0
0 1 1 0
1 4 1 1
END