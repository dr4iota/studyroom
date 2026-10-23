Every operation is an ordinary read or write with no sync points, so any interleaving that keeps each thread's order is allowed.

**Possible values.** The only values ever written to y are 3 (A1), 0 or 3 (B3, from B2), and 0 or 3 (C4, from C1). So y is always 0 or 3. Hence A3 ∈ {0,3}, B4 ∈ {0,3}, and C1 returns 0 or 3.

The writes to x are B1 (writes 1) and C3 (writes C1's value). So the final x is:
- 1 if C3 happens before B1,
- C1's value (0 or 3) if C3 happens after B1.

**x = 1.** C1, C2 and C3 all run before B1. All four (A3,B4) pairs work:
- (3,3): A1 runs early, and the later writes are 3.
- (0,0): C1 reads 0, then B1, B2, B3 and B4 run, then A1, then C4 writes 0, then A2 and A3.
- (0,3): B2 reads 0 and B3 writes 0, then A1, then B4 reads 3, then C4 writes 0, then A3 reads 0.
- (3,0): B2 reads 0, B3 writes 0, B4 reads 0, then A1, then A2 and A3 read 3. C4 writes 0 early, before A1.

**x = 0.** C1 reads 0 first, and C3 writes 0 after B1. The same four interleavings work, with C4 writing 0 in the right place, so all four pairs are possible.

**x = 3.** C1 must read 3, so A1 comes before C1 (or B3 wrote 3, which also needs A1 first).
- (3,3): possible.
- (0,0): B1, B2 reads 0, A1, C1 reads 3, C2, C3, B3 writes 0, B4 reads 0, A2, A3 read 0.
- (3,0): B1, B2, B3 writes 0, B4 reads 0, then A1, C1 reads 3, C2, C3, A2, A3 read 3.
- (0,3): impossible. A3 = 0 needs a 0 write after A1, and the only possible 0 write is B3. But B4 = 3 needs A1 to come after B3 and before B4, which puts B3 before A1. C4 writes 3 here, so no 0 write can follow A1.

BEGIN
3 3 1
3 0 1
0 3 1
0 0 1
3 3 0
3 0 0
0 3 0
0 0 0
3 3 3
3 0 3
0 0 3
END