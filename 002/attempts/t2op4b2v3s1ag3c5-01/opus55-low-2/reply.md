**Timing constraints**

- **Thread A before P:** A1, A2 and A3 finish before P, because A4 starts before P. A4 ends after P.
- **Thread B before P:** B1 and B2 finish before P, because B3 starts before P. B3 ends after P.
- **Thread B after P:** B4 happens entirely after P, so it takes effect after B3.
- **Final y:** A2 takes effect before P, and B3 takes effect before B4. So B4 is the last write to y, and the final y equals the value B1 read.

**B2 (read of y)**

- B2 ends before B3 starts, so B3's write of 3 cannot be seen.
- The only earlier write to y is A2's write of 2.
- So B2 returns 0 if it takes effect before A2, or 2 if after.

**B1 (read of x), which sets the final y**

- B1 can return 0 (before A1), 3 (between A1 and A3) or 1 (after A3).
- If B2 returned 0, then B2 took effect before A2. Since B1 comes before B2, B1 took effect before A2 and therefore before A3. So B1 is 0 or 3.
- If B2 returned 2, B1 can be 0, 3 or 1.

**A4 (read of y)**

A4 takes effect after A2, since A2 ends before A4 starts. It can return:

- 2, if it takes effect before B3;
- 3, if it takes effect after B3 but before B4;
- B1's value, if B4 takes effect before A4. This is possible because both operations can take effect after P.

**Combinations** (A4, B2, final y)

| B2 | B1 = final y | A4 options |
|----|--------------|------------|
| 0 | 0 | 0, 2, 3 |
| 0 | 3 | 2, 3 |
| 2 | 0 | 0, 2, 3 |
| 2 | 3 | 2, 3 |
| 2 | 1 | 1, 2, 3 |

BEGIN
0 0 0
2 0 0
3 0 0
2 0 3
3 0 3
0 2 0
2 2 0
3 2 0
2 2 3
3 2 3
1 2 1
2 2 1
3 2 1
END