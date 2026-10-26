**How the writes interleave.** Block z is written by A3 (3), A4 (4) and A5 (2) in thread A, and by B1 (3), B3 (2) and B5 (1) in thread B. Block x is never written, and the write to y affects none of the asked values.

**Q1 (value returned by A1).** A1 comes before all of A's own writes. So it sees only B's writes to z:
- 0 if A1 takes effect before B1.
- 3 if A1 falls between B1 and B3.
- 2 if A1 falls between B3 and B5.
- 1 if A1 falls after B5.

**Q2 (value returned by B4).** B4 comes after B3 and before B5. It returns the last write to z before it, which is one of:
- B3, giving 2.
- A3, giving 3, if A3 falls between B3 and B4.
- A4, giving 4, if A4 falls between B3 and B4.
- A5, giving 2, if A5 falls between B3 and B4.

**Q3 (final value of z).** The last write to z is either B5, giving 1, or A5, giving 2.

**Combining them.**
- **A1 = 0, 3 or 2.** A1 takes effect before B5, and therefore before B4. A's three writes can then be placed freely around B3, B4 and B5:
  - Before B4, any one of them can be the last write after B3. So B4 can return 2, 3 or 4.
  - Each of these can be combined with either B5 or A5 being the final write to z.
  - That gives all 3 × 3 × 2 = 18 combinations.
- **A1 = 1.** A1 takes effect after B5, so B4 has already happened. All of A's writes come after A1, so none can be seen by B4, which returns 2. A5 comes after B5, so the final value of z is 2. That gives 1 2 2.

BEGIN
0 2 1
0 2 2
0 3 1
0 3 2
0 4 1
0 4 2
3 2 1
3 2 2
3 3 1
3 3 2
3 4 1
3 4 2
2 2 1
2 2 2
2 3 1
2 3 2
2 4 1
2 4 2
1 2 2
END