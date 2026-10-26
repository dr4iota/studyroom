The answer is 25 combinations. Writes to x come from A2 (value 2), B3 and B4 (value b), and C4 (value c). Since b is 1 or 2, c is 0, 1, or 2, and the final value of x is the last of these to take effect. Q1, Q2, and Q3 were enumerated by the order of the x-writes and the position of A1, B1, B2, and C2 relative to them. Each listed combination has a schedule that achieves it. The two excluded combinations (Q1=1, Q3=2 with Q2 = 0 or 2) are impossible: a value of 1 at A3 forces b=1, and then final value 2 forces c=2, which forces Q2=1.

BEGIN
0 0 0
0 1 0
0 2 0
1 0 0
1 1 0
1 2 0
2 0 0
2 1 0
2 2 0
0 0 1
0 1 1
0 2 1
1 0 1
1 1 1
1 2 1
2 0 1
2 1 1
2 2 1
0 0 2
0 1 2
0 2 2
1 1 2
2 0 2
2 1 2
2 2 2
END