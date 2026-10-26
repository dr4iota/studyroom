**Approach:** first pin down what the known read results force, then check which combinations of the remaining choices can occur.

**What B5 forces.** B5 reads z and gets 2. The only writes to z are:
- A1 writes 3.
- A4 writes 4.
- B3 writes the value B1 read.

Only B3 can produce 2, so B1 must have returned 2. So:
- C1 took effect before B1.
- The last write to z before B5 is B3, so A4 is not between B3 and B5.

**What C2 forces.** C2 reads z and gets 3, so A1 took effect before C2. Neither A4 nor B3 lies between A1 and C2.

**Q1 and Q3 (B2 and final y).** Every write to y stores 2: C1 writes 2, and B4 writes B1's value, which is 2. B2 comes after B1, which comes after C1, so B2 returns 2. The final value of y is 2. A2's known result of 2 is consistent with this, since A2 just needs to follow C1.

**Q2 (C4).** C4 comes after C3, which writes 5 to x. The only other write to x is A3, which writes 2.
- If A3 takes effect between C3 and C4, C4 returns 2.
- Otherwise C4 returns 5.

**Q4 (final z).** From the B5 constraint, A4 is either before B3 or after B5.
- If A4 is before B3, the last write is B3, so z ends as 2.
- If A4 is after B5, z ends as 4.

**Checking that all four combinations can happen:**
- C4 = 2 with z = 2: C1, A1, C2, C3, A2, A3, C4, A4, B1, B2, B3, B4, B5.
- C4 = 5 with z = 2: same as above, but move A3 before C3.
- C4 = 2 or 5 with z = 4: move A4 to after B5 in either of the orders above.

All four combinations are possible.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END