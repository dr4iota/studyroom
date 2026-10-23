I enumerated every interleaving of the two threads' operations that keeps program order and makes B3 return 3. Invalid interleavings are those where A2 (writing 2) is the last x-write before B3, which happens only when A2 falls between B2 and B3 and A5 falls after B3. For each valid interleaving I computed A1, A4, and the final value of y.

The distinct outcomes (Q1 Q2 Q3) are:

BEGIN
0 0 0
1 1 1
3 3 3
1 1 0
3 3 0
0 2 0
1 2 1
3 2 3
1 2 0
3 2 0
1 0 0
3 0 0
END