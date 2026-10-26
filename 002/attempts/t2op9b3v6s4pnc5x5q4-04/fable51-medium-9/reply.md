**Analysis**

- **z / B9:** B8 (after R) is the last write to z, since all of A's z-writes (A1, A6, A9) and B1 happen before R. So B9 returns B2's value, and final z = B2's value → Q1 = Q4.
- **A4:** reads z after P. Candidates are A1 (6) and B1 (1), unordered with respect to each other → A4 ∈ {1, 6}. A6 rewrites the same value, so A7 = A4 and A8 writes A4 to y. Final y = A4.
- **B2:** reads y before Q; A8 (the only y write) is also before Q. B2 is either before A8 (returns 0) or after it (returns A4).
- **x:** final value is 4 (B7) unless A2 happens after B7, giving 1. If B2 saw A8's write, then A2 < A8 < B2 < B7, forcing final x = 4. If B2 = 0, both are possible.

BEGIN
0 1 1 0
0 4 1 0
0 1 6 0
0 4 6 0
1 4 1 1
6 4 6 6
END