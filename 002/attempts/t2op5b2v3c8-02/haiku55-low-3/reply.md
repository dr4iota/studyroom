I modeled each execution as a total order of effect instants that keeps each thread's operations in program order. A3 can only see B1 and B2, since A4 comes after it. B3 and B4 always see B2 and can see A4's write, so their values are 3 or a1. Enumerating where A1, A3, and A4 fall among B1 through B4 gives these combinations of (A3, B3, B4):

BEGIN
0 3 3
1 3 3
0 0 0
1 0 0
3 0 0
1 1 1
3 1 1
3 3 3
0 3 0
1 3 0
3 3 0
1 3 1
3 3 1
END