The reachable outcomes are the 32 combinations below. Only the y-operations matter (A1, B1, B3, B5, C2, C3, C4), since x and z never affect y. Each thread's operations take effect in listed order, and there are no sync points, so every merge of the three threads is allowed. I enumerated the write orders and where each read falls among them.

BEGIN
1 0 0
1 1 0
1 4 0
1 5 0
4 0 0
4 4 0
4 5 0
5 0 0
5 4 0
5 5 0
0 0 0
1 1 1
1 4 1
1 5 1
4 1 1
4 4 1
4 5 1
5 1 1
5 4 1
5 5 1
1 0 4
1 1 4
1 4 4
1 5 4
0 0 4
0 4 4
4 4 4
4 5 4
5 0 4
5 1 4
5 4 4
5 5 4
END