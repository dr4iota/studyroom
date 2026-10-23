Only one final value of y is possible: 1.

**Writes to x.** The writers are A1 (1), A2 (4), B3 (5), B4 (2) and C4 (the value C1 read from z). For x to end at 4, the last write to x must be a 4. Either A2 writes it last, or C4 does.

**C4 cannot be the last write of 4.** For C4 to write 4, C1 must read z = 4. The only source of a 4 in z is A5 copying a 4 that A4 read from y, and y can only be 4 after B2 has run. That gives the chain B2 < A4 < A5 < C1. C2 comes after C1 and reads 3, which only B1 (or C3, which runs after C2) can supply. B1 therefore has to write after C1, but B1 precedes B2 in thread B, and B2 precedes C1 in the chain, so this is a contradiction. The last write to x must therefore be A2's 4.

**Consequence for y.** A2 must come after B3, because B3 writes 5 and would otherwise be last or overwrite A2's 4. B3 comes after B2 in thread B, so B2 < B3 < A2. A3 comes after A2 in thread A, so B2 < A3. B2 (writing 4) therefore happens before A3 (writing 1), and y finishes as 1.

**Feasibility.** The constraints are all consistent with one ordering: B1, C1, C2 (reads 3), B2, B3, B4, C4, A1, A2, A3, A4, A5, and so on. This ordering gives x = 4 and y = 1.

BEGIN
1
END