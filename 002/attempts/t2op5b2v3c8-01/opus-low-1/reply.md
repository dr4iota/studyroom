A3 must see either A2's write of 1 or a later write by B3 or B4, so y is 1, the value B1 read, or the value B2 read.

**What B1 and B2 can read.** B1 and B2 both come before B3 and B4. So they can only see A's writes: 0 before A1, 3 after A1, or 1 after A2. Because A's writes happen in a fixed order and B1 comes before B2, B2 can never see an earlier write than B1. That leaves six pairs: (0,0), (0,3), (0,1), (3,3), (3,1) and (1,1).

**What A3 can read.** A3 comes after A2, so it returns 1 unless B3 or B4 takes effect between A2 and A3. A4 then copies that value to y, so the final y equals what A3 read.
- **y = 1:** Run all of thread B before A2, or run B3 and B4 after A3.
- **y = B1's value:** Place B3 after A2 and before A3, and B4 after A3. B3 can always be delayed past A2 because it comes after B2.
- **y = B2's value:** Place B4 after A2 and before A3.

Each of these orderings is compatible with every (B1, B2) pair above. So for each pair, y can be 1, B1's value or B2's value.

| B1 | B2 | possible y |
|----|----|------------|
| 0 | 0 | 0, 1 |
| 0 | 3 | 0, 1, 3 |
| 0 | 1 | 0, 1 |
| 3 | 3 | 1, 3 |
| 3 | 1 | 1, 3 |
| 1 | 1 | 1 |

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
0 3 3
0 1 0
0 1 1
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END