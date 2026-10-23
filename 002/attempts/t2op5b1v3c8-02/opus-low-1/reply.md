The writes to x alternate between A and B, so I worked through every interleaving of the two threads. The analysis splits on whether B4 takes effect after or before A5.

**Case 1: B4 takes effect after A5.** B4 is then the last write, so the final value of x is whatever B2 read.
- A3 must run before B4, so A3 sees A2's write and returns 1. A4 therefore writes 1.
- The values x holds on A's timeline are 0, then 3, then 1 (written by A2 and again by A4), then 2.
- B1, B2 and B3 read these values in non-decreasing time order.
- Each choice of positions for B1 ≤ B2 ≤ B3 gives the outcome (B1, B3, B2). The positions on the timeline are 0, 3, 1, 2 in that order.
- B1 reads 0:
  - B3 reads 0: (0 0 0).
  - B3 reads 3: (0 3 0), (0 3 3).
  - B3 reads 1: (0 1 0), (0 1 3), (0 1 1).
  - B3 reads 2: (0 2 0), (0 2 3), (0 2 1), (0 2 2).
- B1 reads 3: (3 3 3), (3 1 3), (3 1 1), (3 2 3), (3 2 1), (3 2 2).
- B1 reads 1: (1 1 1), (1 2 1), (1 2 2).
- B1 reads 2: (2 2 2).

**Case 2: B4 takes effect before A5.** A5 is then the last write, so the final value of x is 2.
- B3 comes before B4, and B4 comes before A5, so B3 cannot see the value 2.
- B3 also cannot see B4's own write, since B4 comes after it.
- If B4 lands between A2 and A3, A3 and A4 may copy B4's value. However, B1 and B3 both read before B4, so they still only see 0, 3 or 1.
- So B1 and B3 read from the sequence 0, 3, 1, with B1 at or before B3.
- That gives (0 0 2), (0 3 2), (0 1 2), (3 3 2), (3 1 2), (1 1 2).

BEGIN
0 0 0
0 3 0
0 3 3
0 1 0
0 1 3
0 1 1
0 2 0
0 2 3
0 2 1
0 2 2
3 3 3
3 1 3
3 1 1
3 2 3
3 2 1
3 2 2
1 1 1
1 2 1
1 2 2
2 2 2
0 0 2
0 3 2
0 1 2
3 3 2
3 1 2
1 1 2
END