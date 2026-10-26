Nothing in the problem constrains how the threads interleave, so any interleaving of the three threads' operations is allowed.

Let v be the value B1 reads and a the value A3 reads.

- **v:** B1 can run before any write to z (v=0), after A1 but before C1 (v=4), or after C1 (v=2).
- **a:** A1 and A2 precede A3, so z is already 4 or has been overwritten by C1. So a is 4 or 2.
- **Q1 (A4):** y is 0 until B4 writes v. A4 returns 0 if it runs before B4, or v if it runs after B4. So A4 is 0, or v, which can be 2 or 4.
- **Q2 (C5):** the last write to z before C5 is either C1 (2) or an A write of 4. A5 writes a, which is 2 or 4, so C5 is 2 or 4. Both are always achievable by placing A's writes before or after C1 and C5.
- **Q3 (x):** B3 always comes after B2, so B2's 4 is never final unless B3 writes 4 too. The final x is therefore C2's 2 or B3's v.

Which (A4, x) pairs are possible:
- **A4=0:**
  - x=0 needs v=0, with B1 first and B3 after C2.
  - x=2 is possible when C2 is last.
  - x=4 needs v=4 with B3 last, and A4 before B4.
- **A4=2:** this needs v=2, so B3 writes 2 and x=2.
- **A4=4:** this needs v=4. Then x=2 (C2 last) or x=4 (B3 last).

Each (A4, x) pair works with both C5=2 and C5=4. For example, to get C5=2 with A4=4, run A1, B1, C1 and then C2–C5, and let A5 write later.

That gives 3·2 + 1·2 + 2·2 = 12 combinations.

BEGIN
0 2 0
0 4 0
0 2 2
0 4 2
0 2 4
0 4 4
2 2 2
2 4 2
4 2 2
4 4 2
4 2 4
4 4 4
END