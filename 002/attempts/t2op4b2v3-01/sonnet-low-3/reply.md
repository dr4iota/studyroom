Thread B's writes take effect in the order 3, 2, 1, so x passes through the values 0, 3, 2, 1 in that order.

Thread A's reads run one after another, so each read sees the same point in this sequence as the previous read, or a later one. So A1, A2, A3 and A4 return values at non-decreasing positions in the sequence 0, 3, 2, 1.

A3 is not asked about. For any positions chosen for A2 and A4, A3 can take the same position as A2, so it never rules anything out. The possible combinations are therefore every non-decreasing triple of positions for (A1, A2, A4), which gives 20 triples. Mapping positions to values (position 0 → 0, 1 → 3, 2 → 2, 3 → 1) gives the list below.

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