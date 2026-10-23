Six combinations are possible. B9 always equals the final z, and both equal what B2 read from y. The final y is either 1 or 6, decided by which of A1 and B1 writes z last.

**Ordering constraints from the sync points**
- A1 < S < B5, B6, B7
- B1 < P < A3, …, A9
- B1, B2 < Q < A9
- A1 … A9 < R < B8, B9

**What A reads and writes**
- **A4:** Both A1 (z=6) and B1 (z=1) happen before A4. B1 is before P, which is before A3. So A4 returns 6 if B1 happened before A1, or 1 if A1 happened before B1. Both orders are allowed.
- **A6 and A7:** A6 writes A4's value to z. No other write to z can fall between A6 and A7. B1 is already done, and B8 comes after R. So A7 returns A4's value, and A8 writes it to y.
- **Final y:** A8 is the only write to y, so the final y equals A4's value, which is 1 or 6.

**What B2 reads and what that decides**
- **B2:** It returns 0 if it happens before A8. It returns A4's value if it happens after A8. Being after A8 is allowed, since we only need B2 < Q < A9.
- **B8 and B9:** B8 writes B2's value to z. All of A's operations are before R, so nothing writes z after B8. Therefore B9 = final z = B2's value.

**Final x**
- B7 writes 4. A2 writes 1 and can come after B7, because A2 is only bounded by A1 < A2 < R.
- If B2 happened after A8, then B7 comes after B2, which comes after A8 and therefore after A2. So the final x must be 4.
- If B2 read 0, the final x can be 1 or 4.

**Combinations (Q1, Q2, Q3, Q4)**
- B2 = 0: (0,1,1,0), (0,1,6,0), (0,4,1,0), (0,4,6,0)
- B2 = A4's value: (1,4,1,1), (6,4,6,6)

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END