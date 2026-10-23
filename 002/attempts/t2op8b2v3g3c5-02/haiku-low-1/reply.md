The possible outcomes are the 13 combinations below. Every x-write stores a value read from x, and x starts at 0, so x is always 0. A2 reads y = 2, which forces B4 to take effect before A2. The remaining reads and final y depend only on how the A4, A5, A7 writes and reads interleave with B5, B6, B7. Enumerating the 20 possible interleavings gives these (A7, B6, final y) outcomes.

Asked values, in order: Q1 = A7, Q2 = B6, Q3 = final y.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 3 0
0 3 2
0 3 3
2 0 2
2 2 2
2 3 2
3 0 3
3 3 3
END