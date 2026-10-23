All four (y, z) combinations are possible, and A9 always returns 5.

**Q1 (A9).** A8 writes 5 to x, and A9 runs after A8. Other writes to x are B4 and the earlier B2 (value 1), both of which take effect before A8, since B4 is before P and A8 is after P. The only later write to x is B9, which writes whatever B8 read. B7 and B8 start after Q, and A8 is before Q, so B8 reads x after A8 and sees 5. So B9 writes 5, and x holds 5 from A8 onward. A9 therefore returns 5.

**Q2 (final y).** The writes to y are A1 (5), A2 (4), A6 (the value A4 read) and B5 (6). A4 runs after A2, so it reads either 4 (from A2) or 6 (from B5, if B5 took effect between A2 and A4). A6 then writes 4 or 6.
- If B5 comes after A6, the final y is 6.
- If B5 comes before A6, the final y is A6's value. That is 6 if B5 landed between A2 and A4, and 4 if B5 came before A2 or between A4 and A6.

So the final y is 4 or 6.

**Q3 (final z).** The writes to z are B1 (2), B3 (6), A3 (1) and A5 (the value A4 read, 4 or 6). A3 comes before A5 in thread A and B1 comes before B3 in thread B, so the final z is whichever of B3 and A5 comes last.
- If B3 is last, z is 6.
- If A5 is last, z is its value, 4 or 6.

**Combinations of (y, z).**
- (4, 4): A4 reads 4, and B3 comes before A5.
- (4, 6): A4 reads 4, and B3 comes after A5.
- (6, 6): B5 comes after A6, so y is 6, and B3 comes after A5 (or A4 reads 6), so z is 6.
- (6, 4): B1, B2 and B3 run first, then A1 through A6 with A4 reading 4, then B4 and B5. This ordering respects every sync constraint.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END