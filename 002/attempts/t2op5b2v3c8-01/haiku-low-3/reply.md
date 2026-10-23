I modeled this as all interleavings of the two threads' operations that respect each thread's program order, with each read returning the latest write before it. Because `y` is written only once, by A4, the final `y` equals the value A3 read. I found 12 outcomes, and each one has a schedule that produces it.

Reads of x by B1 and B2 can only see 0, 3 (A1), or 1 (A2), since B's own writes come after both reads. A3 reads the most recent of A2, B3, or B4 that precedes it. I checked each achievable (b1, b2) pair against the possible positions of B3, B4, and A3 to find the values of y.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 3 0
0 3 1
0 3 3
1 1 1
3 1 1
3 1 3
3 3 1
3 3 3
END