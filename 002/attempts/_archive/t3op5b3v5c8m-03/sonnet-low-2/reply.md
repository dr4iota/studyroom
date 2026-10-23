Every interleaving of the three threads' operations that keeps each thread's own order is possible. Only x, y and z matter, and they can only hold these values.

- x can only be written with 2 (A1) or with B's read of y (B4). y only ever holds values copied from x, so x and y are always 0 or 2.
- z is written either with 3 (C1) or with A3's read of y, so z ends as 0, 2 or 3.

**Q1: B1.** B1 reads x, which only A1 and B4 can write. B4 comes after B1, so B1 returns 0 if it runs before A1 and 2 if it runs after A1.

**Q2: final x.** The last write to x is A1 (value 2) or B4 (value b2, B2's read of y).
- To end with x = 0, A1 must come before B4 and B2 must read y = 0. For example: B1, A1, B2, B3, B4 gives b1 = 0 and x = 0. With A1, B1, B2, B3, B4 we get b1 = 2 and x = 0, since B2 still reads y = 0 before B3 writes 2.
- To end with x = 2, either B4 runs before A1, or B2 reads 2.

**Q3: final z.** The last write to z is C1 (3) or A4 (A3's read of y).
- z = 3: C1 runs after A4.
- z = 0: C1 runs before A4, and A3 reads y = 0.
- z = 2: C1 runs before A4, and A3 reads y = 2. For b1 = 0, y = 2 needs C to write 2, which happens when C2 reads x = 2 after A1. For b1 = 2, B3 writes 2 to y.

**Combinations of Q1, Q2, Q3.** Every choice of B1 ∈ {0,2}, x ∈ {0,2}, z ∈ {0,2,3} can be realized, giving all 12 combinations. One witness for each hard case:
- b1 = 0, x = 0, z = 2: B1, A1, B2, C1, C2 (reads 2), C3 (y = 2), A2, A3, A4 (z = 2), B3 (y = 0), B4 (x = 0).
- b1 = 2, x = 0, z = 0: C1, A1, B1, B2 (reads 0), A2, A3, A4 (z = 0), B3, B4 (x = 0), C2 and the rest.
- b1 = 2, x = 2, z = 2: A1, B1, B3 (y = 2), B2 (reads 2), A2, A3, A4, B4 (x = 2), with C1 earlier.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END