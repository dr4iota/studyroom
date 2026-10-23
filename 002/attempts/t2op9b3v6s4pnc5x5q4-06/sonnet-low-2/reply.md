Each of the four values can be pinned down from the sync constraints.

**Ordering constraints**
- A1–A5 happen before S, and B1 happens after S, so A4 reads y = 0.
- B1 happens before R, and no write to y has happened yet, so B1 reads 0.
- A8 writes A4's value, which is 0.
- A8 starts after R, and A9 starts after Q and after A8. A9 ends before P.
- B9 starts after P, so B9 comes after A9.
- B2–B4 end before Q, so B2 comes before A9.

**Writes to x that matter:** B2 writes 4, A8 writes 0, and B9 writes B5's value. B9 is the last write to x because it comes after P.

**A9 (Q1):** A9 comes after both B2 and A8, and B9 comes after A9. So A9 returns the later of B2 and A8.
- If A8 comes before B2, A9 returns 4.
- If B2 comes before A8, A9 returns 0.

**B5 and B8:** B5 comes after B2, and B8 comes after B5. Both come before B9, so each reads either 4 or 0.
- If A8 comes before B2, then B5 = 4 and B8 = 4.
- If B2 comes before A8, B5 can be 4 (read before A8) or 0 (read after A8).
- If B5 = 0, then B8 = 0.
- If B5 = 4, then B8 can be 4 or 0.

**Final x (Q3):** B9 writes B5's value, so the final x equals B5.

This gives these combinations of (A9, B8, final x):
- (4, 4, 4)
- (0, 0, 0)
- (0, 4, 4)
- (0, 0, 4)

**Final z (Q4):** The writes to z are A5 (3), A6 (0), B3 (0) and B6 (1). A6 has no upper bound on when it happens, so either A6 or B6 can be last. The final z is therefore 0 or 1, independent of the other values.

BEGIN
4 4 4 0
4 4 4 1
0 0 0 0
0 0 0 1
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
END