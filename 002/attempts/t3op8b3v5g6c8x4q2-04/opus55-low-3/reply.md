**Possible outcomes:** C6 returns 1 or 3, and the final value of x is always 5.

**1. Which writes can C6 see?**
- C6 runs after C1, so it returns 3 (from C1), 1 (from A2) or 5 (from B8). It cannot return 0.

**2. B8 must come after C7, so C6 cannot return 5.**
- C7 reads z = 5. The only writes of 5 to z are B2 and B5. Both come before B7, which writes 1 to z.
- If B7 took effect before C7, then a write of 5 to z would have to follow B7. None exists, so C7 could not see 5.
- So B7 comes after C7, and B8 comes after B7. That puts B8 after C6, so C6 never sees it.

**3. C6 = 1 is possible.**
- Order the writes to x as C1, then A2, then C6.
- C2 must read z = 0 before A3 writes z. This is compatible, since A2 only needs to be before A3.

**4. C6 = 3 is possible.**
- Let A2 take effect before C1, so C6 sees C1's 3.

**5. Final x is always 5.**
- C1 cannot be last, because C1 comes before C6, which comes before B8.
- If C6 = 1, A2 comes before C6, so A2 is also before B8. B8 is last and x = 5.
- If C6 = 3, A2 is the only other candidate for last. Suppose A2 comes after B8.
  - Then A3 comes after B7, which is after B2 and B5. So A4 reads z = 2 (from A3) or 3 (from C8).
  - A5 then writes 2 or 3 to y.
  - Every write of 5 to y (B1, B6, C4, C5) comes before A2, so before A5.
  - A6 would then read 2 or 3, not the known 5. This case is impossible, so B8 is last and x = 5.

BEGIN
1 5
3 5
END