Every operation takes effect at a single instant and there are no sync points, so the executions are exactly the interleavings that keep each thread's own order. Let v be the value A1 reads. A then writes v to z twice and writes v to y last. B2 reads 0 or 1, because only C2 writes x. B3 then writes that value to y. The final y is whichever of A4 (writing v) and B3 (writing B2's value) takes effect later.

**Which (B5, C4) pairs can occur**
- Both B5 and C4 can be 0 only if A writes a 0 after B1 and C1. That needs A1 to read 0 before B1 and C1, and then A2 or A3 to write 0 after both.
- (B5, C4) = (2, 0) is impossible. C4 = 0 means v = 0, so the only write of 2 is C1, which takes effect before C4. B5 would then have to read 2 after a later 0 write, which nothing supplies.
- The other eight pairs are possible. Q1 is B5 and Q2 is C4.

**Which final y values occur**
- y = 2 needs v = 2 with A4 after B3, so A1 reads 2 after C1. A then never writes 0, so C4 ≠ 0. B5 ≠ 0 because B1 precedes B5 and A writes no 0. This leaves B5 and C4 each in {1, 2}, and all four of those pairs can be built.
- y = 1 comes from B2 = 1 with B3 last, which puts C1, C2 and B1 before B2. All eight possible pairs work.
- y = 0 comes from v = 0 with A4 last, or from B2 = 0 with B3 last. All eight possible pairs work. For example, (2, 1) uses B2 = 0: C1, A1 (reads 2), B1, B2, C2, C4 (reads 1), A2, A3, A4, B3 (writes 0), B4, B5 (reads 2).

That gives 8 + 8 + 4 = 20 combinations.

BEGIN
0 0 0
0 1 0
0 2 0
1 0 0
1 1 0
1 2 0
2 1 0
2 2 0
0 0 1
0 1 1
0 2 1
1 0 1
1 1 1
1 2 1
2 1 1
2 2 1
1 1 2
1 2 2
2 1 2
2 2 2
END