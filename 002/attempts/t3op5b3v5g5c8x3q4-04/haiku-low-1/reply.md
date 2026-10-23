The possible outcomes are (Q1, Q2, Q3) = (0, 0, 3), (0, 0, 4), (5, 0, 3), (5, 0, 4), and (1, 0, 3). Q2 is always 0, and Q3 can be 4 only when Q1 is 0 or 5.

**Q2 (B2's read) is always 0.** B2 can only see A3's write, which carries A1's value. If A3 takes effect before B2, then B3 writes b2 (= a1) to x after A3 and before B4. B4 must read 0, so b2 = 0. Otherwise B2 reads 0 directly.

**Q3 (final y)** is the later of C1's write (4) and A5's write (3). Both are always performed, so the final value is 3 or 4.

**Q1 (A4's read)** returns the latest z-write before A4, which can be 0, 5 (from B1 or C2), or 1 (from C3).

- **Q1 = 0:** Run all of A first, so A4 reads 0. Then C1 can go before or after A5, giving Q3 = 3 or 4.
- **Q1 = 5:** Run B1 first, then A through A3, and let B2 read 0 before A3 takes effect. Putting C1 before or after A5 gives Q3 = 3 or 4.
- **Q1 = 1:** A4 must come after C3 with no z-write in between. That forces C1 < C2 < C3 < A4 < A5, so Q3 = 3. Q3 = 4 is impossible here.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END