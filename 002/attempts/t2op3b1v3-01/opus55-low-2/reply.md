**Approach.** Each operation takes effect at a single instant, so I enumerated the possible orders of those instants. Thread A's operations stay in order A1, A2, A3, and thread B's stay in order B1, B2, B3.

**Q3 (B1).** B1 is B's first operation, so the only write that can precede it is A1.
- If B1 takes effect before A1, it returns 0.
- If B1 takes effect after A1, it returns 1.

**Q1 and Q2 (A2, A3).** Both reads come after A1, so each returns the latest write among A1 (1), B2 (3) and B3 (2). A3 comes after A2, so A3 can never return an earlier write than A2. The possible pairs depend on where A1 falls among B's writes:
- **A1, B2, B3:** the write sequence is 1, 3, 2. The pairs are (1,1), (1,3), (1,2), (3,3), (3,2) and (2,2).
- **B2, A1, B3:** the sequence is 1 then 2. The pairs are (1,1), (1,2) and (2,2).
- **B2, B3, A1:** only (1,1) is possible.

So the possible pairs are 1 1, 1 3, 1 2, 3 3, 3 2 and 2 2.

**Combining with B1.**
- **B1 = 0:** B1 takes effect before A1. B2 and B3 can still fall anywhere relative to A1, so all six pairs occur.
- **B1 = 1:** A1 takes effect before B1, and therefore before B2 and B3. That is the order A1, B2, B3, which already gives all six pairs. For example, (1,1) occurs with the order A1, A2, A3, B1, B2, B3.

So 6 pairs × 2 values of B1 gives 12 combinations.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END