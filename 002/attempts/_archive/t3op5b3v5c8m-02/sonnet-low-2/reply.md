Every interleaving that respects each thread's program order is allowed, since no sync points are given.

**B3 (read y).** B2 writes 1 to y before B3, so B3 returns 1 or 4. It returns 4 only if A1 falls between B2 and B3, and then A2 must come after B3. B3 cannot return 0.

**A3 (read x).** The writes to x are C2 (2), C3 (1), and B4 (the value B3 read, 1 or 4). A3 can return 0, 1, 2 or 4.
- A3 = 4 needs B4 to write 4, so B3 = 4 and A3 comes after B4.
- Every other pairing of A3 ∈ {0, 1, 2} with B3 ∈ {1, 4} can be arranged. For B3 = 4 the order is B2 < A1 < B3 < A2 < A3, and A3 can sit before B4, C2 and C3 (reading 0) or after any one of them.
- The feasible (A3, B3) pairs are (0,1), (0,4), (1,1), (1,4), (2,1), (2,4), (4,4).

**Final z.** The writes to z are B1 (4), A4 (A3's value), C4 (C1's value) and C5 (4), with C5 after C4 in thread C.
- C4 can never be last, because C5 follows it.
- If C5 or B1 is last, z = 4. This is possible for every feasible pair, since C5 can be placed last in the whole execution.
- If A4 is last, z equals A3's value. Nothing prevents A4 from running after everything else, so this is possible for every pair too.
- So the final z is either 4 or A3's value.

BEGIN
0 1 0
0 1 4
0 4 0
0 4 4
1 1 1
1 1 4
1 4 1
1 4 4
2 1 2
2 1 4
2 4 2
2 4 4
4 4 4
END