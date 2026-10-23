Block x is only ever written with values that were read from x, and it starts at 0. Every read of x therefore returns 0, so B1 = 0 (and A1 = 0).

**Q2, the value B2 returns.** Block y can hold 0, 1, 2 or 3. B2 cannot return 1, because the only write of 1 is B5, which comes after B2. B2 can return:
- 0, if B2 runs before any write to y.
- 2, if B2 runs after C1.
- 3, if B2 runs after A4. A4 comes after A2, which has already returned 2.

**Q3, the value C3 returns.** C3 comes after C1, and C3 can return any of 0, 1, 2 or 3:
- 0: C1 writes 2, A2 reads 2, A4 writes 3, A5 writes 0 (the value A1 read), then C3 reads 0.
- 1: B5 writes 1 after A2 has read 2, then C3 reads 1.
- 2: C3 reads C1's value before A4 or B5 take effect.
- 3: A4 writes 3, then C3 reads 3.

**Combinations.** For each B2 value in {0, 2, 3}, every C3 value in {0, 1, 2, 3} can be scheduled, so all 12 pairs are possible. For example, B2 = 3 with C3 = 2 uses the order C1, A2 (reads 2), C2, C3 (reads 2), A4, B2 (reads 3).

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END