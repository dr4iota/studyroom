The approach is to find which writes can come before each read. Then I check which combinations can happen together.

**Ordering constraints from the sync points**
- R comes after A1–A5 and before B5–B9.
- P comes after A1–A7 and before B8–B9.
- Q comes after all of A and before B6–B9.
- So B6–B9 happen after all of thread A. B1–B4 have no ordering against thread A.

**Q1 (A1 reads z):**
- The writes to z are A3 (5), B3 (3), A9 and B9.
- A3 and A9 come after A1 in thread A, and B9 comes after all of A.
- So A1 returns 0, or 3 if B3 took effect first.

**A2:**
- A2 is also before A3, so it returns 0 or 3.

**Q2 (A5 reads x):**
- The writes to x are B1 (5), A4 (the value from A2) and B7.
- B7 comes after all of A, so it cannot affect A5.
- So A5 returns A2's value, or 5 if B1 took effect after A4.

**Q3 (final z):**
- B9 is the last write to z, so the final z is the value B2 read.
- A6 returns 5 or 3, because A3 or B3 has taken effect by then. So A9 writes 5 or 3.
- B2 can never return 3:
  - B3 comes after B2, so B2 could only see 3 from A9 after A6 returned 3.
  - That needs B3 before A6, and therefore B2 before A6.
  - But then A9 has not happened yet when B2 runs, so B2 sees 5 (from A3) or 0, not 3.
- So the final z is 0 or 5.

**Combining the cases**
- **A1 = 3:**
  - B3, and therefore B1 and B2, came before A1.
  - So B2 returned 0, and the final z is 0.
  - A2 = 3, and B1 is too early to overwrite A4, so A5 = 3.
  - Result: **3 3 0**.
- **A1 = 0, A2 = 3:**
  - B3 lies between A1 and A2, so B1 and B2 came before A2.
  - So B2 returned 0, the final z is 0, and A5 = 3.
  - Result: **0 3 0**.
- **A1 = 0, A2 = 0:**
  - If A5 = 0, B2 can return 0 or 5, so the final z is 0 or 5. Results: **0 0 0** and **0 0 5**.
  - If A5 = 5, B1 is after A4, so B2 is after A3 and cannot return 0. The final z is 5. Result: **0 5 5**.

BEGIN
0 0 0
0 0 5
0 5 5
0 3 0
3 3 0
END