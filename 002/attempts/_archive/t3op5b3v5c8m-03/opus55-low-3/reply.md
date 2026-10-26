Every combination of B1 ∈ {0, 2}, final x ∈ {0, 2} and final z ∈ {0, 2, 3} is possible, which gives 12 outcomes. There are no sync points in this problem, so any interleaving of the three threads that keeps each thread's own order is allowed.

**Which values can appear?**
- **x** is written by A1 (the value 2) and by B4 (whatever B2 read from y).
- **y** is written by B3 (whatever B1 read from x) and by C3 and C4 (whatever C2 read from x).
- **z** is written by C1 (the value 3) and by A4 (whatever A3 read from y).

Every read of x or y starts from 0 or from 2, and each copy passes one of those along. So every value read from x or y is 0 or 2. This means:
- B1 is 0 or 2.
- The final x is 0 or 2.
- The final z is 3, or 0 or 2 if A4's write comes after C1.

**Each combination can be reached:**
- **B1 = 0:** B1 runs before A1.
  - **Final x = 0:** B2 reads y before any write to y, so it gets 0. B4 then writes 0 to x after A1.
  - **Final x = 2:** A1 is the last write to x.
- **B1 = 2:** B1 runs after A1. The same two ways of ending x apply.
  - **Final x = 0:** B2 still reads 0 if it runs before B3 and C3, and B4 writes 0 after A1.
- **Final z = 3:** A4 runs before C1.
- **Final z = 0:** A3 reads y before any write to y. A4 then writes 0 after C1.
- **Final z = 2:** A3 reads a 2 written to y, either by B3 (when B1 = 2) or by C3 (when C2 read 2 after A1). A4 then writes 2 after C1.

**Checking the hardest case (B1 = 0, x = 0, z = 2):**
1. B1 reads 0.
2. B2 reads 0.
3. A1 writes 2 to x.
4. C1 writes 3 to z.
5. C2 reads 2.
6. C3 writes 2 to y.
7. A2 and A3 read 2.
8. A4 writes 2 to z.
9. B3 writes 0 to y, and B4 writes 0 to x, which ends x at 0.

The other choices fit together in the same way, so all 12 combinations are valid.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END