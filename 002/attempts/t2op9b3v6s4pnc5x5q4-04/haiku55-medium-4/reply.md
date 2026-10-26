The possible outcomes are (Q1, Q2, Q3, Q4) = (B9, final x, final y, final z):

- **Q1 and Q4 are equal.** B8 writes the value B2 read, after every write to z by A, so B9 and the final z both equal v(B2).
- **Q3 is 1 or 6.** A1 is the only earlier z-write that can be last before A4, and B1 can land just after it. So the value read by A7 is 1 when A1 < B1 and 6 when B1 < A1. A8 is the only write to y, so the final y equals that value.
- **Q1 is 0 or equal to Q3.** B2 reads 0 if it precedes A8. Otherwise it reads A8's value, which is Q3.
- **Q2 is 1 or 4.** The final x is 1 only if A2 comes after B7, which requires B2 < B7 < A2 < A8. That rules out B2 reading A8's value, so Q2 = 1 is only possible when Q1 = 0.

Each combination below was checked against an explicit ordering of the operations.

BEGIN
0 1 1 0
0 4 1 0
0 1 6 0
0 4 6 0
1 4 1 1
6 4 6 6
END