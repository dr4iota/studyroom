Reading the sync points shows that A2 returns 0, B9 always equals B2, and B2 and A8 only take certain values. The reasoning follows.

**A2 reads 0.** A1 and A2 finish before P, and B2 starts after P. All of B's writes to z (B3, B4, B7) come after B2. So A2 reads 0, and A3 and A7 both write 0 to x.

**B9 equals B2.** A5 (y=3) finishes before Q and S. B5 comes after S, so it is after A5 and writes B2's value to y. B5 is before B9 in B's thread, so B9 reads B2's value.

**B2 can be 0, 3 or 5.**
- It reads 3 if B1 happens before A1 and B2 happens before A3.
- It reads 5 if B1 is the last write to x before B2.
- It reads 0 if A3 or A7 comes after B1 and before B2.

**B8 can only be 0 or 5.** It is after Q, so after A3, and A1 precedes A3, so 3 cannot be the last write.

**Cases:**
- B2 = 3: B1 precedes A1, and A3 and A7 come after B2. The last write to x is 0, so B8 = 0 and A8 = 0. This gives (A8, B2, B8, B9) = (0, 3, 0, 3).
- B2 = 0: B1 is already overwritten by a 0 write, so B8 = 0 and A8 = 0. This gives (0, 0, 0, 0).
- B2 = 5:
  - A8 = 5 requires A7 to precede B1. Then no later 0 write exists, so B8 = 5. This gives (5, 5, 5, 5).
  - A8 = 0 requires A7 after B1. B8 can fall before A7 (reads 5) or after it (reads 0). This gives (0, 5, 5, 5) and (0, 5, 0, 5).

The asked order is A8, B2, B8, B9.

BEGIN
0 3 0 3
0 0 0 0
5 5 5 5
0 5 5 5
0 5 0 5
END