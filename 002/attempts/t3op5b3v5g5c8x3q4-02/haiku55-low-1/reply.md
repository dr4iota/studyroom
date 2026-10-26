Every thread's operations take effect in program order, and there are no sync points, so the possible executions are all interleavings of the three threads' operations that keep each thread's order. The known results (A1 = 3, C2 = 3) constrain which interleavings are valid.

**Key facts:**
- **Q1 (A2) is always 0.** Only A3 writes y, and A3 always comes after A2 in thread A.
- **C3 (Q3)** reads y, so it is 4 if A3 takes effect before C3, otherwise 0.
- **C4** writes C3's value to x. So the x-writes are B1 (4), C1 (3), and C4 (0 or 4).
- **A1 = 3** forces C1 to be the last x-write before A1. This means C4 must come after A1, and B1 must not fall between C1 and A1.
- **C2 = 3** forces B1 not to fall between C1 and C2.
- **A4 (Q2)** can be 3 (C1 is the last x-write), 4 (B1 or C4 with value 4 is last), or C3's value (0 or 4, only if C4 is last). Since C4 writes 4 whenever Q3 = 4, A4 can never be 0 in that case.

**Valid executions (examples):**
- (0, 0, 0): C1, A1, C2, C3, C4, A2, A3, A4 with B1 before C1.
- (0, 3, 0): C1, A1, C2, C3, A2, A3, A4, C4 with B1 before C1.
- (0, 4, 0): C1, A1, C2, C3, A2, A3, B1, A4, C4.
- (0, 3, 4): C1, A1, C2, A2, A3, C3, A4, C4.
- (0, 4, 4): C1, A1, C2, A2, A3, C3, C4, A4.

Impossible combinations include any with Q3 = 4 and Q2 = 0, since C4 would write 4 and no other write can leave x at 0 after C1.

BEGIN
0 0 0
0 3 0
0 4 0
0 3 4
0 4 4
END