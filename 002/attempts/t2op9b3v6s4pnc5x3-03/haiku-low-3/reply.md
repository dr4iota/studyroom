**Constraints from the sync points**

- All of B (B1–B8) takes effect before Q, and A2–A8 take effect after Q. So every B operation precedes A2 through A8.
- A1 has no sync constraint, so it can take effect anywhere before A2. Say A1 lands after the first k of B's operations, with k from 0 to 8.
- The remaining sync constraints (B1 < P < A8, B4 < R < A6, B7 < S < A7) can always be satisfied, so they rule out nothing.

**Values**

- **Q1 (A7 reads z):** A3 writes 2 to z after B4 writes 6, and nothing else writes z later. So Q1 = 2 always.
- **Q2 (A8 reads y):** A4 writes a2 to y after all of B, and a2 is the value A2 read. A2 reads x, whose last B write is B5, which writes b3. So Q2 = b3, the value B3 read from y.
- **b3:** B3 sees A1's write (y = 1) only if A1 lands before B3, i.e. k ≤ 2. Otherwise b3 = 0. So Q2 = 1 for k ≤ 2 and 0 for k ≥ 3.
- **Q3 (B8 reads y):** B8 follows B7, which writes 6 to y. The only way B8 sees something else is if A1 lands between B7 and B8 (k = 7), giving 1. So Q3 = 1 for k = 7 and 6 otherwise.

**Cases**

- k = 0, 1, 2: 2 1 6
- k = 3, 4, 5, 6, 8: 2 0 6
- k = 7: 2 0 1

So three distinct outcomes are possible.

BEGIN
2 1 6
2 0 6
2 0 1
END