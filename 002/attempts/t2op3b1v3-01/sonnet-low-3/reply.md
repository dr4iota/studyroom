Each operation takes effect at a single instant, so the operations of one thread take effect in program order. Every possible execution is therefore an interleaving of A1 A2 A3 with B1 B2 B3. The writes to x are A1 (1), B2 (3) and B3 (2), with B2 before B3. Reads A2 and A3 see the state at their instants, and A3 sees a state no earlier than A2's. B1 takes effect before B2 and B3.

The position of A1 among the writes gives three cases.

**Case 1: write order 1, 3, 2 (A1 first).** The states are 1, 3, 2, and both A reads come after A1, so they see states in that order.
- A2, A3 can be (1,1), (1,3), (1,2), (3,3), (3,2), (2,2).
- B1 comes before B2, so it reads 0 (before A1) or 1 (after A1). Either is compatible with every pair above.

**Case 2: write order 3, 1, 2 (A1 between B2 and B3).** B1 comes before B2, so B1 reads 0. Both A reads come after A1, so they see state 1 or 2.
- A2, A3 can be (1,1), (1,2), (2,2).

**Case 3: write order 3, 2, 1 (A1 last).** B1 reads 0. The A reads can see the states 0, 3, 2, 1, in that order.
- A2, A3 can be (0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

Combining the cases:
- B1 = 0 gives 12 distinct pairs for A2, A3.
- B1 = 1 gives 6 pairs, all from Case 1.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
0 0 0
0 3 0
0 2 0
0 1 0
3 1 0
2 1 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END