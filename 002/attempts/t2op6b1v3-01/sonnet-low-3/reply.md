Only one thread's reads can be affected by the other's writes, so I split on B1.

**Writes to x.** B writes 1, 2, 3, 1 in order (B2 to B5). A5 writes 1, but only after A4 has finished. A's reads therefore only ever see the value sequence from B's writes: 0, 1, 2, 3, 1.

**B1.** B1 runs before any of B's writes, so it returns either 0 or 1.
- B1 can return 1 only if A5 has already written 1. That requires A1 to A4 to have finished before B1, with no B write yet, so A2 = 0 and A4 = 0.
- B1 = 0 is possible with any placement of A's reads, since B1 can run first.

**A2 and A4.** A2 is read before A4, so they see positions i ≤ j in the sequence 0, 1, 2, 3, 1.
- i = 0: (0,0), (0,1), (0,2), (0,3)
- i = 1: (1,1), (1,2), (1,3)
- i = 2: (2,2), (2,3), (2,1)
- i = 3: (3,3), (3,1)
- i = 4: (1,1)

This gives 12 distinct pairs, all possible with B1 = 0. The extra case is B1 = 1 with (A2, A4) = (0, 0).

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 1 0
2 2 0
2 3 0
3 1 0
3 3 0
0 0 1
END