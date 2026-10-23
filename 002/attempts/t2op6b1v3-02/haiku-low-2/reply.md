Every outcome is an interleaving of the two threads' writes, with reads taking the last write before them. Because B3 always precedes B4 in program order, B4 can only see B3 or an A-write that lands between B3 and B4. Final x is either 1 (B5 is last) or 2 (A5 is last). Enumerating the placements gives 14 distinct outcomes.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END