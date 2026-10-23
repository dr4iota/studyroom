Thread B's writes take effect in the order B1, B2, B3. Over time, x therefore goes through the values 0, 3, 2, 1. Call these positions 0, 1, 2, 3.

Thread A's reads happen in order, so each read sees a position at least as late as the previous read's. Nothing forces any particular overlap between the threads, so every non-decreasing choice of positions for A1, A2, A3, A4 is achievable.

A3's value is not asked about. It can always be placed at the same position as A2, so it adds no constraint. That leaves the non-decreasing position triples (A1, A2, A4), of which there are C(6,3) = 20. Mapping positions back to values (0→0, 1→3, 2→2, 3→1) gives the combinations below.

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