Since there are no sync points, the only constraints are program order within each thread and B1 reading 0 (always satisfiable since A4 only writes a nonzero value after B2 has taken effect, which is after B1).

x's history from B is 0 → 3 → 2 → 1. A2 reads one of these, A3 reads the same or a later value, and A4 writes A3's value. The final x is 1 if B4 lands after A4, otherwise A3's value (A4 can be delayed arbitrarily, so A3's value is always achievable as final; and 1 is always achievable too).

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END