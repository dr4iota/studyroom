**Q1 (A2).** The only write to y is A3, which writes 4. A2 runs before A3 in thread A, so A2 always returns **0**.

**Q3 (C3).** C3 reads y, so it returns 0 if it takes effect before A3, or 4 if after. Both orders are allowed.

**Constraints from the known results.**
- **A1 returns 3:** C1 takes effect before A1, and B1 is not between C1 and A1.
- **C2 returns 3:** B1 is not between C1 and C2.
- A4 takes effect after A3.
- **Possible writers to x:** B1 writes 4, C1 writes 3, and C4 writes whatever C3 read.

**Case C3 = 0.** C4 writes 0 to x.
- **A4 = 3:** B1, C1, C2, A1, A2, C3, A3, A4, with C4 after A4.
- **A4 = 4:** C1, C2, A1, then B1, then A4, with C4 after A4.
- **A4 = 0:** C3, then A3, then C4, then A4, with B1 placed before C1.

**Case C3 = 4.** Here A3 comes before C3, and C4 writes 4 to x.
- **A4 = 3:** C1, A1, A2, A3, A4, then C3, C4, with B1 placed before C1.
- **A4 = 4:** A4 can read either B1's 4 or C4's 4.
- **A4 = 0 is impossible:** C1 has already written 3, and no later write puts 0 in x.

BEGIN
0 3 0
0 4 0
0 0 0
0 3 4
0 4 4
END