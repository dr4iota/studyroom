Because there are no sync points and every operation takes effect at a single instant, the possible executions are exactly the interleavings of the three threads that keep each thread's own order.

**A1 (read x).** x is written by B2 (1), C1 (2) and A5 (2), and A5 comes after A1. So A1 can return 0, 1 or 2.

**Where the values in y can come from.**
- The value 0 is written only by A3, and only when A1 returned 0. So B4 = 0 or C4 = 0 requires A1 = 0.
- The value 2 is written by C2, by A3 (when A1 = 2), and by B5 or C5 (copies of what B4 or C4 read).
- The value 3 is written by B1 and A4.

**B4 = 3.** B4 comes after B3, which overwrites B1's 3. So the 3 must come from A4, and A3 must have run before A4.

**Constraints on the pairs.**
- **B4 = 0:** this needs A1 = 0, and A3 must land after B3 and before B4.
- **C4 = 0:** this needs A1 = 0, and A3 must be the last write before C4.
- **B4 = 2:** this is always possible, via C2 landing between B3 and B4.
- **C4 = 2:** C2 comes before C3, so the 2 has to come from A3 (A1 = 2) or from B5 (B4 = 2). So C4 = 2 requires A1 = 2 or B4 = 2.
- **B4 = 0 and C4 = 2:** impossible. B4 = 0 forces A1 = 0 (no 2 from A3), and B5 would write 0, not 2.
- **B4 = 3 and C4 = 0:** impossible. A4 must precede B4, which overwrites A3's 0, and A3 is the only source of 0.

**Feasible combinations by A1.**
- **A1 = 0:** (B4, C4) can be (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,1), (0,3), (1,3), (2,3), (3,3) or (2,2).
- **A1 = 1:** B4 and C4 are both in {1,2,3}, except that C4 = 2 needs B4 = 2. This gives (1,1), (2,1), (3,1), (1,3), (2,3), (3,3) and (2,2).
- **A1 = 2:** B4 and C4 are both in {1,2,3}, with no further restriction. C4 = 2 works for every B4, using A3 with value 2, and all 9 combinations are achievable.

BEGIN
0 0 0
0 1 0
0 2 0
0 0 1
0 1 1
0 2 1
0 3 1
0 0 3
0 1 3
0 2 3
0 3 3
0 2 2
1 1 1
1 2 1
1 3 1
1 1 3
1 2 3
1 3 3
1 2 2
2 1 1
2 2 1
2 3 1
2 1 2
2 2 2
2 3 2
2 1 3
2 2 3
2 3 3
END