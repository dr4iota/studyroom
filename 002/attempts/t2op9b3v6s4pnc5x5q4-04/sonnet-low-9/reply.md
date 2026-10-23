Every combination is listed below. Q1 and Q4 are always equal, and Q3 is always the value A4 reads.

**What A4 can read.** B1 ends before P and A2 starts after P, so both A1 and B1 finish before A4. A4 therefore reads 6 or 1, depending on which of A1 and B1 wrote z last. Call this value v.

**Effect on z and y.** Only A and B1 write z before B8, and A6 comes after B1. A7 therefore also reads v. A8 writes v to y, and A9 writes v to z. So the final y is v, which is 1 or 6.

**What B2 can read.** B2 ends before Q, and A9 starts after Q. B2 reads y, which is 0 if A8 has not run yet, or v if A8 has run.

**B8 and B9.** B8 starts after R, and every A step ends before R. B8 writes B2's value to z. B9 then reads that same value. So Q1 equals Q4, and both are B2's value, 0 or v.

**Final x.** B7 writes 4 to x, and A2 writes 1 to x.
- If B2 = 0, A2 can run after B7. A2 only needs to start after P and end before R, and neither constraint conflicts with B7. So the final x is 1 or 4.
- If B2 = v, A8 must run before B2. Then A2 runs before A8, which is before B2, which is before B7. So the final x is 4.

**Combinations (Q1 Q2 Q3 Q4):**
- B2 = 0: Q1 = 0, Q4 = 0, Q2 is 1 or 4, Q3 is 1 or 6.
- B2 = v: Q1 = v, Q4 = v, Q3 = v, Q2 = 4, with v either 1 or 6.

BEGIN
0 1 1 0
0 4 1 0
0 1 6 0
0 4 6 0
1 4 1 1
6 4 6 6
END