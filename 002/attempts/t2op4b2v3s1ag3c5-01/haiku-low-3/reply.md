The possible outcomes are below, with values in the order Q1 (A4's read), Q2 (B2's read), Q3 (final y). I derived them by reasoning about the allowed orderings of the effect instants rather than by running a program.

**Key constraints**
- A1 < A2 < A3 < A4 and B1 < B2 < B3 < B4 (program order within each thread).
- A1, A2, A3, B1, B2 all take effect before P, and B4 takes effect after P, so B4 is last among the operations that matter.
- A4 and B3 each straddle P, so their effects can fall on either side of P and in either relative order.

**Derived values**
- Q2 = 2 if A2 < B2, otherwise 0. A2 is the only write to y that can precede B2.
- Q3 = B1's read value, since B4 is the final write to y. B1 reads 0 if B1 < A1, 3 if A1 < B1 < A3, and 1 if B1 > A3.
- Q1 is the last write to y before A4: A2 (2), B3 (3), or B4 (B1's value), or 0 if none has happened.

**Enumeration by B1's value**
- B1 reads 0: A4 can read 2, 3, or 0, and B2 can read 2 or 0, giving 6 outcomes.
- B1 reads 3: A4 can read 2 or 3, and B2 can read 2 or 0, giving 4 outcomes. A4 cannot read 0 because A2 always precedes it.
- B1 reads 1: B2 always reads 2, and A4 can read 2, 3, or 1, giving 3 outcomes.

That gives 13 combinations.

BEGIN
0 0 0
0 2 0
2 0 0
2 2 0
3 0 0
3 2 0
2 0 3
2 2 3
3 0 3
3 2 3
1 2 1
2 2 1
3 2 1
END