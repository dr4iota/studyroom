All 27 combinations are possible. No sync points are given, so any interleaving that keeps each thread's order is allowed.

**Possible values**
- **A3** runs after A1. It can return 2 (from A1, C3 or D1), 3 (from D3 or D4), or 0. A 0 comes from B4 when B1 read 0, or from C2 when C1 read 0 (C1 before A1 and D1).
- **Final x** is set by whichever write to x lands last. That can be A1 or C3 (2), D4 (3), or B4. B4 writes whatever B1 read, which is 0, 2 or 3.
- **Final y** is set by the last of A2 (2), D2 (3) and B2. B2 writes whatever B1 read.

**Final y = 0.** B1 runs before A2 and D2 and reads 0. B2 then runs after both A2 and D2 and writes 0, so it is the last write to y. B4 comes after B2.
- Final x = 0: B4 is last. A3 can read before B4 and see 2 (A1 or D1) or 3 (D3 or D4). It can also run after B4 and read 0.
- Final x = 2 or 3: C3 or D4 runs last. A3 can still read 0, 2 or 3 before that, for example 0 right after B4.

So all 9 combinations with y = 0 are possible.

**Final y = 2.** A2 is the last write to y.
- Final x = 0: B1 reads 0 early, and B4 writes 0 last.
- Final x = 2: A1 or C3 writes last.
- Final x = 3: D4 writes last.
- In each case A3 can be placed to read 0, 2 or 3 by the same reasoning as above.

**Final y = 3.** D2 is the last write to y. Final x and A3 work the same way as for y = 2.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END