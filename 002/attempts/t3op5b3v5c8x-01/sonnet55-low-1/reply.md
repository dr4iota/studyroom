Every operation takes effect at one instant and each thread keeps its own order, so the possible outcomes are the interleavings of the three threads. There are no sync points. I reasoned through the cases by hand rather than running a program.

**Final value of y.** y is written only by A4 (value a, what A1 read from z) and B3 (value b, what B2 read from x). Whichever of the two takes effect last determines y.
- a can be 0, 1 or 2, depending on when A1 reads z.
- b can be 0 or 1. It is 1 only if C2 happens before B2.
- Both writes always happen, so y is never left at its starting value except through a write of 0.

**Case y = 2.** This needs a = 2, with A4 after B3. Then every write to z is nonzero (B1 writes 1, C1 writes 2, A2 and A3 write 2). So B5 and C4 can only be 1 or 2. All four pairs are reachable:
- (1,1) and (2,2) are straightforward.
- (B5,C4) = (1,2): C1, C4 reads 2, A1 reads 2, B1, B5 reads 1. A2 and A3 come later.
- (B5,C4) = (2,1): C1, A1 reads 2, B1, C4 reads 1, A2 writes 2, B5 reads 2.

**Case y = 0 or 1.** All nine (B5, C4) pairs are reachable.
- With a = 0, A2 and A3 can write 0 after B1 and C1. That is how B5 or C4 can read 0.
- Every pair except (B5,C4) = (2,1) is reachable with a = 0.
- (2,1) needs a = 1: B1, A1 reads 1, C1, B5 reads 2, A2 writes 1, C4 reads 1.
- y = 0 is reachable when A4 is last with a = 0, or when B3 is last with B2 before C2.
- y = 1 is reachable when B3 is last with C2 before B2, or when A4 is last with a = 1.

This gives 9 × 2 + 4 = 22 combinations.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 0 1
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END