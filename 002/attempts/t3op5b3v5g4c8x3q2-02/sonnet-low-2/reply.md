Every combination of A3 and B3 that can occur is listed below.

**Ordering forced by the known reads**
- C2 reads y = 1, so A1 < C2 < A2.
- C5 reads y = 2, so A2 < C5.
- C is sequential, so C1 < C2. Therefore C1 < A2 < A3, and x already holds 3 before A3 starts. The only other write to x is B4.

**Q1, the value A3 returns**
- A3 returns 3 if B4 has not written x between C1 and A3.
- A3 returns B4's value (the value B3 read) if B4 takes effect after C1 and before A3.

**Q2, the value B3 returns**
- B3 reads y, so it can return 0 (before A1), 1 (between A1 and A2), or 2 (after A2).

**Combinations**
- A3 = 3 works with B3 = 0, 1, or 2. In each case B4 takes effect after A3 (or before C1), so x stays at 3 for A3.
- A3 = B3 works for each of 0, 1, and 2. Here B4 writes the value B3 read after C1 and before A3, so A3 reads that value.
  - B3 = 0 happens before A1, with B4 after C1.
  - B3 = 1 happens between A1 and A2.
  - B3 = 2 happens after A2.
- The requirement that B5 reads z = 1 never rules out any of these. C4 or A4 can write 1 to z before B5, and B5 can read before A5 overwrites it.

BEGIN
3 0
3 1
3 2
0 0
1 1
2 2
END