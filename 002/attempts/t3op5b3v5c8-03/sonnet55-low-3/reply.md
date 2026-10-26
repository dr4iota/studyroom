Z is never written except by A5, which writes what A3 read. A3 runs before A5, so z stays 0 and A3 reads 0. Therefore A4 writes 0 to y.

The writes to y are A1 (3), A4 (0), B2 (5) and C1 (2). A1 comes before A4, and B1 comes before B2, which comes before B4.

**Q1 (B1):** B1 runs before B2, so it can read 0, 3 or 2 but never 5.

**Final y:** A1 is always followed by A4, so the final value cannot be 3. It can be 0 (A4 last), 5 (B2 last) or 2 (C1 last).

**Final y = 5:** B2 is the last write, so B4 reads 5. B1 can be 0, 2 or 3.
- (0,5,5), (2,5,5), (3,5,5)

**Final y = 2:** C1 comes after B2 and A4. B1 cannot be 2, because the only write of 2 comes after B2. B1 = 3 rules out B4 = 3, because the only write of 3 would then come before B2.
- B1 = 0: B4 can be 5, 0, 2 or 3.
- B1 = 3: B4 can be 5, 0 or 2.

**Final y = 0:** A4 is the last write. B1 = 2 rules out B4 = 2, and B1 = 3 rules out B4 = 3, since each value is written only once.
- B1 = 0: B4 can be 5, 0, 2 or 3.
- B1 = 2: B4 can be 5, 3 or 0.
- B1 = 3: B4 can be 5, 0 or 2.

BEGIN
0 5 5
2 5 5
3 5 5
0 5 2
0 0 2
0 2 2
0 3 2
3 5 2
3 0 2
3 2 2
0 5 0
0 0 0
0 2 0
0 3 0
2 5 0
2 3 0
2 0 0
3 5 0
3 0 0
3 2 0
END