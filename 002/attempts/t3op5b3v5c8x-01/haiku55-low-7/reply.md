The three asked values are B5's return (Q1), C4's return (Q2), and the final value of y (Q3). With no sync points, any interleaving that respects each thread's program order is allowed. I enumerated by the value A1 reads from z (which fixes what A2, A3, and A4 write), then checked which (B5, C4) pairs and y-outcomes can coexist with the orderings of B1, C1, C2, B2, B3, and A4.

Key facts:
- B5 and C4 can only read 1 or 2 when A1 reads 1 or 2, and 0 is possible only when A1 reads 0.
- A1 reads 0, 1, or 2, and the final y is whichever of A4 (value A1 read) and B3 (value B2 read) takes effect later.
- Some pairs are impossible: (B5, C4) = (2, 1) cannot occur when A1 reads 0, and (2, 0) only occurs when A1 reads 0.

Each feasible (Q1, Q2) pair with its possible Q3 values gives:

- (0, 0): Q3 ∈ {0, 1}
- (0, 1): Q3 ∈ {0, 1}
- (0, 2): Q3 ∈ {0, 1}
- (1, 0): Q3 ∈ {0, 1}
- (1, 1): Q3 ∈ {0, 1, 2}
- (1, 2): Q3 ∈ {0, 1, 2}
- (2, 0): Q3 = 0
- (2, 1): Q3 ∈ {0, 1, 2}
- (2, 2): Q3 ∈ {0, 1, 2}

This gives 21 combinations.

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