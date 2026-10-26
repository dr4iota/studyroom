I enumerated every interleaving that respects each thread's program order, with reads returning the latest earlier write. The key constraints are:

- **y** is only written by A3 (value 4), and A2 comes before A3, so A2 always reads 0. C3 reads 0 or 4, depending on whether A3 has already happened.
- **x** is written by B1 (4), C1 (3), and C4 (the value C3 read, so 0 or 4). A1 and C2 both read 3, so C1 must be the last x-write before each, with no B1 or C4 in between.
- **A4** can read 3 (from C1), 4 (from B1, or from C4 when C3 read 4), or 0 (only from C4 when C3 read 0).

Feasible (A4, C3) pairs, each with a witnessing order:
- (3, 0): B1, C1, A1, C2, A2, C3, A3, A4, C4
- (3, 4): B1, C1, A1, C2, A2, A3, C3, A4, C4
- (4, 0): C1, A1, C2, A2, C3, C4, B1, A3, A4
- (4, 4): C1, A1, C2, A2, A3, C3, B1, C4, A4
- (0, 0): B1, C1, A1, C2, A2, C3, C4, A3, A4

So Q1 is always 0, Q2 is 0, 3, or 4, and Q3 is 0 or 4.

BEGIN
0 3 0
0 3 4
0 4 0
0 4 4
0 0 0
END