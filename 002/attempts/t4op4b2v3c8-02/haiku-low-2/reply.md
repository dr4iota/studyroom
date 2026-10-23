The outcomes are the same for all 27 combinations of the three values, so every value in {0, 2, 3} is possible for each of Q1, Q2, and Q3.

**Why only 0, 2, 3 appear:** The only values ever written are 2, 3, and copies of values read earlier. Every read returns either 0 (no prior write) or a value from {2, 3}, so the reads and copies can only carry 0, 2, or 3.

**Final x (Q2):** The last write to x is one of A1 (2), B4 (copy of B1), C3 (2), or D4 (3). C2 can never be last because C3 follows it, and D1 and D3 can never be last because D4 follows them. The possible results are 0, 2, and 3.

**Final y (Q3):** The last write to y is one of A2 (2), B2 (copy of B1), or D2 (3). The possible results are 0, 2, and 3.

**A3 (Q1):** A3 reads the last write to x before it, which can be 0 (via C2 or B4 carrying 0), 2, or 3.

**Witnesses:** For each of the 27 combinations I built an explicit interleaving that respects each thread's order. Examples:
- (0, 0, 0): B1, A1, A2, D1, D2, B2, B3, C1, C2, C3, D3, D4, B4, A3
- (0, 2, 0): C1, A1, B1, A2, D1, D2, C2, A3, B2, B3, B4, D3, D4, C3
- (3, 2, 2): A1, C1, C2, A2, B1, D1, D2, B2, B3, B4, D3, D4, A3, C3
- (2, 3, 0): B1, A1, A2, A3, D1, D2, B2, B3, B4, C1, C2, C3, D3, D4

I checked each witness by tracing the read values and the last writes. I did not run a program to search the interleavings, so this rests on the constructions and the case analysis above.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END