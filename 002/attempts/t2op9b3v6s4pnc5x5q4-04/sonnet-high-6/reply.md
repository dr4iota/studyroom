Six combinations are possible.

**Ordering constraints**
- B1 is before P, B2 is before Q, and A3–A8 are after P.
- A9 is after Q and before R, and B8 and B9 are after R.
- A1 is before S, and B5–B7 are after S.

**Q1 and Q4 (z).** B1 is before P and A1 is before A4, so A4 reads whichever of A1 (6) or B1 (1) took effect last. Call that value v, with v = 6 or 1. Nothing else writes z before A4.
- A6 writes v to z, and A7 reads z before A9, so A7 also reads v.
- A8 writes v to y, and it is the only write to y. So the final y is v.
- B2 reads y and sees either 0 or v, depending on whether A8 took effect before B2.
- A9 is before R and B8 is after R, so B8 is the last write to z. B8 writes B2's value, and B9 reads it back. So B9 = final z = B2's value.

**Q2 (x).** The writes to x are A2 (1) and B5, B6, B7 (3, B3's value, 4). B7 is the last of B's writes, so the final x is 4 if A2 is before B7, or 1 if A2 is after B7.
- Both orders are possible. For example, A1, S, B2–B7 can all happen before P, with A2 after them.
- If A2 comes after B7, then B2 is before A2, which is before A8. So B2 reads 0, giving B9 = 0 and z = 0.
- If x ends as 4, B2 can read 0 or v. B2 reads v when A2 and A3–A8 all happen after P and before B2, and B7 comes later.

**Cases**

| B9 | x | y | z |
|---|---|---|---|
| 0 | 4 | 6 | 0 |
| 0 | 4 | 1 | 0 |
| 6 | 4 | 6 | 6 |
| 1 | 4 | 1 | 1 |
| 0 | 1 | 6 | 0 |
| 0 | 1 | 1 | 0 |

BEGIN
0 4 6 0
0 4 1 0
6 4 6 6
1 4 1 1
0 1 6 0
0 1 1 0
END