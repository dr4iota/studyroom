Working through the interleavings (y-writes are A1=3, B3=b2, C4=c1; x-writes are B1=1, C3=c1), the reachable outcomes for (A3, B4, final x) are:

- Values of y are always 0 or 3, so A3 and B4 are in {0, 3}.
- Final x is 1 if B1 is last, or c1 if C3 is last.
- The pair (B2, C1) can be (0,0), (3,0), (0,3), or (3,3). When C1 = 3 and B2 = 0, B1 must precede B2, which precedes C3, so final x = 1 is impossible.
- When B2 = C1 = 3, all y-writes are 3, so A3 = B4 = 3, and final x can be 1 or 3.

BEGIN
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 0 0
3 0 1
3 0 3
3 3 0
3 3 1
3 3 3
END