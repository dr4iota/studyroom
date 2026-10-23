The possible outcomes are the six combinations below, with values ordered Q1 Q2 Q3 Q4.

**Key facts**

- **Q1 and Q4 (B9 and final z):** Every z-write other than B8 happens before R, and B8 happens after R, so B8 is the last z-write. B9 reads it, so Q1 = Q4 = b2, the value B2 read from y.
- **Q3 (final y):** A8 is the only write to y, and it writes a7. A7 is preceded immediately by A6, which writes a4, so a7 = a4. Final y = a4.
- **a4:** A4 sees the later of A1 (value 6) and B1 (value 1), so a4 is 6 or 1, depending on whether B1 comes before or after A1.
- **b2:** B2 reads y. It sees a4 if A8 is before B2, and 0 otherwise.
- **Q2 (final x):** B7 is always after B5 and B6, so the final x is the later of A2 (value 1) and B7 (value 4). It is 4 if A2 is before B7, and 1 if B7 is before A2.
- **Infeasible cases:** If A8 is before B2, then A2 < A8 < B2 < B7, so final x must be 4. This rules out b2 = a4 with final x = 1.

**Feasible combinations** (each checked with an explicit ordering)

- a4=1, b2=0, final x=1: `0 1 1 0`
- a4=6, b2=0, final x=1: `0 1 6 0`
- a4=1, b2=0, final x=4: `0 4 1 0`
- a4=6, b2=0, final x=4: `0 4 6 0`
- a4=1, b2=1, final x=4: `1 4 1 1`
- a4=6, b2=6, final x=4: `6 4 6 6`

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END