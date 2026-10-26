A1 can return 0, 2 or 3 with any of the 6 (B4, final z) pairs. A1 = 1 allows only B4 = 2 and final z = 2, which gives 19 combinations.

Only the operations on z matter here: A2 reads x and B2 writes y, and neither affects the asked values.

- **Thread A on z:** A1 reads z, then A3 writes 3, A4 writes 4, A5 writes 2.
- **Thread B on z:** B1 writes 3, B3 writes 2, B4 reads z, B5 writes 1.

**What A1 can return.** A1 comes before all of A's writes, so only B's writes can be visible to it.
- 0 if A1 is before B1.
- 3 if A1 is between B1 and B3.
- 2 if A1 is between B3 and B5.
- 1 if A1 is after B5.

**What B4 can return.** B4 comes after B3 and before B5, so it sees B3 or one of A's writes.
- 2 if B3 is the last write before B4, or if A5 is.
- 3 if A3 lands between B3 and B4, with A4 after B4.
- 4 if A4 lands before B4, with A5 after B4.

**Final z.** A5 is A's last write and B5 is B's last write, so the final value is 1 if B5 takes effect last and 2 if A5 does.

**Combining them by A1's value.**
- **A1 = 0:** A1 is before B1, so all of A's writes can be placed anywhere relative to B's. B4 can be 2, 3 or 4, and in each case A5 can fall before or after B5. All 6 pairs (B4, final) are possible.
- **A1 = 3:** A1 is between B1 and B3. A's writes can all come before B3 (giving B4 = 2 and final 1), or later in any arrangement. All 6 pairs are possible.
- **A1 = 2:** A1 is between B3 and B5. If A1 is after B4, B4 returns 2 and the final value can be 1 or 2. If A1 is before B4, B4 can return 2, 3 or 4 and the final value can be 1 or 2. All 6 pairs are possible.
- **A1 = 1:** A1 is after B5, so all of A's writes come after B5. B4 then returns 2 and the final value is 2. Only (2, 2) is possible.

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