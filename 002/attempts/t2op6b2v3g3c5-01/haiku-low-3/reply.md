The possible outcomes are below. Two facts drive the analysis:

- **A1 can't read 2.** The only write of 2 to x is A2, which comes after A1 in thread A.
- **Final y is either b4 or a1.** B4's value is a1 if A3 precedes B4, else 0. A4 reads a1, 2, or b4 (never 0 unless B6 wrote 0).

Working through the interleavings of A3 and A4 against B4, B5, and B6, and checking each a1 ∈ {0, 1, 3} for feasibility against the x-constraints from B3, gives these (Q1, Q2, Q3) outcomes. Each was checked with a concrete ordering. For example, (3, 2, 3) comes from B1 B2 A1 B3 A2 A3 B4 B5 A4 B6 A5.

BEGIN
0 0 0
0 2 0
1 0 0
1 1 0
1 1 1
1 2 0
1 2 1
3 0 0
3 2 0
3 2 3
3 3 0
3 3 3
END