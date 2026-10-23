I modeled each thread as a chain of operations whose effects happen in program order, and let any interleaving of those effects occur. Only the operations that affect the asked values matter: A1, A2, A4, A5, B1, B2, C1, C2, C3. A1's read is 1 exactly when C1 takes effect before A1, so the value written by A2 and A5 is 0 or 1.

- **Final y** is the value of A5 if B1 takes effect before A5, and 2 if B1 takes effect after A5. A4 can never be last because A5 follows it.
- **Q1 (B2's read of z)** is the later of A2's write and C3's write (3) if both precede B2. It is 0 if neither precedes B2.
- **Q2 (C2's read of y)** is the latest of B1 (2), A4 (3), and A5 (the value of A1) that precedes C2, or 0 if none does.

Enumerating the orderings in each case gives 29 distinct combinations (Q1 ∈ {0,1,3}, Q2 ∈ {0,1,2,3}, Q3 ∈ {0,1,2}). A few combinations are impossible, such as (0,1,2) and (1,1,0), because of the ordering constraints.

BEGIN
0 0 0
0 0 1
0 0 2
0 1 1
0 2 0
0 2 1
0 2 2
0 3 0
0 3 1
0 3 2
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