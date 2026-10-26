x goes through values 0 → 3 → 2 → 1 over time (monotone in sequence order). A's reads A1 ≤ A2 ≤ A3 ≤ A4 in time, so the values read are a non-decreasing sequence of positions in [0,3,2,1]. Q1, Q2, Q3 = A1, A2, A4 values with A1 ≤ A2 ≤ A4 in position order (A3 is unconstrained in between).

Positions: 0(0),1(3),2(2),3(1). All triples (p1,p2,p4) with p1 ≤ p2 ≤ p4.

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