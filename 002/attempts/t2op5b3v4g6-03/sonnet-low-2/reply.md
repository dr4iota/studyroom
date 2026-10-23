Every operation takes effect at one instant, and the problem has no sync points, so the executions are exactly the interleavings that keep each thread's order and agree with the known results.

**Constraints**
- B5 returns 4, so A3 comes before B5.
- B1 returns 0, so A5 comes after B1. This always holds, because A5 is the last operation of A and B1 is the first of B.
- Over time, x takes the values 0, then 2 (B2), 1 (B3), 2 (B4). A5 inserts a 3 at some point after A4.
- A1 comes before A3, and A3 comes before B5, so A1 can fall anywhere up to B4. A1 can therefore return 0, 2, 1 or 2.
- A4 is after A1, so it reads the same position in that sequence or a later one. A5 is after A4, so A4 never reads 3.

**Final value 3 (A5 after B4)**
- A4 may read any position from A1's position through B4's.
- This gives (A1, A4) = (0,0), (0,1), (0,2), (1,1), (1,2), (2,1), (2,2).

**Final value 2 (B4 after A5)**
- A4 comes before A5, which is before B4, so A4 cannot read B4's write.
- A4 is therefore at or before the "1" position, which rules out A1=1 with A4=2.
- This gives (0,0), (0,1), (0,2), (1,1), (2,1), (2,2).

BEGIN
0 0 2
0 0 3
0 1 2
0 1 3
0 2 2
0 2 3
1 1 2
1 1 3
1 2 3
2 1 2
2 1 3
2 2 2
2 2 3
END