**Reasoning**

- **A4 (read x):** x is written by B2 (1), C3 (copy of C2 ∈ {0,1,2}), C6 (2). A4 can be placed before any write (0), right after B2 (1), or at the very end after C6 (2). So A4 ∈ {0, 1, 2}, independent of the other choices.
- **C2 (read y, after C1 writes 1):** can return 1 (own write), 2 (B1 after C1), or 0 (A3/A6/B5 copying an initial 0 into y after C1). So C2 ∈ {0, 1, 2}.
- **C4 (read x, after C3 writes C2's value):** returns C2's value, or 1 if B2 lands between C3 and C4. C6 comes later, so 2 is only possible when C2 = 2. So C4 ∈ {C2, 1}.

All combinations are jointly realizable.

BEGIN
0 0 0
0 0 1
0 1 1
0 2 2
0 2 1
1 0 0
1 0 1
1 1 1
1 2 2
1 2 1
2 0 0
2 0 1
2 1 1
2 2 2
2 2 1
END