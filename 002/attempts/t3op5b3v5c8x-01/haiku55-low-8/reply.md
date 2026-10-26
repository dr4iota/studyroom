Each combination is (Q1, Q2, Q3) = (value of B5, value of C4, final y). I found 21 by enumerating the interleavings of the 15 operations (each thread's order preserved) and checking every value against the rules. With no sync points given, every interleaving that respects program order is allowed. Two combinations are impossible: `2 0 1` and `1 0 2`.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END