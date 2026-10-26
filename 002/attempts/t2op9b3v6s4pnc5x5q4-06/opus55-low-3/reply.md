**Fixed values first.**

- A4 reads y before S, and every B operation comes after S. B is the only thread that writes y, so A4 returns 0.
- A6 therefore writes 0 to z, and A8 writes 0 to x.
- B1 reads y before B4 and B7, which are the only writes to y. So B1 returns 0, B3 writes 0 to z, and B4 writes 0 to y.

**Ordering constraints from the sync points.**

- B2 happens before Q, and A9 happens after Q, so B2 happens before A9.
- A9 happens before P, and B9 happens after P, so A9 happens before B9.
- B5 comes after B2 in thread B.
- A1–A3 happen before S, so they come before every B write.
- B9 is the last write to x, so the final value of x is the value B5 read.

**Values of x seen by A9, B5 and B8.** The only writes to x after S are B2 (4), A8 (0) and B9.

- A9 returns whichever of B2 and A8 took effect last.
- B5 and B8 return 4, or 0 if A8 took effect after B2 and before that read.

**Final value of z.** The writes to z are A5 (3), A6 (0), B3 (0) and B6 (1). A5 comes before A6, and B3 comes before B6. So the final value of z is 1 if B6 is last, or 0 if A6 comes after B6.

**Cases.** Values below are listed as (A9, B8, final x, final z).

1. **A8 before B2:**
   - A9, B5 and B8 all return 4, so x ends as 4.
   - A6 < A8 < B2 < B6, so z must end as 1.
   - Result: (4, 4, 4, 1).
2. **B2 before A8, with A8 after B8:**
   - A9 returns 0, while B5 and B8 return 4. x ends as 4.
   - A6 and B6 can come in either order, so z is 0 or 1.
   - Results: (0, 4, 4, 0) and (0, 4, 4, 1).
3. **B2 before A8, with A8 between B5 and B8:**
   - A9 returns 0, B5 returns 4 and B8 returns 0. x ends as 4.
   - z is 0 or 1.
   - Results: (0, 0, 4, 0) and (0, 0, 4, 1).
4. **B2 before A8, with A8 before B5:**
   - A9, B5 and B8 all return 0, so x ends as 0.
   - A6 < A8 < B5 < B6, so z must end as 1.
   - Result: (0, 0, 0, 1).

BEGIN
4 4 4 1
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
0 0 0 1
END