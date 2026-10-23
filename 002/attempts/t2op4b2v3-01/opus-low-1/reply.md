Thread B's writes take effect in order, so x goes through the values 0, 3, 2, 1, in that order. Each of A's reads returns one of these values. Because A's reads are also sequential, each read sees the same point in this sequence as the previous read or a later one. It can never see an earlier point.

**Index each value by its position:** 0 → position 0, 3 → position 1, 2 → position 2, 1 → position 3.

**Constraint:** If A1, A2 and A4 see positions i, j and k, then i ≤ j ≤ k. A3 lies between A2 and A4, so it adds no further constraint.

**Result:** Any non-decreasing triple of positions from {0, 1, 2, 3} is achievable by timing the reads between the writes. There are C(6,3) = 20 such triples. Converting each position back to its value gives the list below.

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