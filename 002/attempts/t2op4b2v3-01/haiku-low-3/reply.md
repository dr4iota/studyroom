The write sequence seen by the reads is 0, 3, 2, 1. Each thread's operations take effect in program order, so A1 ≤ A2 ≤ A4 in effect time, and B's writes take effect in order 3, 2, 1. With no sync points, any interleaving of A's reads with B's writes is possible. Each read sees the latest write before it, so the reads see a nondecreasing position in the sequence 0, 3, 2, 1. Every nondecreasing choice of positions for A1, A2, A4 is achievable, which gives C(6,3) = 20 combinations.

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