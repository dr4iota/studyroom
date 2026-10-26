Let the write instants be w3 < w2 < w1 (B1, B2, B3), and the read instants be r1 < r2 < r3 < r4 (A's reads run one at a time). Each read returns the value of the latest write before it, so as the reads proceed, the value seen moves through the sequence 0, 3, 2, 1 without going back. Any non-decreasing choice of stages for A1, A2, and A4 can be realized by placing the reads between the writes, and A3 can go anywhere in between. That gives 20 combinations.

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