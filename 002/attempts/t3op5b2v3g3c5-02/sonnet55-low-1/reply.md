Each operation takes effect at a single instant, and the problem has no sync points, so any interleaving that keeps each thread's order is allowed. The two known results are A2 = 2 and B5 = 2.

**Possible values of x.** The only writes to x are C1 (2), A3 (the value A1 read) and B4 (the value B2 read). Starting from 0, x can only ever hold 0 or 2. So A1 and B2 return 0 or 2, and both are possible.
- A1 = 0 works when A1 runs first and C1 later supplies the 2 that B5 reads.
- A1 = 2 works when C1 comes before A1.

**Q2, the value B3 returns.** B1 writes 1 to y before B3, so B3 cannot read 0. The other values are all reachable.
- B3 = 1: B1 then B3 run first, and C2 comes later.
- B3 = 2: C2 comes after B1 and before B3.
- B3 = 3: A4 comes before B3, with A2 reading 2 earlier.

**Constraint from A2.** A2 reads 2, so C2 (or C5 writing 2) must come before A2, and A4 must come after A2.

**Q3, the final value of y.**
- Final 3: A4 is the last write to y. B3 can be 1, 2 or 3.
- Final 2: C5 writes 2 last, having read 2 in C4. A4 and B1 take effect between C4 and C5, or earlier. B3 can be 1, 2 or 3.
- Final 1: B1 is the last write to y. B3 comes after B1 and nothing writes after B1, so B3 must be 1.

Each of these combinations works with either A1 = 0 or A1 = 2. That gives 7 (B3, final y) pairs times 2 values of A1, which is 14 combinations.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 2
0 2 3
0 3 2
0 3 3
2 1 1
2 1 2
2 1 3
2 2 2
2 2 3
2 3 2
2 3 3
END