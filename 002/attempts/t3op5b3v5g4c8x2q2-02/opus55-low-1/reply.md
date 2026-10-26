Possible combinations (C3, final y): (0, 3), (0, 4), (1, 3), (1, 4), (3, 4). The only excluded pair is (3, 3).

**Value read by B3.** Only B1 writes x, and it writes 3. B3 comes after B1 in thread B, so B3 returns 3 and B4 writes 3 to y.

**Writes to y.** The only writes are B4 (value 3) and C5 (value 4). So A2 returns 0, 3 or 4, and the final y is 3 or 4.

**Writes to z.** A1 writes 1, B2 writes 1, and A4 writes whatever A2 returned.

**Possible values for C3 (the read of z):**
- **0:** C3 must follow C2, and C2 follows B1. C3 can still take effect before both A1 and B2, so it returns the initial 0.
- **1:** C3 takes effect after A1 or B2, and A4 has not yet overwritten z.
- **A4's value:** A4 can take effect before C3. Then A2 < A4 < C3 < C5, so A2 cannot see 4. A2 returns 0 or 3, and C3 could return 0 or 3 this way.

**Combining with the final y:**
- **C3 = 3** requires B4 < A2 < A4 < C3 < C5. C5 is then the last write to y, so the final y must be 4.
- **C3 = 0 or 1:** the order of B4 and C5 is unconstrained, so the final y can be 3 or 4.

BEGIN
0 3
0 4
1 3
1 4
3 4
END