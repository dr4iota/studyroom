Every operation in the problem is atomic and there are no sync points, so any interleaving that keeps each thread's own order is possible. I worked through which interleavings give each outcome.

**Q1, the value A3 reads from y.** The writes to y are B1 (2), B3 (the value B2 read) and C4 (1). B2 runs after B1, so it reads 1 or 2, and B3 therefore writes 1 or 2. A3 can therefore read 0, 1 or 2.

**Final x = 3.** A5 can run after everything else, so the last write to x is 3. A3 can read 0, 1 or 2, and the final y can be 1 or 2 in each case. That gives all six combinations of A3 ∈ {0,1,2} and y ∈ {1,2}.

**Final x set by C2 (C2 is the last write to x).** C2 must come after A5 and B5, and C4 comes after C2, so C4 is the last write to y and y = 1. Then A3 cannot read 1, because C4 would have to precede A3, and A3 precedes A5, which precedes C2 and C4. Also B2 must read 2, because C4 has not yet run. So A3 ∈ {0,2}, and C1 can read 0, 1, 2 or 3, which gives x ∈ {0,1,2,3}. The new combinations are:
- x = 0: (0,0,1), (2,0,1)
- x = 1: (0,1,1), (2,1,1)
- x = 2: (0,2,1), (2,2,1)

**Final x set by B5 (B5 is the last write to x).** Here x equals the value B2 read.
- If B2 read 1, C4 ran before B2, so y = 1. A3 can be 0, 1 or 2, which adds (1,1,1).
- If B2 read 2, B3 writes 2 and C4 can land before or after it.
  - y = 2 works for A3 = 0, 1 or 2.
  - y = 1 requires C4 after B3, which rules out A3 = 1.

  This adds (0,2,2), (2,2,2) and (1,2,2).

**Excluded combinations.** x = 1 or x = 0 with y = 2 is impossible, because those cases force C4 or B5 to make y = 1. (1,2,1) is impossible for the reason above.

BEGIN
0 3 1
0 3 2
1 3 1
1 3 2
2 3 1
2 3 2
0 0 1
2 0 1
0 1 1
1 1 1
2 1 1
0 2 1
0 2 2
1 2 2
2 2 1
2 2 2
END