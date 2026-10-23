The final value of y can be **2** or **5**.

1. **What B3 reads.** The only write to z is A1, which writes 5. B2 already returned 5, so A1 took effect before B2, and therefore before B3. So B3 returns 5. That means B4 writes 5 to y and B5 writes 5 to x.

2. **The writes to y.** There are four: C1 writes 1, C4 writes 4, A4 writes 2 and B4 writes 5.

3. **Ordering from the known reads.**
   - A2 returned 1, so it took effect after C1 and before C4.
   - A3 returned 4, so it took effect after C4. No other write to y can fall between C4 and A3, so B4 is not in that gap.
   - A4 comes after A3 in thread A.
   - Together these give C4 → A3 → A4. So C4 is never the last write, and the final value of y comes from either A4 or B4.

4. **Whether B4 can come last (y = 5).** B4 must come after B3, which comes after A1. Nothing else forces B4 to come before A4. So B4 can take effect after A4, and the final value is 5.

5. **Whether A4 can come last (y = 2).** B4 can take effect between A3 and A4. It can also take effect before C1, since C1 has no ordering link to thread B. Either way A4 is last, and the final value is 2.

6. **Checking C3.** C3 returned 1 for x. It must take effect after B1 (which writes 1) and before B5 (which writes 5). Thread C has no ordering link to B5 or to B1, so C3 can be placed there in both cases.

BEGIN
2
5
END