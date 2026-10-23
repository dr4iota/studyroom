Each operation takes effect at a single instant and each thread keeps its own order, so the possible outcomes are exactly those of the interleavings of the three threads.

**What is fixed**
- B5 comes after B1, which writes 1 to z. So B5 reads either 1 or 2, never 0, because z is only ever overwritten with 0 by A2 or A3, and that needs A1 to have read 0.
- That also holds when A writes 0: B5 can read 0 only if a later write of 0 is the last write before B5. Allowing this, B5 = 0 would need A2 or A3 to write 0 after B1 and after C1. I did not rule this case out above, so I check it below.
- C4 comes after C1, which writes 2 to z. The same reasoning applies to C4.

**Checking whether 0 is possible for B5 or C4**
A writes 0 to z only if A1 read 0. A1 can read 0 before B1 and C1, and A2 and A3 can then run after B1 and C1. For example, order A1 (reads 0), B1, C1, A2 (writes 0), then C4 and B5 both read 0. So 0 is possible for B5 and for C4, and the values for Q1 and Q2 are in {0, 1, 2}.

Let a be the value A1 reads from z, and b the value B2 reads from x.

**Final y**
y is the last write among B3 (writes b, where b is 0 or 1) and A4 (writes a, where a is 0, 1 or 2). Every value 0, 1 and 2 is reachable as the final y:
- y = 2: a = 2 (A1 runs after C1) and A4 runs after B3.
- y = 1: b = 1 (B2 runs after C2) with B3 after A4, or a = 1 with A4 last.
- y = 0: b = 0 with B3 last, or a = 0 with A4 last.

**Combinations of B5 and C4**
With a = 2 and extra writes of 2 from A2 and A3, all nine pairs (B5, C4) in {0, 1, 2}² can be arranged. Examples:
- (B5 = 2, C4 = 1): C1, A1 (reads 2), B1, C4 (reads 1), A2 (writes 2), B5 (reads 2).
- (B5 = 0, C4 = 1): A1 reads 0 and A2 and A3 write 0 after C4 and before B5, with B1 and C1 earlier.
- The remaining pairs follow by similar orderings of B1, C1, A2 and A3.

Each pair can be combined with each final y by placing B2, B3 and A4 appropriately, since B2 and B3 only constrain y and x.

All 27 combinations are therefore possible.

BEGIN
0 0 0
0 0 1
0 0 2
0 1 0
0 1 1
0 1 2
0 2 0
0 2 1
0 2 2
1 0 0
1 0 1
1 0 2
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 0 1
2 0 2
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END