There are no sync points, so the only constraints are program order within each thread. Each thread's operations take effect in listed order, and the two threads interleave in any of C(6,3) = 20 ways.

Writes: A1 writes 1, B2 writes 3, B3 writes 2. Each read returns the most recent write that took effect before it.

- **A2** returns 2 if B3 precedes it, else 3 if B2 precedes it, else 1 (A1 always precedes A2).
- **A3** follows the same rule, applied at its own position. Since A3 comes after A2, its value is never earlier than A2's.
- **B1** returns 1 if A1 precedes it, else 0.

Going through all 20 interleavings gives these (A2, A3, B1) results:

| Interleaving (order) | A2 A3 B1 |
|---|---|
| A1 A2 A3 B1 B2 B3 | 1 1 1 |
| A1 A2 B1 A3 B2 B3 | 1 1 1 |
| A1 A2 B1 B2 A3 B3 | 1 3 1 |
| A1 A2 B1 B2 B3 A3 | 1 2 1 |
| A1 B1 A2 A3 B2 B3 | 1 1 1 |
| A1 B1 A2 B2 A3 B3 | 1 3 1 |
| A1 B1 A2 B2 B3 A3 | 1 2 1 |
| A1 B1 B2 A2 A3 B3 | 3 3 1 |
| A1 B1 B2 A2 B3 A3 | 3 2 1 |
| A1 B1 B2 B3 A2 A3 | 2 2 1 |
| B1 A1 A2 A3 B2 B3 | 1 1 0 |
| B1 A1 A2 B2 A3 B3 | 1 3 0 |
| B1 A1 A2 B2 B3 A3 | 1 2 0 |
| B1 A1 B2 A2 A3 B3 | 3 3 0 |
| B1 A1 B2 A2 B3 A3 | 3 2 0 |
| B1 A1 B2 B3 A2 A3 | 2 2 0 |
| B1 B2 A1 A2 A3 B3 | 1 1 0 |
| B1 B2 A1 A2 B3 A3 | 1 2 0 |
| B1 B2 A1 B3 A2 A3 | 2 2 0 |
| B1 B2 B3 A1 A2 A3 | 1 1 0 |

That leaves 12 distinct combinations of (Q1, Q2, Q3), where Q1 = A2, Q2 = A3, Q3 = B1. Values 1 and 2 never appear for A3 with A2 = 3, and A2 = 2 forces A3 = 2, as expected from the monotonic order of writes.

BEGIN
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
END