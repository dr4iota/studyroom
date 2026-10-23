Writes to x occur as B2 (3), B3 (2), B4 (1) in that order, with A4 (2) inserted somewhere among them. B1 reads 0, so it must take effect before every write. A2 and A3 must take effect in order and before A4.

- If A4 is placed after k of the B writes (k = 0 to 3), the final x is 2 only when k = 3 (A4 last) and 1 otherwise.
- A2 and A3 can each see any prefix of the B writes up to k, so their values come from {0, 3, 2, 1} for prefixes of length 0, 1, 2, 3, with A2's prefix no longer than A3's.

This gives 6 combinations with final x = 1 (k = 0, 1, 2) and 10 combinations with final x = 2 (k = 3).

BEGIN
0 0 1
0 2 1
0 3 1
2 2 1
3 2 1
3 3 1
0 0 2
0 1 2
0 2 2
0 3 2
1 1 2
2 1 2
2 2 2
3 1 2
3 2 2
3 3 2
END