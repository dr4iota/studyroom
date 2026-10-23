**Ordering constraints**

- Thread A: A1–A4 finish before Q. A5 lies after Q and before P.
- Thread B: B1–B4 finish before Q. B5 starts before P and ends after P.
- B5 has no constraint relative to Q. It may start, and take effect, before Q. So B5 can take effect anywhere after B4, including before or between A1–A4.
- A5 reads x and is not asked about, so it does not matter here.

**Possible values**

- **A1** can read 0 (no write yet), 1 (B1 or B5), 3 (B2, or B4 copying a 3), or 2. A1 = 2 is impossible: the only source of 2 is A4, which comes after A1, or B4 copying B3 = 2. B3 = 2 needs A4 before B3, and B3 is before B4 and so before A1, a contradiction.
- **B3** comes after B2, so it reads 3 (B2), 2 (A4), or A1's value (via A2).
- **Final y** is the last write among A2, A4, B4 and B5. B1 and B2 can never be last because B4 follows them.

**Case analysis**

- **A1 = 0** (A1 before B1):
  - B3 = 3: the last write can be A2 (0), A4 (2), B4 (3) or B5 (1).
  - B3 = 2: A4 is before B3, so the last write is B4 (2) or B5 (1).
  - B3 = 0: A2 is between B2 and B3, and A4 comes after B3. The last write is A4 (2), B4 (0) or B5 (1).
- **A1 = 1**:
  - B3 = 3: final y is 1, 2 or 3.
  - B3 = 2: final y is 1 or 2.
  - B3 = 1: A4 comes after B3, so final y is 1 or 2.
- **A1 = 3**:
  - B3 = 3: final y is 3 (A2 or B4), 2 or 1.
  - B3 = 2: final y is 1 or 2.

BEGIN
0 3 0
0 3 1
0 3 2
0 3 3
0 2 1
0 2 2
0 0 0
0 0 1
0 0 2
1 3 1
1 3 2
1 3 3
1 2 1
1 2 2
1 1 1
1 1 2
3 3 1
3 3 2
3 3 3
3 2 1
3 2 2
END