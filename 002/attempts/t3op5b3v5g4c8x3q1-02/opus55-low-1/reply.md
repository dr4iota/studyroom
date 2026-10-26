C4 can return **1, 2 or 4**.

**What C4 can read.** C4 reads z after C1 has written 2 to z. So C4 returns 2, or the value of a later write to z. The only other writes to z are:
- A2, which writes 1.
- B3, which writes the value read by B2.

**What B2 can read.** B1 read y and got 1, so A1 (write 1 to y) took effect before B1. B2 comes after B1, so it reads 1, or 4 if C3 has already taken effect. B3 therefore writes 1 or 4.

**The known results.** A4 must read 4 from y, so C3 takes effect before A4 and no other write to y comes between them. A1 is before A4, so A1 must come before C3. B1 must read 1, so B1 falls between A1 and C3. Each schedule below meets all of this.

**Each value is reachable** (each list is the order in which operations take effect):
- **C4 = 2:** A1, B1, A2, C1, C2, C3, C4, then the rest (A3, A4, A5, B2, B3, B4). Nothing writes z between C1 and C4.
- **C4 = 1:** C1, A1, B1, A2, C2, C3, C4, then the rest. A2 overwrites z with 1 after C1.
- **C4 = 4:** A1, B1, A2, C1, C2, C3, B2, B3, C4, then the rest. B2 reads 4 from y, and B3 writes 4 to z just before C4.

No other value is ever written to z, so these three are the only outcomes.

BEGIN
1
2
4
END