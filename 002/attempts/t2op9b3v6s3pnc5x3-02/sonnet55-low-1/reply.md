Only A2's value matters for the final x, because A7 writes it back and nothing writes x after that.

**Constraints**
- B1 and B2 end before P, and A2 starts after P, so B1 and B2 both come before A2.
- B3 to B8 end before R, and A3 onward starts after R, so all of B's operations come before A3.
- A1 has no sync constraint, only program order before A2. It is the only write to x apart from B2 before A3.
- After A3, the only other write to x is A7. A2 is the read of x that A7 copies, so the final x equals A2's value.

**Q1, B1:** A1 may come before or after B1, so B1 is 0 or 6.

**Q2, B6:** It reads x after B2. B2 writes 4, and A1 may land before B6 and after B2, so B6 is 4 or 6.

**Cases**
- **A1 before B1:** B1 = 6, then B2 overwrites with 4. B6 and A2 both read 4, so the final x is 4. The result is (6, 4, 4).
- **A1 between B1 and B2:** B1 = 0, then B2 overwrites with 4. B6 = 4, A2 = 4, and the final x is 4. The result is (0, 4, 4).
- **A1 after B2:** B1 = 0. A1 must still come before A2, so A2 = 6 and the final x is 6. B6 is 4 if A1 comes after B6, or 6 if A1 comes before it. The results are (0, 4, 6) and (0, 6, 6).
- **B1 = 6 with B6 = 6 is impossible,** because B2 would overwrite A1's 6 with 4 before B6.

BEGIN
6 4 4
0 4 4
0 4 6
0 6 6
END