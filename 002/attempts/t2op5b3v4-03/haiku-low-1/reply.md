Each thread's writes are constants and no operation depends on another's result, so any interleaving that preserves each thread's order is valid. Each read's value depends only on which writes precede it:

- **A1 (read z)** sees the last of B1 (writes 3) or B3 (writes 2) that precedes it, or 0 if neither does. So it can return 0, 3, or 2.
- **A5 (read y)** returns 4 if B5 precedes it, otherwise 0.
- **B4 (read x)** returns 1 if A4 precedes it, otherwise 0.

All 3 × 2 × 2 = 12 combinations are achievable. For example:
- `2 4 0`: B1, B2, B3, A1, B4, B5, A2, A3, A4, A5
- `3 0 1`: B1, A1, A2, A3, A4, A5, B2, B3, B4, B5
- `0 4 1`: A1, A2, A3, A4, B1, B2, B3, B4, B5, A5 (B4 reads x=1 because A4 precedes it; A5 reads y=4 because B5 precedes it)

Values are listed as Q1 Q2 Q3.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
2 0 0
2 0 1
2 4 0
2 4 1
3 0 0
3 0 1
3 4 0
3 4 1
END