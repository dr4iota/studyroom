**Key facts**

- y is never written, so A1 always returns 0. It places no constraint on the other operations.
- B1 returns 0, which only requires B1 to take effect before B2. Thread order already guarantees this.
- The writes to x take effect in the order 0 (initial), 3 (B2), 2 (B3), 1 (B4).
- A2 starts above the sync line, so its start has no constraint. Only its end must come after P. Its effect can be anywhere before that end, even before P. So A2 can return any of 0, 3, 2, 1.
- A3 takes effect after A2. So A3 returns the same value as A2 or a later one in the order 0 → 3 → 2 → 1.
- A4 writes A3's value back to x:
  - If A4 takes effect after B4, the final x equals A3's value.
  - If A4 takes effect before B4, B4 overwrites it and the final x is 1. This needs A3 to have read before B4, so A3's value is not 1.
  - If A3 read 1, then B4 is already done and the final x is 1.

**Combinations**

| A2 | A3 | Final x |
|----|----|---------|
| 0 | 0 | 0 or 1 |
| 0 | 3 | 3 or 1 |
| 0 | 2 | 2 or 1 |
| 0 | 1 | 1 |
| 3 | 3 | 3 or 1 |
| 3 | 2 | 2 or 1 |
| 3 | 1 | 1 |
| 2 | 2 | 2 or 1 |
| 2 | 1 | 1 |
| 1 | 1 | 1 |

For example, the first row with final x = 0 needs A2, A3 and A4 all to take effect before B2, with A2's end after P. That is allowed.

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END