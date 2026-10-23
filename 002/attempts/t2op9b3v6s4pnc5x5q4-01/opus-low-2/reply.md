Thread B finishes B1–B8 before Thread A starts, and B9 can fall anywhere relative to Thread A.

**Fixed facts**
- Thread A's steps all come after Q. Thread B's steps B1–B8 all come before Q. So every operation of A happens after B8 ends.
- When B2 reads y, the only possible writer of y before it is A4, and A4 comes later. So B2 returns 0.
- Because B2 returned 0, B8 writes 0 to y and B9 writes 0 to x.
- When A starts, x = 4 (from B3) and y = 0 (from B8).
- A1 reads y = 0, and A2 writes 0 to z. Neither affects the asked values.
- A3, A5, A6 and A8 each read x. Each returns 4 if B9 has not yet taken effect, and 0 if it has. Once a read sees 0, every later read also sees 0.
- A4 is the last write to y, so the final y equals what A3 returned.

**Where B9 can fall**

| Position of B9 | A3 | A5 | A6 | A8 | Final y |
|---|---|---|---|---|---|
| before A3 | 0 | 0 | 0 | 0 | 0 |
| between A3 and A5 | 4 | 0 | 0 | 0 | 4 |
| between A5 and A6 | 4 | 4 | 0 | 0 | 4 |
| between A6 and A8 | 4 | 4 | 4 | 0 | 4 |
| after A8 | 4 | 4 | 4 | 4 | 4 |

BEGIN
0 0 0 0
0 0 0 4
4 0 0 4
4 4 0 4
4 4 4 4
END