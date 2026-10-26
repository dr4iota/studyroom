Every interleaving of the two threads is allowed, because there are no sync points.

**Reads by B1 and B2**

Before B3 runs, only thread A writes to x, and it does so in order: x goes 0 → 3 → 1. B1 reads before B2, so B2 can never see an earlier value than B1 did. That gives six possible pairs (B1, B2): (0,0), (0,3), (0,1), (3,3), (3,1), (1,1).

**Final value of y**

A3 runs after A2, so it reads one of these:
- the 1 written by A2, if no write by B lands between A2 and A3;
- B1's value, if B3 takes effect between A2 and A3 and B4 takes effect after A3;
- B2's value, if B4 takes effect between A2 and A3.

None of these orderings conflicts with how B1 and B2 got their values. Both reads can happen before B3 and B4, which are then free to run late enough. So y can be 1, B1's value, or B2's value for every pair.

BEGIN
0 0 1
0 0 0
0 3 1
0 3 0
0 3 3
0 1 1
0 1 0
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END