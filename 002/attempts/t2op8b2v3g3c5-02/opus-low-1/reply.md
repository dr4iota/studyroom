**Key facts**

1. **A1 returns 0.** Only A3 and A6 write to x, and both come after A1 in thread A. So nothing has written x when A1 takes effect. Every write to x therefore writes 0, which also fits B1 returning 0. This means A5 writes 0 to y.

2. **A2 returns 2.** Only B4 writes 2 to y. So B4 takes effect before A2, and no other write to y comes between them. B3 comes before B4, and A4 comes after A2, so neither can be in that gap. This fixes the order B3 < B4 < A2 < A4 < A5 < A7.

3. **Writes to y.** A4 writes 3, A5 writes 0, B3 writes 1, B4 writes 2, and B7 writes whatever B5 read. The final value of y is set by whichever of A5 and B7 takes effect last.

**B5 can return 2, 3 or 0.** B5 comes after B4, so it reads one of these:
- 2, if it is before A4;
- 3, if it is between A4 and A5;
- 0, if it is after A5.

B6 comes after B5 and before B7. A7 returns the value B7 wrote if B7 falls between A5 and A7, and 0 otherwise.

**Case B5 = 2** (B7 writes 2)
- B6 = 2, or B6 = 3 (B6 between A4 and A5). B7 can be:
  - before A5: A7 = 0, final y = 0;
  - between A5 and A7: A7 = 2, final y = 2;
  - after A7: A7 = 0, final y = 2.
- B6 = 0 (B6 after A5). B7 is then after A5, so final y = 2, and A7 is 2 or 0.

**Case B5 = 3** (B7 writes 3)
- B6 = 3. B7 can be:
  - before A5: A7 = 0, final y = 0;
  - between A5 and A7: A7 = 3, final y = 3;
  - after A7: A7 = 0, final y = 3.
- B6 = 0. B7 is then after A5, so final y = 3, and A7 is 3 or 0.

**Case B5 = 0** (B7 writes 0)
- B6 = 0, A7 = 0 and final y = 0.

Combinations, in the order A7, B6, final y:

BEGIN
0 2 0
2 2 2
0 2 2
0 3 0
2 3 2
0 3 2
2 0 2
0 0 2
3 3 3
0 3 3
3 0 3
0 0 3
0 0 0
END