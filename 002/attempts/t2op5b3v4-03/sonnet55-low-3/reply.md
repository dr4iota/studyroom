All 12 combinations are possible. No sync points are given, so any interleaving of the two threads' operations is allowed.

**Q1 (A1 reads z):** A1 is the first operation in A, so only B's writes to z (B1 writes 3, B3 writes 2) can precede it. A1 can return 0, 3 or 2.

**Q2 (A5 reads y):** The only write to y is B5, which writes 4. A5 returns 0 if it runs before B5 and 4 if it runs after.

**Q3 (B4 reads x):** The only write to x is A4, which writes 1. B4 returns 0 if it runs before A4 and 1 if it runs after.

**Independence:** Every combination of the three values has a valid interleaving.
- For A1 = 0, 3 or 2, put the needed B writes (none, B1, or B1–B3) before A1, then order A2–A4, A5, B4 and B5 as the other two answers require.
- A5 = 4 needs B5 before A5, so B4 must also come before A5, and A4 must come before A5 too. B4 can still fall before A4 (returns 0) or after it (returns 1).
- A5 = 0 needs A5 before B5. B4 can then be before A4 (returns 0) or after it (returns 1), since A4 is still before A5.

For example, A1 = 2, B4 = 0, A5 = 0 comes from the order B1, B2, B3, A1, B4, A2, A3, A4, A5, B5.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
3 0 0
3 0 1
3 4 0
3 4 1
2 0 0
2 0 1
2 4 0
2 4 1
END