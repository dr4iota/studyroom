Q1 can be 1 or 3, and Q2 is always 5.

**Reads that must return 5.** B4 returns 5, so B5 writes 5 to z, B6 writes 5 to y, and B8 writes 5 to x.

**B8 comes after C6.**
- C7 reads z = 5, so the last write to z before C7 must be a 5. A3 writes 2 and B7 writes 1, and neither can be the last z-write before C7. C8 comes after C7.
- If B7 took effect before C7, a later 5-write to z would be needed before C7. Only B2 and B5 write 5, and both precede B7, so none exists.
- So B7 comes after C7, and B8 comes after B7. Since C6 precedes C7, B8 comes after C6.

**Q1.** C1 precedes C6, so C6 cannot return 0. B8 comes after C6, so C6 cannot return 5. The only other writers to x are C1 (3) and A2 (1), so C6 returns 3 or 1. Both are achievable:
- C6 = 3 when A2 comes before C1 or after C6.
- C6 = 1 when A2 falls between C1 and C6.

**Q2.** The final x is the last of A2, B8 and C1. C1 precedes C6, which precedes B8, so 3 can't be final.
- Suppose A2 came after B8. Then A3 comes after B8, so all of B's writes to z are done, and the only later z-write is C8, which writes 3 or 1.
- A4 would therefore read a value other than 5 (A3's 2, or a value from C8).
- A5 would then write that non-5 value to y. No further write of 5 to y could follow: B and C's writes are done, and A1 comes earlier. A6 could not read 5, contradicting its known result.
- So A2 is not last, and B8 is last, giving final x = 5.

BEGIN
1 5
3 5
END