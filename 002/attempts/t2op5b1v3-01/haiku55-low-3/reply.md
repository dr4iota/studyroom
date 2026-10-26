With no sync points, the only constraints are that each thread's operations take effect in program order, and operations from different threads can interleave freely. So every merge of the two sequences (A1–A4 with B1–B5) is achievable, and the outcomes are determined by the possible merges.

**Q1 (A1):** A1 returns 1 if B1 took effect before it (B4 can only be before A1 if B1 is too), and 0 otherwise. So A1 ∈ {0, 1}.

**Q2 (B3):** B1 always precedes B3, so B3 is 1, 2, or 3. It is 3 if A4 precedes B3, 2 if only A3 does, and 1 otherwise.

**Q3 (B5):** B4 always precedes B5 and writes 1. B5 is 3 if A4 falls between B4 and B5, 2 if A3 falls between B4 and B5 with A4 after B5, and 1 otherwise.

**Combining the cases:**
- A1 = 0 (A1 before B1): (B3, B5) ∈ {(1,1), (1,2), (1,3), (2,1), (2,3), (3,1)}.
- A1 = 1 (B1 before A1): the same (B3, B5) pairs are reachable.

Impossible pairs: (2,2), since A3 before B3 forces A3 before B4, so B5 cannot see A3; and (3,2), (3,3), since A4 before B3 forces B5 = 1.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END