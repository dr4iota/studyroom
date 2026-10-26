No thread here has sync points, so the only constraints are that each thread runs its own operations in order and that reads agree with writes.

**A3 and A4 (reads of y):** Block y only ever holds 0, then 4 (after B3), then 2 (after B4), in that order. A3 runs before A4, so A4 can never see an earlier value than A3. That leaves six possible pairs: (0,0), (0,4), (0,2), (4,4), (4,2) and (2,2).

**B2 (read of x):**
- B2 returns 0 if it takes effect before A1, and 3 if it takes effect after A1.
- If B2 = 0, the order is B2 < A1 < A2 < A3 < A4, and B2 < B3 < B4. B3 and B4 can still fall anywhere relative to A3 and A4. So all six (A3, A4) pairs remain possible.
- If B2 = 3, the order is A1 < B2 < B3 < B4. B3 and B4 can still land before, between or after A3 and A4, because A2 can be placed freely. So all six pairs remain possible again.

The reads of z (B1 and A5) are not asked about and do not constrain anything. That gives 6 × 2 = 12 combinations.

BEGIN
0 0 0
0 0 3
0 4 0
0 4 3
0 2 0
0 2 3
4 4 0
4 4 3
4 2 0
4 2 3
2 2 0
2 2 3
END