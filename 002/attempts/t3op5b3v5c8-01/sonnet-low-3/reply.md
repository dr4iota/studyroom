Each thread's operations can interleave in any order, since there are no sync points.

**Possible values**
- z is only written with 4 (A1, A2), with 2 (C1), or with A5's copy of what A3 read, which is 4 or 2. After C1 runs, z is therefore 2 or 4, so C5 returns 2 or 4.
- Let v be what B1 reads, which can be 0, 2 or 4. B3 writes v to x, and B4 and B5 write v to y. A4 returns 0 or v.
- Among the writes to x, B2 always precedes B3. The final x is therefore 2 if C2 is last, or v if B3 is last. If B3 is last and v = 4, x = 4.

**Cases by final x**
- **x = 0:** This needs v = 0, so B1 runs before any write to z, and B3 comes last. Every write to y is 0, so A4 = 0. C5 can be 2 or 4, depending on whether an A write lands between C1 and C5.
- **x = 2:** C2 is last, and v can be 0, 2 or 4. A4 can therefore be 0 (A4 before B4), 2 (v = 2, B4 before A4) or 4 (v = 4, B4 before A4). C5 can be 2 or 4 in each case.
- **x = 4:** This needs v = 4 with B3 last. A4 can be 0 (A4 before B4) or 4, but not 2, because v = 4. C5 can be 2 or 4.

BEGIN
0 2 0
0 4 0
0 2 2
0 4 2
2 2 2
2 4 2
4 2 2
4 4 2
0 2 4
0 4 4
4 2 4
4 4 4
END