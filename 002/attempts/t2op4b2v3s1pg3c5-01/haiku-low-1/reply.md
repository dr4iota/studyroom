The possible outcomes are 14 combinations of (Q1, Q2, Q3). Q1 and Q2 are the values read by A2 and A3, and Q3 is the final value of x.

**Key facts:**
- B1 always reads 0, since no write to x can precede it.
- The writes to x occur in the order 3 (B2), then 2 (B3), then 1 (B4). B2 always precedes P, and A3's read always follows P. A4 writes Q2 at a time after A3.
- A2's read can fall before or after P, and its position is not otherwise constrained. A2's read precedes A3's read, which precedes A4's write.
- So Q1 can be 0, 3, 2, or 1, and Q2 can be 3, 2, or 1 (never 0, since B2 always precedes A3's read).
- Q1 ≤ Q2 in the write sequence 0 → 3 → 2 → 1.
- The final value is either Q2 (if A4's write lands after B4) or 1 (if B4 lands after A4).

**Enumeration:**

| Q1 | Q2 | Q3 |
|---|---|---|
| 0 | 3 | 3 or 1 |
| 0 | 2 | 2 or 1 |
| 0 | 1 | 1 |
| 3 | 3 | 3 or 1 |
| 3 | 2 | 2 or 1 |
| 3 | 1 | 1 |
| 2 | 2 | 2 or 1 |
| 2 | 1 | 1 |
| 1 | 1 | 1 |

BEGIN
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END