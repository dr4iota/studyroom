The possible outcomes are six combinations of (Q1, Q2, Q3, Q4).

**Constraints.** Program order holds within each thread. The sync points add these cross-thread constraints: A1 < B5 (from S), B1 < A3 (from P), B2 < A9 (from Q), and A9 < B8 (from R). B8 and B9 therefore come last.

**Simplifications.**
- B9 reads z after B8, so Q1 = Q4 = the value B2 read.
- y is written only by A8, which writes A4's value (A7 reads A6's write, which equals A4's value). So Q3 = A4's value.
- x's final value is 4 if B7 is after A2, and 1 if A2 is after B7. So Q2 ∈ {1, 4}.
- A4 reads z, which holds either 6 (from A1) or 1 (from B1), depending on which is later.
- B2 reads y, so it is 0 if it precedes A8, or A4's value if it follows A8.

**Cases.**
- **A4 = 1** (A1 before B1): B2 can be 0 or 1. The combinations are (B2, x) = (0, 4), (1, 4), (0, 1). The pair (1, 1) is impossible because B2 after A8 forces B2 before B7 before A2 after A8, a contradiction.
- **A4 = 6** (B1 before A1): B2 can be 0 or 6. The combinations are (0, 4), (0, 1), (6, 4). The pair (6, 1) is impossible for the same reason as above.

Each combination has a witness schedule that satisfies all sync constraints. For example, (6, 4, 6, 6) is witnessed by B1 A1 A2…A8 B2 A9 B3…B7 B8 B9.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END