I treated the rules as allowing every interleaving that preserves each thread's program order. Only the x-operations matter for the asked values. The values written to z and the read of y don't feed into any x-operation, so they can't change Q1, Q2, or Q3.

The x-writes are A4 (5), B1 (4), and C4 (1). A5 returns the latest of these before it, and A4 always precedes A5. C5 returns the latest of these before it, and C4 always precedes C5. The final x is the latest of the three writes overall. Enumerating the 6 orders of A4, A5, C4, C5 (with A4 before A5 and C4 before C5) and inserting B1 into each of the 5 gaps gives 30 orderings. They produce these 14 distinct (Q1, Q2, Q3) triples.

BEGIN
1 1 1
1 1 4
1 4 4
4 1 1
4 1 4
4 4 4
4 5 4
5 1 1
5 1 4
5 1 5
5 4 4
5 4 5
5 5 4
5 5 5
END