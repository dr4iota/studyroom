**Answer: three combinations are possible: (0, 2, 2, 2), (0, 2, 3, 2) and (0, 3, 3, 2).**

**Step 1 – What C2 must have read.** B5 read 2 from y. The only writes to y are A1 (5), B1 (4) and C3 (the value C2 read). So C3 wrote 2, which means C2 read 2. C3 is also the last write to y before B5.

**Step 2 – Order of the y operations.**
- B3 read 4, so B1 is the last write to y before B3. C3 therefore takes effect after B3, and A1 is not between B1 and B3.
- A3 read 4, so B1 is the last write to y before A3. A1 comes before A3 in thread A, so A1 must come before B1. C3 must come after A3.
- This gives: A1 < B1 < {A3, B3} < C3 < B5.

**Step 3 – Q4, final y.** C3 is the last write to y, so the final y is **2**.

**Step 4 – Q1, A2.** The only write to z is C5. A2 comes before A3, which comes before C3, which comes before C5. So A2 returns **0**.

**Step 5 – Q2 and Q3, the x values.** The writes to x are B2 (3), B4 (3) and C1 (2). C2 read 2, so no B write falls between C1 and C2. C4 comes after C3, which is after B3. The final x is whichever of C1 and B4 takes effect last.
- **C1 after B4:** the final x is 2. No x write follows C1, so C4 reads 2. This gives **(0, 2, 2, 2)**.
- **C1 before B4, C4 after B4:** C4 reads 3 and the final x is 3. This gives **(0, 3, 3, 2)**.
- **C1 before B4, C4 before B4:**
  - If C1 comes after B2, C4 reads 2 and the final x is 3. A valid order is A1, B1, B2, C1, C2, B3, A3, C3, C4, B4, B5. This gives **(0, 2, 3, 2)**.
  - If C1 comes before B2, then C2 also comes before B2. C4 reads 3 and the final x is 3, which repeats **(0, 3, 3, 2)**.

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END