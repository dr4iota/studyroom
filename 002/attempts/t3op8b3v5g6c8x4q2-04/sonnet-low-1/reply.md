Final x is always 5, and C6 can return 3 or 1.

**What the known results force:**
- C2 reads z = 0, so C2 happens before B2 and A3, the only writes to z other than B5, B7 and C8 that come later.
- C7 reads z = 5. The only writes of 5 to z are B2 and B5, and B7 (z = 1) comes after both. B7 would overwrite them, and nothing later puts 5 back before C7, so C7 happens before B7.
- B8 comes after B7, so C1, C6 and C7 all happen before B8.

**Q1 (C6):** C6 comes after C1, so it cannot return 0. It cannot return 5, because B8, the only write of 5 to x, comes after C6. It can return 3 if A2 has not happened yet, or 1 if A2 happened after C1 and before C6.

**Q2 (final x):** B8 writes 5 to x, and it comes after C1, so the final x is not 3. Could A2 come after B8, leaving x = 1?
- A6 reads y = 5, and A5 just before it writes A4's value to y.
- A4 reads z after A3 (z = 2), so it returns 2 or a later z write. The only 5s written to z are B2 and B5. For A4 to read 5, B5 must come after A3. That forces A2 < A3 < B5 < B8, so A2 comes before B8 and x ends as 5.
- Otherwise A5 writes a non-5 value, and a later write of 5 to y must restore it before A6. The writers of 5 to y are B6, C4 and C5. B6 comes before B8. C4 and C5 come before C6 and so before B8. Either way A5, and therefore A2, comes before B8.
- So A2 is always before B8, and the final x is 5.

C6 = 1 together with final x = 5 works, since B8 overwrites A2's 1 afterward. C6 = 3 with final x = 5 works the same way.

BEGIN
3 5
1 5
END