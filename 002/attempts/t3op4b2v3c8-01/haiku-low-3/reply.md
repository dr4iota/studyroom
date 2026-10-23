Each read returns the latest write to its block before it in one global order that keeps each thread's operations in sequence. The reachable values are determined by how the reads of y (A1, B3, C1) interleave with the writes B2 (writes 2) and C4 (writes the value C3 read from x). Working through the orderings, C1 is either 0 or 2, and A1 and B3 can each be 0, 2, or 3. Fifteen of the 18 combinations are reachable. The three excluded ones are (A1, B3, C1) = (2, 0, 2), (3, 0, 2), and (3, 0, 0).

BEGIN
0 0 0
0 2 0
0 3 0
2 0 0
2 2 0
2 3 0
3 2 0
3 3 0
0 0 2
0 2 2
0 3 2
2 2 2
2 3 2
3 2 2
3 3 2
END