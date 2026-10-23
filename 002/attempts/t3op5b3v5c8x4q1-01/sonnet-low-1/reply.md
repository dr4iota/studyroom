C4 can only return 2.

**What the known results force**
- C3 returned 2 from z. The only writes to z are A4 and A5, which write the value A3 read. So A3 read 2 from y.
- B4 returned 2 from y. B3 writes 4 to y just before it in B's order. So some write of 2 to y must take effect after B3 and before B4's read.
- The writes to y are C2 (value 2), B3 (value 4), and A2 (the value A1 read, which is 0, 2 or 4).

**Why C4 cannot return 0**
- C2 takes effect before C4 in C's order, so y is no longer 0 when C4 runs.
- A2 could write 0 only if A1 read 0, which means A1 ran before C2. A2 comes before A3 in A's order, and A3 must read 2, so a 2 must be written after A2. That 2 can only come from C2, so C2 is after A2 and the 0 is overwritten.

**Why C4 cannot return 4**
- C4 runs after C3, which runs after A3. A2 and the write that gave A3 its 2 are therefore all done before C4.
- B3 must precede a write of 2, because B4 reads 2 after B3. B3 therefore cannot be the last write to y. Any 4 written by A2 is likewise overwritten by the later 2 that A3 reads.
- So the last write before C4 is always a 2.

**Why 2 is achievable**
One valid order is: C2, A1 (reads 2), B3, A2 (writes 2), A3 (reads 2), B4 (reads 2), A4, C3 (reads 2), C4 (reads 2).

BEGIN
2
END