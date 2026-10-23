The possible outcomes are determined by a few timing facts:

- **Final z** is always the value B2 read: B8 is the last write to z (every other z write precedes R, and B8 follows R). B9 comes right after B8, so Q1 is the same value, and Q4 = Q1.
- **Final y** is the value A7 read: A8 is the only write to y.
- **A7's read of z** equals A4's read, since B1 precedes A4 (and A6), and A1 precedes both. A4 reads 6 if B1 precedes A1, and 1 if A1 precedes B1. So Q3 ∈ {1, 6}.
- **B2's read of y** is 0 if B2 precedes A8, or the value A8 wrote (Q3) if A8 precedes B2. This is feasible, since A8 < B2 < Q < A9 is consistent with the constraints.
- **Final x** is 4 (from B7) if A2 precedes B7, or 1 if A2 comes after B7. Both orderings are feasible, since A2 only needs to precede A3, and B7 only needs to follow S.

These choices are independent, so the outcomes are the combinations of Q3 ∈ {1, 6}, Q1 = Q4 ∈ {0, Q3}, and Q2 ∈ {1, 4}.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 1 1 1
1 4 1 1
6 1 6 6
6 4 6 6
END