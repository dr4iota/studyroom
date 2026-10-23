Q1 is always 2, Q3 is always 2, Q2 can be 2 or 5, and Q4 can be 2 or 4. All four combinations are achievable.

**Key constraints:**
- **y:** Both writes to y (C1 and B4) write 2, so y is 0 until C1 and 2 afterward. A2 returns 2 only if A2 comes after C1. Because B1 must also return 2 (see below), B2 returns 2 and the final y is 2.
- **B1 and z:** The only z-writes are A1 (3), A4 (4), and B3 (the value B1 read). B5 returns 2, which can only come from B3, so B1 must return 2. That forces C1 < B1 < B3 < B4 < B5.
- **C2 returns 3:** The latest z-write before C2 must be A1, so A1 < C2 with no B3 or A4 in between.
- **B5 returns 2:** The latest z-write before B5 must be B3, so B3 < B5 with no A1 or A4 in between.
- **Final z:** Either A1 < B3 (with C2 < B3), where final z is 2 if A4 comes before B3 and 4 if after; or B3 < B5 < A1, where final z is 4.
- **C4 (x):** The read returns 5 if C4 sees C3 as the latest x-write, and 2 if A3 falls between C3 and C4. Both are possible.

**Witness schedules (one per combination):**
- 2 2 2 4: C1, B1–B5, A1, A2, C2, C3, A3, C4, A4
- 2 5 2 4: C1, B1–B5, A1, A2, A3, C2, C3, C4, A4
- 2 2 2 2: C1, B1, B2, A1, A2, C2, C3, A3, C4, A4, B3, B4, B5
- 2 5 2 2: C1, B1, B2, A1, A2, C2, C3, C4, A3, A4, B3, B4, B5

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END