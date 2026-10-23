Let the effect times be a1 < a2 < ... < a5 for thread A and b1 < ... < b5 for thread B.

**Constraints:**
- B1 returned 0, so b1 precedes every write to x (b2, b3, b4, a5).
- A2 returned 0, and A3 is the only write to z, so a2 < a3.
- B5 returned 4, so a3 < b5. This places no constraint on the x-reads except through the thread order.
- Within thread A, a1 < a4 < a5.

**Possible orders of the x-writes:** b2 < b3 < b4 are fixed, and a5 can go in any of four slots:
- W1: a5, b2, b3, b4 → values 3,2,1,2, final x = 2
- W2: b2, a5, b3, b4 → values 2,3,1,2, final x = 2
- W3: b2, b3, a5, b4 → values 2,1,3,2, final x = 2
- W4: b2, b3, b4, a5 → values 2,1,2,3, final x = 3

**Read values:** a1 and a4 must both occur before a5, and a1 ≤ a4. Each read sees the value of the last write before it, so each read falls into one of the segments before a5. The segments before a5 have these values:
- W1: 0 only.
- W2: 0, then 2.
- W3: 0, 2, 1.
- W4: 0, 2, 1, 2.

Schedules where a3 and b5 are placed late (or a2 and a1 early) never restrict these segments, so every ordered pair of segments (a1's segment ≤ a4's segment) is achievable.

**Collecting the (Q1, Q2) pairs:**
- Final x = 2 (W1, W2, W3): (0,0), (0,2), (0,1), (2,2), (2,1), (1,1)
- Final x = 3 (W4): the same six pairs plus (1,2)

BEGIN
0 0 2
0 2 2
0 1 2
2 2 2
2 1 2
1 1 2
0 0 3
0 2 3
0 1 3
2 2 3
2 1 3
1 1 3
1 2 3
END