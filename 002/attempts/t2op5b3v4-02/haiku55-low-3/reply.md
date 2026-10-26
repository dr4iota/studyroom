Without sync points, all interleavings are allowed as long as each thread's own operations keep their order. Only the y-writes (B3 writes 4, then B4 writes 2) and the x-write (A1) matter for the asked values.

- **y over time:** it is 0 until B3, then 4 until B4, then 2. A2, A3, A4 read in order, so their phases never go backward. That allows (A3, A4) ∈ {(0,0), (0,4), (0,2), (4,4), (4,2), (2,2)}. The pairs (2,4), (4,0), and any pair decreasing in phase are impossible.
- **B2 (reads x):** it returns 3 if A1 takes effect before B2, and 0 otherwise. Both are possible.
- **Compatibility:** each (A3, A4) pair can be paired with each B2 value. For B2 = 0, B2 comes before A1 and B3 can be placed anywhere after it. For B2 = 3, A1 comes before B2 and B3 comes after B2, so B3 and B4 can still be placed among the reads freely. For example, (4,2) with B2 = 3 is realized by A1, B1, B2, B3, A2, A3, B4, A4, A5.

That gives 6 × 2 = 12 combinations, listed as Q1 Q2 Q3.

BEGIN
0 0 0
0 4 0
0 2 0
4 4 0
4 2 0
2 2 0
0 0 3
0 4 3
0 2 3
4 4 3
4 2 3
2 2 3
END