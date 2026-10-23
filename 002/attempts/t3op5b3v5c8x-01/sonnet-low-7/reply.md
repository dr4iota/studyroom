The problem has no sync points, so every operation takes effect at one instant and the executions are exactly the interleavings of the three threads. I enumerated them by hand, working out which (B5, C4, final y) triples are reachable.

**Facts used**
- Let a be the value A1 reads from z. A2 and A3 write a to z, and A4 writes a to y.
- Let r be the value B2 reads from x, which is 0 or 1. B3 writes r to y.
- The final y is whichever of A4 and B3 takes effect last, so it is a or r.
- B1 and C1 both take effect before B5 and C4 respectively. A value of 0 can still be read from z, but only if A (with a = 0) overwrites z with 0 after B1 or C1.

**B5 = 0**
- This needs a = 0, because only A can write 0 after B1.
- C4 = 1 is impossible. The only write of 1 other than A's is B1, and B1 precedes B5, so no 1 can appear after B5 has read 0.
- C4 = 0 is possible with y = 0 or y = 1. For y = 1, A4 runs before B3 and B3 reads x = 1.
- C4 = 2 is possible, but only with y = 0. For y = 1, B3 would have to read x = 1, which forces C1 before B5. After that, z could not return to 2 for C4.

**C4 = 0** (this needs a = 0, so y is 0 or 1)
- B5 = 1 allows y = 0 and y = 1.
- B5 = 2 allows only y = 0. Here A3 must fall between B5 and C4, so A4 comes after B3 and writes 0 last.

**a = 2, so y = 2 is possible**
- This needs A4 after B3, and z is never 0.
- It is possible for (1,1), (1,2), (2,1) and (2,2) as (B5, C4).

**Remaining cases**
- B5 = 1 or 2 with C4 = 1 or 2 can reach y = 0, 1 and 2.
- (2,1,0) works with a = 2 and r = 0, so that A4 precedes B3.

**Reachable triples**
- (0,0,0), (0,0,1), (0,2,0)
- (1,0,0), (1,0,1)
- (2,0,0)
- (1,1,0), (1,1,1), (1,1,2)
- (1,2,0), (1,2,1), (1,2,2)
- (2,1,0), (2,1,1), (2,1,2)
- (2,2,0), (2,2,1), (2,2,2)

BEGIN
0 0 0
0 0 1
0 2 0
1 0 0
1 0 1
2 0 0
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END