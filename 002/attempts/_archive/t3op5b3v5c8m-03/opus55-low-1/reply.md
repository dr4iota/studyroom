All 12 combinations of the three asked values are possible: B1 returns 0 or 2, and final x is 0 or 2, and final z is 0, 2 or 3.

**Q1: value returned by B1.** The only writes to x are A1 (writes 2) and B4. B4 comes after B1 in thread B, so B1 cannot see it. B1 therefore returns 0 or 2.

**Q2: final x.** The final value comes from whichever of A1 and B4 takes effect last.
- If A1 is last, x = 2.
- If B4 is last, x = the value read by B2. Before B2, the only writes to y can come from C3 and C4, because B3 comes after B2. C3 and C4 write C2's value.
- C2 reads x. It cannot see B4's value in a way that reaches B2: if C2 read B4's value, then C3 would follow B4, which follows B2. So C2's value, as seen by B2, is 0 or 2.
- So B2 returns 0 or 2, and final x is 0 or 2.

**Q3: final z.** The final value comes from whichever of C1 and A4 takes effect last.
- If C1 is last, z = 3.
- If A4 is last, z = the value read by A3. The writes to y are B3 (B1's value: 0 or 2) and C3/C4 (C2's value: 0, 2, or B4's value, which is 0 or 2). So A3 returns 0 or 2.
- Final z is 0, 2 or 3.

**Checking that every combination can actually happen.**
- **B1 = 0:** All combinations work. The hardest case is x = 0 with z = 2, and this order produces it:
  1. B1 reads 0, then A1 writes 2 to x.
  2. C2 reads 2, then B2 reads y = 0.
  3. C3 and C4 write 2 to y.
  4. A2 runs, then A3 reads y = 2.
  5. B3 writes 0 to y, either before C3 or after A3.
  6. C1 writes 3 to z, then A4 writes 2 to z (A4 after C1, so z ends at 2).
  7. B4 writes 0 to x after A1 (so x ends at 0).
- **B1 = 2:** A1 must come before B1. The cases still work:
  - x = 0: let B2 read 0 and put B4 last. B4 is automatically after A1.
  - z = 0: let A3 read y before B3 and C3.
  - z = 2: let A3 read B3's 2.
  - z = 3: let C1 come after A4.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END