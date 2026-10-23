The final value of z can be **4** or **5**.

**Step 1: Which write does A4 read?**

The writes to z are A1 (5), A2 (3), B2 (the value B1 read from x), B3 (4), C2 (3) and C5 (the value C4 read). A4 returns 5, so the last write to z before A4 must have written 5.

- **A1 is ruled out.** A2 runs after A1 and before A4, and A2 writes 3. Some write of 5 must come after A2.
- **B2 is ruled out.** B2 writes 5 only if B1 read x = 5. The only write of 5 to x is A5, which comes after A4. Then B1, and therefore B2, would come after A4, too late to feed A4.
- **So it must be C5, and C4 must have read 5.** C5 takes effect between A2 and A4. No other write to z falls between C5 and A4.

**Step 2: Which write does C4 read?**

C4 must also read 5. B2 cannot be that write: it would come after A5, which is after A4, which is after C5, which is after C4. So C4 reads A1's 5. That gives A1 < C4 < A2, with no write to z between A1 and C4. C2 comes before C4, so C2 must come before A1.

**Step 3: Final value of z**

B3 (writes 4) cannot fall between A1 and C4 or between C5 and A4. That leaves two cases:

- **B3 after A4.** B3 is the last write to z, so the final value is **4**. For example: A1, C4, A2, C5, A4, then B1, B2, B3.
- **B3 between C4 and C5.** B2 can also go there or before A1, so C5 is the last write and the final value is **5**.

BEGIN
4
5
END