**Q1 = 0, Q2 is 2 or 3, Q3 is 2 or 3 (but not Q2 = 3 with Q3 = 2), and Q4 = 2.**

1. **C2 must have read 2.** B5 reads 2 from y. The only writes to y are A1 (5), B1 (4) and C3 (the value read by C2). So C3 wrote 2, which means C2 read 2. It follows that C5 writes 2 to z.

2. **Order of the writes to y.**
   - B3 reads 4, so B1 takes effect before B3, and neither A1 nor C3 falls between B1 and B3.
   - B5 reads 2, so C3 is the last write to y before B5. With step 1, that puts C3 after B3.
   - A3 reads 4, and A1 comes before A3 in thread A. So the order is A1 < B1 < A3 < C3.
   - No write to y follows C3, so **Q4 = 2**.

3. **Q1 (A2).** The only write to z is C5, and C5 comes after C3. A2 comes before A3, which is before C3. So A2 takes effect before any write to z and returns **0**.

4. **Q2 and Q3 (C4 and final x).**
   - The writes to x are C1 (2), B2 (3) and B4 (3).
   - C2 reads 2, so neither B2 nor B4 falls between C1 and C2.
   - B2 comes before B3, which is before C3, which is before C4. B4 comes after B3.
   - If B4 is before C1, then C4 reads 2 and final x = 2. One valid order is B2, B3, B4, C1, C2, C3, C4, B5.
   - If B4 is after C4, then C4 reads 2 and final x = 3.
   - If B4 (or B2) falls between C2 and C4, then C4 reads 3 and final x = 3.
   - C4 = 3 with final x = 2 is impossible. It would need B4 before C4 and C1 after C4, but C1 comes before C4.

All three combinations fit the thread A ordering in step 2.

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END