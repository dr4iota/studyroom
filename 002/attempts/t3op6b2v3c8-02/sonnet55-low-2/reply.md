Every operation takes effect at a single instant, so the possible executions are the interleavings of the three threads that keep each thread's program order. No sync points or known results restrict them. For each (C2, C4) pair, I then checked which values A4 can read.

**Possible C2 values**
- C2 always follows C1, which writes 1 to y, so C2 normally reads 1 or 2.
- C2 can read 1 if C1 is the last write to y before it.
- C2 can read 2 if B1 writes 2 after C1 and before C2.
- C2 can also read 0. A1 reads 0 first, then C1 writes 1, then A3 writes A1's value 0 to y, then C2 reads 0.

**Possible C4 values given C2**
- C3 writes C2's value to x before C4. C6 (which writes 2) comes after C4, so it cannot supply C4's value. B2 can write 1 to x at any time.
- C2 = 0: C4 = 0 if B2 has not yet written, or if B2 wrote before C3 and C3's 0 overwrote it. C4 = 1 if B2 writes after C3 and before C4. C4 = 2 is impossible, since only C3 or C6 could supply a 2, and C3 writes 0 here.
- C2 = 1: C3 writes 1, so C4 = 1 (from C3 or B2). C4 = 0 and C4 = 2 are impossible.
- C2 = 2: C3 writes 2, so C4 = 2 if B2 does not intervene, or C4 = 1 if B2 writes after C3 and before C4. C4 = 0 is impossible.

**Possible A4 values**
In every case above A4 can be 0, 1 or 2.
- A4 = 0: it reads before B2 and before C3.
- A4 = 1: it reads after B2.
- A4 = 2: it reads after C3 has written 2 or after C6. The A4 = 2 cases with C4 = 0 or 1 are possible because C6 comes after C4 and A4 can be placed after C6.

This gives all 15 combinations of A4 ∈ {0,1,2} with (C2, C4) ∈ {(0,0), (0,1), (1,1), (2,1), (2,2)}.

BEGIN
0 0 0
1 0 0
2 0 0
0 0 1
1 0 1
2 0 1
0 1 1
1 1 1
2 1 1
0 2 1
1 2 1
2 2 1
0 2 2
1 2 2
2 2 2
END