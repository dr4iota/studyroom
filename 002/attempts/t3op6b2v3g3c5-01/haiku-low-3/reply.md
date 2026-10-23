I found 14 possible outcomes. Q1 (A1's value) is 0, 2, or 3. Q2 (C2's value) is 0, 2, or 3, but Q2 = 0 is possible only when Q1 = 0, because A5 must be the last write before C2. Q3 (C4's value) is 0 or 2, and it is independent of the others because B5 can be placed freely relative to C4. Each feasible (Q1, Q2) pair was checked with an explicit interleaving, and each can be combined with either Q3 value.

Feasible (Q1, Q2) pairs: (0,0), (0,2), (0,3), (2,2), (2,3), (3,2), (3,3). The pairs (2,0) and (3,0) are impossible.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END