There are no sync points, so any interleaving that keeps each thread's order is allowed. Let b = B2's result and c = C1's result. The values ever written are A's (1, 3, 1, 2), B3 (writes b) and C2/C3 (write c). The final value is set by whichever of A4, B3 or C3 takes effect last.

**What C1 (c) can read**
- **0:** C1 runs before A1.
- **1:** C1 runs after A1 or after A3.
- **3:** C1 runs after A2 and before A3.
- **2:** C1 runs after A4.
- C1 could also read B3's value. That gives c = b, which is already covered by the cases above.

**What B2 (b) can read**
- **B1 must read 1.** That 1 comes from A1, A3, or C2/C3 when c = 1.
- **0:** only if c = 0 and C2 or C3 writes 0 between B1 and B2.
- **1, 3, 2:** B2 reads one of A's writes. If c ≠ 0, b ≠ 0.

**Final value per (b, c) pair**

| b | c | Possible finals |
|---|---|---|
| 0 | 0 | 2, 0 (b = 0, so B3 and C3 both write 0) |
| 1 | 0 | 2 (A4 last), 1 (B3 last), 0 (C3 last) |
| 3 | 0 | 2, 3, 0 |
| 2 | 0 | 2, 0 |
| 1 | 1 | 2, 1 |
| 3 | 1 | 2, 3, 1 |
| 2 | 1 | 2, 1 |
| 1 | 3 | 2, 1, 3 |
| 3 | 3 | 2, 3 |
| 2 | 3 | 2, 3 |
| 1 | 2 | 1, 2 |
| 3 | 2 | 3, 2 |
| 2 | 2 | 2 |

When c = 2, C3 comes after A4, so the final value is set by B3 or C3.

BEGIN
0 0 2
0 0 0
1 0 2
1 0 1
1 0 0
3 0 2
3 0 3
3 0 0
2 0 2
2 0 0
1 1 2
1 1 1
3 1 2
3 1 3
3 1 1
2 1 2
2 1 1
1 3 2
1 3 1
1 3 3
3 3 2
3 3 3
2 3 2
2 3 3
1 2 1
1 2 2
3 2 3
3 2 2
2 2 2
END