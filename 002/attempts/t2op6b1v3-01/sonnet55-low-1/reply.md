Only the values A2, A4 and B1 return matter, so the analysis tracks the sequence of values x takes.

**B1.** B1 is B's first operation, so B2–B5 all happen after it. The only write that can precede B1 is A5, which writes 1. So B1 returns 0 or 1.

**Case B1 = 1.** A5 took effect before B1. A5 comes after A1–A4 in thread A, so A1–A4 all took effect before A5. At that point nothing has been written, because B's writes come after B1, which comes after A5. So A2 = 0 and A4 = 0. This gives (0, 0, 1).

**Case B1 = 0.** A5 is after B1, or at least cannot affect A2 and A4, since both finish before A5. B's writes make x take these values in order: 0, 1 (B2), 2 (B3), 3 (B4), 1 (B5). A2 takes effect before A4, so they read states at positions i ≤ j in that sequence. The pairs (A2, A4) are:
- From state 0: (0,0), (0,1), (0,2), (0,3)
- From state 1 (value 1): (1,1), (1,2), (1,3)
- From state 2 (value 2): (2,2), (2,3), (2,1)
- From state 3 (value 3): (3,3), (3,1)
- From the last state (value 1): (1,1), already listed

Each of these is achievable with B1 = 0, since the A reads can be placed anywhere relative to B1's read.

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