**Approach:** There are no sync points, so any interleaving that keeps each thread's order is allowed. Everything depends on the value A1 reads from x, called a below.

**What A1 can read**
- a = 0 if A1 runs before C1.
- a = 1 if A1 runs after C1. (C4 also writes 1.)

**Possible values of each asked quantity**
- **B2 (reads z):** 0, a (written by A2) or 3 (written by C3).
- **C2 (reads y):** 0, 2 (written by B1), 3 (written by A4) or a (written by A5).
- **Final y:** A5 always runs after A4. So the final y is a if A5 is the last write to y, or 2 if B1 comes after A5.

**Case a = 0 (A1 runs before C1)**
- Every combination of B2 ∈ {0, 3}, C2 ∈ {0, 2, 3} and final y ∈ {0, 2} can be scheduled. That gives 12 combinations.
- Example for B2=3, C2=0, y=0: A1, C1, C2, C3, B1, B2, A2, A3, A4, A5. Here C2 reads 0 and B2 reads the 3 written by C3. A2 then writes 0 to z, and A5 writes 0 to y last.

**Case a = 1 (A1 runs after C1)**
- **Final y = 1:** B1 runs before A5. B2 can be 0, 1 or 3, with any C2 ∈ {0, 1, 2, 3}.
  - Example for B2=0: B1, B2, C1, A1, A2, A3, A4, A5, C2. B2 runs before anything writes z.
- **Final y = 2:** B1 runs after A5. B2 comes after B1, so it also comes after A2. B2 therefore reads 1 or 3, never 0. C2 can be any of {0, 1, 2, 3}.
- This gives 4 × 3 + 4 × 2 = 20 combinations.

**Combining the cases**
- Three combinations appear in both cases: (B2=3, C2=0, y=2), (B2=3, C2=2, y=2) and (B2=3, C2=3, y=2).
- Total: 12 + 20 − 3 = 29 distinct combinations.

BEGIN
0 0 0
0 2 0
0 3 0
3 0 0
3 2 0
3 3 0
0 0 2
0 2 2
0 3 2
3 0 2
3 2 2
3 3 2
0 0 1
1 0 1
3 0 1
0 1 1
1 1 1
3 1 1
0 2 1
1 2 1
3 2 1
0 3 1
1 3 1
3 3 1
1 0 2
1 1 2
3 1 2
1 2 2
1 3 2
END