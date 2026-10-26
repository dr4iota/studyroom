**Ordering constraints from the sync points**
- B1 < P < A2…A9.
- B1, B2 < Q < A9 < R. All of A's steps finish before R.
- R < B8, B9.
- A1 < S < B5, B6, B7.
- Nothing orders P relative to S.

**Value of A4, and therefore y**
- A1 (writes 6 to z) and B1 (writes 1 to z) both finish before A2. Their order is free, so A4 returns either 6 or 1. Call this value v.
- A6 writes v to z. The only later write to z is B8, which comes after R, so A7 also reads v.
- A8 writes v to y, and nothing else writes y. So the final y = v, with v in {1, 6}.

**B2, B9 and the final z**
- B2 reads y before Q, so it returns 0 or v. It returns v only if A8 takes effect before B2.
- B8 writes B2's value to z after R, when all of A is done. B9 reads it back, so B9 = final z = B2's value.

**Final x**
- The writes to x are A2 (1), B5 (3), B6 (B3's value) and B7 (4). B6 always precedes B7, so the last write is either A2 or B7.
- A2 can come after B7, since P and S are unordered. In that case x = 1.
- Otherwise B7 is last and x = 4.
- If B2 returned v, then A2 < A8 < B2 < B7, so B7 is last and x = 4.

**Combinations** (B9, x, y, z), with v in {1, 6}:
- 0 1 v 0
- 0 4 v 0
- v 4 v v

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END