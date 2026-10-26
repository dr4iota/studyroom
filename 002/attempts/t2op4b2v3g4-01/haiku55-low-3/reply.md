Each thread's effects happen in program order, so the possible executions are the interleavings of A2, A3, A4 with B2, B3, B4. B1 must come before A4, which is always achievable by placing B1 first. That gives 20 interleavings. Each read returns the last write before it (0 if none), and the final x is 2 if A4 is the last write to x, otherwise 1. Removing duplicates leaves 16 distinct outcomes.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
END