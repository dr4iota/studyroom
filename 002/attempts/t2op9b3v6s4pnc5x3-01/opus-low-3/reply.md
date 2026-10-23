**Fixed ordering.** Every step of B1–B7 happens before S. B1 and B2 come before P, B3 before R, B4 before Q, and B5–B7 before S. All of thread A happens after S, so A starts only after B7. Only B8 and B9 can overlap with thread A.

**B2 and B8.** The only writes to z are B7 and A1. Both take effect after B2, so B2 returns 0. That means B8 writes 0 to y.

**A8.** The z writes are B7 (before S) and then A1. Nothing writes z after A1, so A8 returns 6.

**A3 and A4.** At the end of A2, y = 6. The later writes to y are B8 (which writes 0) and A7, and A7 comes after A3 and A4. So the outcome depends on where B8 takes effect:
- **B8 before A2:** A3 = 6 and A4 = 6.
- **B8 between A2 and A3:** A3 = 0 and A4 = 0.
- **B8 between A3 and A4:** A3 = 6 and A4 = 0.
- **B8 after A4:** A3 = 6 and A4 = 6.

**B9.** B9 reads x after B8. The writes to x are B1 (5) and A5 (the value A4 read). If B9 takes effect before A5, it returns 5. If it takes effect after A5, it returns A4's value. Both orders are possible in every case above, since B8 can also come before A5 in the last case. So B9 is either 5 or A4's value.

**Combinations (A3, A8, B9):**
- A3 = 6, A4 = 6: B9 is 5 or 6.
- A3 = 0, A4 = 0: B9 is 5 or 0.
- A3 = 6, A4 = 0: B9 is 5 or 0.

BEGIN
6 6 5
6 6 6
6 6 0
0 6 5
0 6 0
END