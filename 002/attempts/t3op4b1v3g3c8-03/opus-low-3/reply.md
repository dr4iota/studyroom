**Approach.** There are no sync points, so any interleaving that keeps each thread's order is allowed. Let b be the value B2 returns and c the value C1 returns.
- B3 writes b to x.
- C2 and C3 both write c to x.
- The final value of x comes from whichever of A4 (writes 2), B3 (writes b) or C3 (writes c) takes effect last.

**What B2 and C1 can return.**
- The only way x can be 0 after a write is if C writes 0, which requires C1 = 0.
- B2 runs after B1 has already seen 1, so x has been written by then. Therefore B2 = 0 only if C1 = 0, with C2 or C3 writing 0 between B1 and B2.
- C1 = 0: C1 runs before A1.
- C1 = 1: C1 runs after A1 and before A2, or after A3 and before A4.
- C1 = 3: C1 runs between A2 and A3.
- C1 = 2: C1 runs after A4.
- B2 can return 1, 3 or 2 by the same placements relative to A's writes.

**Final value for each (B2, C1) pair.** It is 2 (A4 last), b (B3 last) or c (C3 last). Each listed ordering was checked to be reachable.

| B2 | C1 | Possible final values | Example ordering |
|----|----|----|----|
| 0 | 0 | 0, 2 | C1, A1, B1(1), C2(0), B2(0), then A2–A4, B3, C3 in any order |
| 1 | 0 | 0, 1, 2 | |
| 3 | 0 | 0, 2, 3 | |
| 2 | 0 | 0, 2 | |
| 1 | 1 | 1, 2 | |
| 3 | 1 | 1, 2, 3 | A1, B1, A2, B2(3), A3, C1(1), then A4/B3/C3 last |
| 2 | 1 | 1, 2 | C1 reads 1 early; C3 runs after A4 |
| 1 | 3 | 1, 2, 3 | A1, B1, A2, C1(3), A3, B2(1), A4, then B3/C3 |
| 3 | 3 | 2, 3 | |
| 2 | 3 | 2, 3 | |
| 1 | 2 | 1, 2 | A1–A4 with B1 and B2 reading 1 early, C1(2), C2, C3, then B3 |
| 3 | 2 | 2, 3 | |
| 2 | 2 | 2 | |

B2 = 0 is impossible whenever C1 ≠ 0, so those pairs do not appear.

BEGIN
0 0 0
0 0 2
1 0 0
1 0 1
1 0 2
3 0 0
3 0 2
3 0 3
2 0 0
2 0 2
1 1 1
1 1 2
3 1 1
3 1 2
3 1 3
2 1 1
2 1 2
1 3 1
1 3 2
1 3 3
3 3 2
3 3 3
2 3 2
2 3 3
1 2 1
1 2 2
3 2 2
3 2 3
2 2 2
END