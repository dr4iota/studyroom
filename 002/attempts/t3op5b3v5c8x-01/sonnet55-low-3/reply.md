Each operation takes effect at a single instant and there are no sync points, so every interleaving of the three threads' program orders is allowed. A1 reads a value `a` from z, and A2, A3 and A4 then write `a`. B2 reads x as `r`, which is 1 only if C2 comes before B2.

The final value of y is whichever write came last: A4 writes `a`, and B3 writes `r`, which is 0 or 1.

**y = 2.** This needs A4 to come last with `a = 2`, so A1 read C1's value. Neither A nor anyone else ever writes 0 to z after that point, so B5 and C4 can only be 1 or 2. All four combinations are reachable:
- B5=1, C4=2: C1, A1, C4, B1, B5, with A2 and A3 after B5.
- B5=2, C4=1: B1 comes after A1, C4 reads 1, then A2 rewrites 2 before B5.
- B5=1, C4=1 and B5=2, C4=2 are also reachable by similar orders.

**y = 0.** Take `a = 0` with A4 last, so A1 comes before C1 and B1. A's later writes of 0 can overwrite z, so B5 and C4 can each be 0, 1 or 2. All nine combinations are reachable. For example, B5=2 with C4=0 uses B1, C1, B5, then A2 writing 0, then C4.

**y = 1.** Take B3 last with `r = 1`, or A4 last with `a = 1`.
- Eight combinations are reachable.
- B5=2 with C4=0 is impossible. B5 comes after B3, B3 comes after A4 (B3 is last), and A's zero-writes all come before A4. B5 reading 2 means C1 came after those zero-writes, so no 0 write can follow C1 for C4 to read. The alternative, A4 last with `a = 1`, never writes 0 at all.

BEGIN
0 0 0
0 1 0
0 2 0
1 0 0
1 1 0
1 2 0
2 0 0
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