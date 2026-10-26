Both A4 and B3 span P. B1 and B2 finish before P, and B4 runs after P.

**Q2 (B2).** B2 can only see 0 or 2. B3's write starts after B2 ends, so B2 cannot return 3. It returns 2 only if A2 took effect before it.

**Q3 (final y).** A2 ends before P, and B3 and B4 both take effect after B3 starts, with B4 after B3 ends, which is after P. So B4 is the last write to y, and the final y equals the value B1 read, call it v. B1 can read 0, 3 or 1:
- v = 1 needs A3 to have taken effect before B1, and so A2 before B1. Then B2 must return 2.
- v = 0 or v = 3 leaves B2 free to be 0 or 2.

**Q1 (A4).** A2 ends before A4 starts, so A4 sees y = 2 unless a later write has landed. A4 can return:
- 2, if it takes effect before B3's write.
- 3, if it takes effect after B3's write and before B4's.
- v, if it takes effect after B4's write. A4 may end after B4 runs, so this is allowed.

A4's value is independent of B1 and B2, because those finish before P.

Combining these gives the following (A4, B2, final y):

BEGIN
2 0 0
2 2 0
3 0 0
3 2 0
0 0 0
0 2 0
2 0 3
2 2 3
3 0 3
3 2 3
2 2 1
3 2 1
1 2 1
END