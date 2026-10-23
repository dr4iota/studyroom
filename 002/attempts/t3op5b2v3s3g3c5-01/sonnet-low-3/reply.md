Only the writes to y matter for A1 and A2, and they are constrained as follows.

**Writes to y.** The writes to y are C1 (1), C2 (2) and B3 (2). Over time y therefore goes 0, then 1, then 2, and stays 2.

**Thread C.** All of C's operations finish before P. That means C1, C2 and C3 take effect before P.

**Thread B.**
- B1 returned 0, so it takes effect before C1.
- B4 starts after P, so it comes after all of C's operations.

**A1 and A2.** A1 comes before A2, and both read y.
- A2 starts early and only has to end after R, so it can take effect before C1, between C1 and C2, or after C2.
- A1 can be 0, 1 or 2, but A2 cannot be smaller than A1, because y never decreases.
- A3 and the other known results are consistent with every one of these pairs.
- The possible (A1, A2) pairs are (0,0), (0,1), (0,2), (1,1), (1,2) and (2,2).

**B2.** B2 reads x.
- B2 comes after B1 but can still come before C3, which is the first write to x. In that case it returns 0.
- B2 can also come after C3, in which case it returns 1.
- This choice does not restrict the A reads, so each (A1, A2) pair combines with both values.

That gives 6 × 2 = 12 combinations.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 2 0
2 2 1
END