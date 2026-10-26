The three asked values are A1, B3, and B5. With no sync points, any interleaving that preserves each thread's order is possible, so I enumerated the feasible values of these reads.

- **A1** runs before any A write, so it can only see B's writes (0 or 1). It returns 0 if it runs before B1 and 1 if it runs after B1.
- **B3** sees B1 (1) and possibly A3 (2) and A4 (3). It can be 1, 2, or 3.
- **B5** sees B4 (1) and possibly A3 or A4, depending on where they fall relative to B4 and B5. It can be 1, 2, or 3.

For (B3, B5), checking each pair against the ordering constraints gives six feasible pairs: (1,1), (1,2), (1,3), (2,1), (2,3), (3,1). The pairs (2,2), (3,2), and (3,3) are impossible because they would require A3 or A4 to sit in a window that the ordering forbids.

Each of these six pairs is achievable with A1 = 0 (A1 runs first) and with A1 = 1 (A1 runs right after B1, before A3). That gives 12 combinations.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END