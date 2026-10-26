I modeled this as an interleaving of the two threads' operations, with each operation taking effect at its own instant and each thread's order preserved. The final value of x is 2 unless B4 takes effect after A5, in which case it is b2. A3 reads b2 only if B4 falls between A2 and A3. This gives 26 distinct outcomes.

Outcomes are listed as (Q1, Q2, Q3) = (b1, b3, final x).

BEGIN
0 0 0
0 3 0
0 1 0
0 2 0
0 3 3
0 1 3
0 2 3
3 3 3
3 1 3
3 2 3
0 1 1
0 2 1
3 1 1
3 2 1
1 1 1
1 2 1
0 2 2
3 2 2
1 2 2
2 2 2
0 0 2
0 3 2
0 1 2
3 3 2
3 1 2
1 1 2
END