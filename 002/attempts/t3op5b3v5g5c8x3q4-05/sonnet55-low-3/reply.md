A2 must return 0 and the final y is always 2. The reasoning follows from the known read results.

**Writes to y.** The writes are A1 (5), B1 (4) and C3 (the value C2 read).
- B5 returns 2, so the last write to y before B5 is C3, and C2 must have read 2.
- B3 returns 4 and B5 returns 2, so the order of y writes is B1, then B3, then C3.
- A3 returns 4, so A1 comes before B1, and A3 happens before C3.
- C3 is therefore the last write to y, so the final y is 2 (Q4).

**Q1.** The only write to z is C5, which comes after C3. A2 comes before A3, and A3 comes before C3, so A2 happens before any write to z. A2 returns 0.

**x, C2 and C4.** C2 reads 2, so C1 is the last write to x before C2. Both B2 and B4 (each writing 3) are therefore either before C1 or after C2. C4 comes after C3, which comes after C2.
- If B2 and B4 both come before C1, x ends at 2 and C4 reads 2.
- If B4 comes after C2, x ends at 3. C4 can read 2 (C4 before B4) or 3 (C4 after B4). B2 can be before C1 or after C2.

The combinations (Q1, Q2, Q3, Q4) are:

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END