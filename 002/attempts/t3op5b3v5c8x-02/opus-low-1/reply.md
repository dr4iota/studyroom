**Setup.** The only writes to y are A1 (4), C2 (1), B3 (5) and B5. B5 writes the value B1 read, called b. B1 comes before B3, so B1 can only see 0, 4 (from A1) or 1 (from C2). Therefore b ∈ {0, 1, 4}.

**Constraints used.**
- B3 comes before B5.
- C3 and C4 come after C's own write C2 (y = 1).
- C3 and C4 each return some y value current at or after C2, and C4's value is never older than C3's.
- The final value of y is whichever of A1, C2 and B5 takes effect last.

**Enumeration.** There are 12 orders of the four writes with B3 before B5. Each order limits b and fixes the values C3 and C4 can see:

| Write order | Possible b | Values visible after C2 | Final y |
|---|---|---|---|
| A1 C2 B3 B5 | 0, 4, 1 | 1, 5, b | b |
| C2 A1 B3 B5 | 0, 1, 4 | 1, 4, 5, b | b |
| A1 B3 C2 B5 | 0, 4 | 1, b | b |
| C2 B3 A1 B5 | 0, 1 | 1, 5, 4, b | b |
| A1 B3 B5 C2 | 0, 4 | 1 | 1 |
| C2 B3 B5 A1 | 0, 1 | 1, 5, b, 4 | 4 |
| B3 B5 A1 C2 | 0 | 1 | 1 |
| B3 B5 C2 A1 | 0 | 1, 4 | 4 |
| B3 A1 B5 C2 | 0 | 1 | 1 |
| B3 A1 C2 B5 | 0 | 1, 0 | 0 |
| B3 C2 A1 B5 | 0 | 1, 4, 0 | 0 |
| B3 C2 B5 A1 | 0 | 1, 0, 4 | 4 |

In each row, C3 and C4 can return any two values from the visible list, read in list order (both may be the same value). Collecting every combination from every row gives the list below.

BEGIN
0 0 0
1 0 0
1 1 0
1 4 0
1 5 0
4 0 0
4 4 0
4 5 0
5 0 0
5 4 0
5 5 0
1 1 1
1 4 1
1 5 1
4 1 1
4 4 1
4 5 1
5 1 1
5 4 1
5 5 1
0 0 4
0 4 4
1 0 4
1 1 4
1 4 4
1 5 4
4 4 4
4 5 4
5 0 4
5 1 4
5 4 4
5 5 4
END