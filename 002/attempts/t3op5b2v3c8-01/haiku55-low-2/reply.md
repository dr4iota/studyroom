All 27 combinations of values in {0, 2, 3} for (A1, A2, A3) are possible. No block ever holds 1, and every combination below has a schedule.

**Why these values:** The only writes of 3 and 2 come from B1, B2, and B3. Every other write copies a value that was already read, so the values stay in {0, 2, 3}.

**Why all 27 are reachable:** There are no sync points, so any interleaving that keeps each thread's order is allowed, and A's reads can be placed at any point. Each combination has a schedule. Some examples:

- **(0, x, y):** Put A1 first, when every block is 0. The remaining pattern for A2 and A3 is then free to match.
- **(3, 0, 0):** B2 (y=3), A1, A2, A3 all before B1.
- **(2, 2, 0):** C1 reads 0 first. Then B2, B3, A1 (y=2), B4, B5 (x=2), A2 (x=2), C2 (x=0), A3 (x=0). Returning x to 0 is only possible through C2, which needs C1 to have read 0 early.
- **(2, 3, 2):** B2, B3, A1 (y=2), B1 (x=3), A2 (x=3), B4, B5 (x=2), A3 (x=2).

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END