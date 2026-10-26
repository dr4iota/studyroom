Block y is written only by B4, and B4 writes the value that B3 read from z.

**Value written to y.** B3 runs after B2, so it reads 4 (B2's write) or 2 (C1's write, if C1 lands between B2 and B3). It never reads 0. Call this value v, with v in {2, 4}. Because B4 is the only write to y, any read of y returns either 0 or the same v.

**Q1 and Q2.** A3 returns 0 or v, and C3 returns 0 or v. A3 and C3 are not constrained against each other, and v is a single value shared by both reads. So A3 and C3 cannot be 2 and 4 in either order.

**Q3 (final x).** The writes to x are B1 (3), C2 (2), A4 (the value A2 read) and C4 (the value C3 read). C2 always precedes C4, and C4 writes C3's value, which is 0 or v. So C2's value 2 can be final only when it equals v. The candidates for the final value are:
- 3, when B1 is last.
- C3's value, when C4 is last.
- A2's value (0 or v), when A4 is last.

Checking each (A3, C3) pair:
- **A3=0, C3=0:** A2 must be 0, so A4 writes 0 and C4 writes 0. The final x is 0 or 3.
- **A3=v or C3=v:** both A2 = 0 and A2 = v are possible, as is C3 = 0 or v. In every case the final x can be 0, 3 or v, and all are achievable.
  - A3=0, C3=v: A2 = 0 and A4 comes last, giving 0.
  - A3=v, C3=0: A2 = v and A4 comes last, giving v.

**Combinations.** With v = 2 or v = 4:
- (0, 0): x in {0, 3}
- (0, v): x in {0, 3, v}
- (v, 0): x in {0, 3, v}
- (v, v): x in {0, 3, v}

BEGIN
0 0 0
0 0 3
0 2 0
0 2 3
0 2 2
0 4 0
0 4 3
0 4 4
2 0 0
2 0 3
2 0 2
4 0 0
4 0 3
4 0 4
2 2 0
2 2 3
2 2 2
4 4 0
4 4 3
4 4 4
END