Thread B's writes take effect in the order 3, then 2, then 1, so x passes through the states 0, 3, 2, 1 over time. Thread A's reads take effect in order, so the states they observe can only move forward through that sequence. Each read can see any state, as long as the states seen by A1, A2, and A4 are non-decreasing in that order. Every such choice is achievable by placing the reads between the write instants. A3 is not asked, so it doesn't constrain the answer.

Mapping states to values: index 0 gives 0, index 1 gives 3, index 2 gives 2, index 3 gives 1. The 20 non-decreasing index triples (i1 ≤ i2 ≤ i4) give these distinct value triples:

BEGIN
0 0 0
0 0 3
0 0 2
0 0 1
0 3 3
0 3 2
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 2
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END