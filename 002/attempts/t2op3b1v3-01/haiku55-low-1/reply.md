Every operation takes effect at its own instant, and the instants are totally ordered. So each execution is an interleaving of the six operations that keeps each thread's order (A1 < A2 < A3 and B1 < B2 < B3). There are C(6,3) = 20 such interleavings.

For each one, the reads return:
- **A2** (Q1): the latest of A1 (writes 1) and any of B2 (writes 3) or B3 (writes 2) that come before it.
- **A3** (Q2): the same rule, applied before A3.
- **B1** (Q3): 1 if A1 comes before B1, otherwise 0. B2 and B3 always come after B1.

Evaluating all 20 interleavings gives 12 distinct (Q1, Q2, Q3) triples. They are the outcomes below.

BEGIN
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
END