The asked values are Q1 = B2's return, Q2 = C1's return, and Q3 = the final value of x. I worked this out by hand by checking which orderings of the writes are consistent with B1 returning 1.

Key facts:
- A's writes always occur in the order 1, 3, 1, 2, so the final value is one of 2 (A4 last), the value of B3 (B3 last), or the value of C3 (C3 last).
- The value 0 can only be read or written if C1 returns 0 (no writes before C1), so the value 0 in B2 requires C1 to return 0.
- For each achievable (Q1, Q2) pair, I checked which of the three possible last writers can come last without breaking the order constraints.

This gives 29 combinations.

BEGIN
0 0 0
0 0 2
1 0 0
1 0 1
1 0 2
1 1 1
1 1 2
1 2 1
1 2 2
1 3 1
1 3 2
1 3 3
2 0 0
2 0 2
2 1 1
2 1 2
2 2 2
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 1 1
3 1 2
3 1 3
3 2 2
3 2 3
3 3 2
3 3 3
END