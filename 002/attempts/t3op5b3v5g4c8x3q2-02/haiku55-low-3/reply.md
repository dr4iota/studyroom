Q1 is A3's value (x at A3) and Q2 is B3's value (y at B3). Known results: C2 reads 1, C5 reads 2, and B5 reads 1.

**Key facts:**
- The y-writes are A1 (1) then A2 (2). C2 returning 1 forces A1 < C2 < A2, and C5 returning 2 forces A2 < C5. So B3 can read 0, 1, or 2.
- C1 (write 3 to x) precedes C2, which precedes A2, which precedes A3. So C1 always lands before A3, and the last x-write before A3 is either C1 (value 3) or B4 (value b3). A3 can never read 0 from an empty x, but it can read 0 if B4 writes 0 and lands between C1 and A3.
- So A3 ∈ {3, b3}.

**Feasibility by B3's value:**
- **b3 = 0** (B3 before A1): a = 3 is feasible (B4 after A3). a = 0 is feasible with order C1 < B4 < A3 after A1, A2. Both work.
- **b3 = 1** (B3 between A1 and A2): a = 3 (B4 after A3) and a = 1 (B4 between C1 and A3) are both feasible.
- **b3 = 2** (B3 after A2): a = 3 (A3 before B3) and a = 2 (B4 between C1 and A3) are both feasible.

Each case admits a full interleaving that respects all three thread orders and the known read results (B5 reads 1 from A4 or C4, and C2, C5 are satisfied). Values such as (1, 0), (0, 1), (2, 1), (0, 2) are impossible, since A3 can only be 3 or b3.

BEGIN
0 0
1 1
2 2
3 0
3 1
3 2
END