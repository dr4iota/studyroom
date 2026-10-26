Four outcomes are possible for (Q1, Q2, Q3):

- **A1 before B1:** B1 reads 6, B6 reads 4, and the final x is 4.
- **A1 between B1 and B2:** B1 reads 0, B6 reads 4, and the final x is 4.
- **A1 between B2 and B6:** B1 reads 0, B6 reads 6, and the final x is 6.
- **A1 after B6:** B1 reads 0, B6 reads 4, and the final x is 6.

The reasoning rests on three facts:

- **Final x:** A7 is the last write to x, and it writes the value A2 read. A2 happens after P, which is after B2, so the final x equals A2's value.
- **A2's value:** A2 reads 6 if A1 comes after B2, and 4 if A1 comes before B2 (B2 is the only other write to x before A2).
- **B1 and B6:** B1 reads 6 only if A1 precedes B1. B6 reads 6 only if A1 falls between B2 and B6, since A3 and A7 both come after R, which is after B6.

BEGIN
6 4 4
0 4 4
0 6 6
0 4 6
END