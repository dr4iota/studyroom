Each operation takes effect at a single instant and there are no sync points, so every interleaving of the three threads' operations is allowed. I worked out which values are reachable for each question by case analysis on B2, not by running a program.

**Setup.** A1 reads x, which is only ever 0 or 1 (C1/C4 write 1, A3 writes A1's value), so call A1's result a ∈ {0,1}. Writes to y are B1=2, A4=3, A5=a, and A4 always precedes A5. Writes to z are A2=a and C3=3.

**Q1 (B2), by case:**

- **B2 = 0.** B2 precedes A2 and C3. Since B1 precedes B2, which precedes A2 and A5, B1 cannot be the last write to y. The final y is therefore a, so 0 or 1. C2 can read 0, 2 or 3 with either final value. C2 can read 1 only when a=1, which forces final y = 1. The reachable (C2, y) pairs are (0,0), (0,1), (1,1), (2,0), (2,1), (3,0), (3,1).
- **B2 = 1.** This requires a=1 and A2 before B2, so A5 writes 1. The final y is 1, or 2 if B1 comes after A5. C2 can be 0, 1, 2 or 3 with either final value, giving 8 combinations.
- **B2 = 3.** This requires C2 < C3 < B2.
  - Final y = 2: B1 comes after A5, so A2 must precede C3. C2 can be 0, 1, 2 or 3.
  - Final y = 0: this needs a=0, so C2 can be 0, 2 or 3 but not 1.
  - Final y = 1: this needs a=1, and C2 can be 0, 1, 2 or 3.

BEGIN
0 0 0
0 0 1
0 1 1
0 2 0
0 2 1
0 3 0
0 3 1
1 0 1
1 0 2
1 1 1
1 1 2
1 2 1
1 2 2
1 3 1
1 3 2
3 0 0
3 0 1
3 0 2
3 1 1
3 1 2
3 2 0
3 2 1
3 2 2
3 3 0
3 3 1
3 3 2
END