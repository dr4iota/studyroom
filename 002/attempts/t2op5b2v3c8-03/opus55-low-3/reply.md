Each thread runs in order, so it is enough to look at where B1 and A4 fall relative to the other operations.

**What B1 can read (call it r):**
- If B1 is before A1, then r = 0.
- If B1 is between A1 and A2, then r = 2.
- If B1 is after A2, then r = 1.

**How the outcomes depend on r and A4:**
- B2 writes r to x.
- B3 returns 3 if A4 takes effect between B2 and B3. Otherwise it returns r.
- B5 returns 3 if A4 takes effect between B2 and B5. Otherwise it returns r.
- The final y is B3's value if B4 takes effect after A5. Otherwise it is 1, because A5 writes 1 last.

**Cases by where A4 falls (for r = 0 or 2):**
1. A4 before B2: B3 = r and B5 = r. A5 can land before or after B4, so the final y is r or 1.
2. A4 between B2 and B3: B3 = 3 and B5 = 3. A5 can land before or after B4, so the final y is 3 or 1.
3. A4 between B3 and B5: B3 = r and B5 = 3.
   - If B4 is before A4, then A5 is after B4 and the final y is 1.
   - If B4 is after A4, A5 can land on either side of B4, so the final y is r or 1.
4. A4 after B5: B3 = r and B5 = r. A5 comes after B4, so the final y is 1.

**Case r = 1:** every write to y after B1 is 1, so the final y is always 1 unless B4 writes 3.
- If A4 is before B2, the result is (1, 1, 1).
- If A4 is between B2 and B3, the results are (3, 3, 3) or (3, 3, 1).
- If A4 is between B3 and B5, the result is (1, 3, 1).
- If A4 is after B5, the result is (1, 1, 1).

**All combinations (B3, B5, final y):**
- r = 0: (0 0 0), (0 0 1), (3 3 3), (3 3 1), (0 3 0), (0 3 1)
- r = 2: (2 2 2), (2 2 1), (3 3 3), (3 3 1), (2 3 2), (2 3 1)
- r = 1: (1 1 1), (3 3 3), (3 3 1), (1 3 1)

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
1 1 1
1 3 1
2 2 1
2 2 2
2 3 1
2 3 2
3 3 1
3 3 3
END