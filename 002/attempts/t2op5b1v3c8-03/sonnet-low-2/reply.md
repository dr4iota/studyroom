Q1 is the value returned by A5 and Q2 is the value returned by B3.

A writes 2, 3, 1, 3 to x in that order. B's two writes both carry the value v2 that B2 read. B's writes happen only after B3.

**Q1, the value A5 can return.** A5 starts after A4, so x holds 3 unless a B write lands between A4 and A5. If no B write lands there, A5 returns 3. If B4 or B5 lands there, A5 returns v2.

**Q2, the value B3 can return.** B3 is a read that comes at or after B2 in time, so it can see any value written up to that point.

**Case A5 = 3.** B's writes all happen after A5, or write 3 themselves. B3 can still be 0, 1, 2 or 3. For example, B3 = 0 happens when all of B's reads come before A1, and B3 = 1 happens when B3 reads after A3.

**Case A5 = 0.** B2 reads 0, so it comes before A1. B4 then writes 0 after A4, and A5 reads that 0. B3 comes before B4, so it can be 0, 2, 1 or 3.

**Case A5 = 2.** B2 reads 2, so it falls between A1 and A2. B3 then reads a later value, which can be 2, 3 or 1. B4 writes 2 after A4, and A5 reads it.

**Case A5 = 1.** B2 reads 1, so it falls between A3 and A4. B3 can read 1 or 3, because B4 writes 1 after A4 and A5 reads it.

BEGIN
3 0
3 1
3 2
3 3
0 0
0 1
0 2
0 3
2 2
2 3
2 1
1 1
1 3
END