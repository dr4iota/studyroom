Neither thread has sync points, so every interleaving that keeps each thread's own order is allowed.

**Possible (B1, B2) pairs.** Before B3 runs, x only takes the values 0, 3, 1, in that order, because only A's writes have happened by then. B1 and B2 read in that order, so B2's value cannot come earlier in that sequence than B1's. The possible pairs are (0,0), (0,3), (0,1), (3,3), (3,1) and (1,1).

**Final y.** A4 always writes the value A3 read, and it is the only write to y. So the final y is A3's value. A3 runs after A2, when x is 1. A3 can then see 1, or the value written by B3 (b1) or B4 (b2) if that write lands between A2 and A3.

- (0,0): B3 and B4 both write 0, so A3 reads 1 or 0. y is 0 or 1.
- (0,3): B3 writes 0 and B4 writes 3. A3 can read 1, 0 or 3. y is 0, 1 or 3.
- (0,1): B3 writes 0 and B4 writes 1. A3 can read 1 or 0. y is 0 or 1.
- (3,3): B3 and B4 both write 3, so A3 reads 1 or 3. y is 1 or 3.
- (3,1): B3 writes 3 and B4 writes 1. A3 can read 1 or 3. y is 1 or 3.
- (1,1): all writes are 1, so y is 1.

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
0 3 3
0 1 0
0 1 1
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END