The possible outcomes are (Q1, Q2) = (0, 3), (0, 4), (1, 3), (1, 4), and (3, 4).

**Fixed facts.** Only B1 writes x, so the known reads force C1 < B1 < C2, and B1 < A3. Since B1 precedes B3, B3 always returns 3, so B4 always writes 3 to y. Final y is 3 if C5 is before B4, and 4 if B4 is before C5.

**Q1 (value of z at C3).** The writes to z are A1 (1), B2 (1), and A4 (writes a2, the value A2 read from y). So C3 can return 0 (no z-write before it), 1 (A1 or B2 is the last write before it), or a2 (A4 is the last write before it). The value a2 can be 0, 3, or 4.

- **c3 = 4** would need C5 before A2, which is before A4, which is before C3. But C5 comes after C3. Impossible.
- **c3 = 3** needs A4 before C3 with a2 = 3. Reading 3 at A2 requires B4 before A2 and no C5 before A2. This forces B4 < A2 < A4 < C3 < C5, so final y = 4. Only (3, 4) is possible.
- **c3 = 0** is possible with final y = 3 or 4. Put A1, B2, and A4 after C3, and place B4 after or before C5.
- **c3 = 1** is possible with final y = 3 or 4. Let B2 precede C3 and A4 follow C3, then place B4 before or after C5.

**Checked schedules.**
- (0, 3): C1, B1, C2, C3, C4, C5, B2, B3, B4, A1, A2, A3, A4. A2 reads 3, C3 reads 0, final y = 3.
- (0, 4): C1, B1, C2, C3, C4, B2, B3, B4, C5, A1, A2, A3, A4. A2 reads 4, C3 reads 0, final y = 4.

BEGIN
0 3
0 4
1 3
1 4
3 4
END