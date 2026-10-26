Only two final values of z are possible: **2** and **4**.

**Key facts:**
- **B1 always reads 0.** The only write to y is B3, which writes B1's own result. B3 starts after B1 ends, so B3 can never take effect before B1 and y is always 0 when B1 reads it. So B2 writes 0 to z, and B3 writes 0 to y.
- **The z writes are** A1 (2), B2 (0), C1 (1), and C2 (4).
- **B4 returned 4**, so C2 must take effect before B4, and no other z write may fall between C2 and B4.
- **B2 must precede C2.** B2 is before B4 in program order, and it writes 0, so it cannot lie between C2 and B4. That means B2 is before C2.
- **C1 must precede C2** by program order, so C1 can never be the last z write. Neither can B2, which precedes C2.
- **A1 must precede C2 or follow B4.** It writes 2, which cannot lie between C2 and B4.

**Final z = 4:** C2 is last. Order B1, B2, B3, A1, C1, C2, B4, then A2–A5. A3 and A4 read x = 1 because A2 precedes them and nothing else writes x.

**Final z = 2:** A1 is last. Order B1, B2, B3, C1, C2, B4, then A1, A2–A5. A1 can come after B4 because it only needs to precede A2, and A2 writes x, not z.

BEGIN
2
4
END