Only x is written. Thread B writes 3, 2, 1 in that order, and A4 writes 2 once after A3. Reads of y don't matter (A1 reads 0 either way).

**Reads A2 and A3.** A4 comes after both reads, so before A3 finishes the only writes to x are B's. During that time x goes through 0, 3, 2, 1 in order. A2 and A3 are consecutive reads, so each returns one of these states, and A3's state is the same as or later than A2's. That gives 10 pairs (A2, A3):
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

B1 reads 0 only if it takes effect before B2, which is always possible and puts no extra limit on A.

**Final value of x.** The final value is set by whichever of A4 and B4 takes effect last.
- If A4 comes last, the final value is 2. This is possible for every pair.
- If B4 comes last, the final value is 1. This needs A4 to take effect before B4. That is impossible when A3 returned 1, because B4 has already taken effect by then. For every other A3 value it is possible.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
END