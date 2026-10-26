**Key facts from the rules**

- **Thread A:** A1 happens before S; A3 onward happens after P; A9 happens after Q and before R.
- **Thread B:** B1 happens before P; B2 happens before Q; B5 onward happens after S; B8 onward happens after R.
- Since A9 lies between Q and R, Q < R.

**Reducing the reads**

- **r4 (A4 reads z):** Only A1 (writes 6) and B1 (writes 1) precede A4, and both always do. So r4 = 1 if A1 < B1, and r4 = 6 if B1 < A1.
- **r7 (A7 reads z):** The last z-write before A7 is A6, which wrote r4. So r7 = r4.
- **y:** Only A8 writes y, with value r7. So **final y = r4**.
- **r2 (B2 reads y):** Either A8 precedes B2, giving r7, or it does not, giving 0.
- **r9 (B9 reads z):** B8 writes r2 to z, and it is the last z-write before B9, since A9 < R < B8. So **r9 = r2**.
- **final z:** B8 is the last z-write overall, so **final z = r2**.
- **final x:** The x-writes are A2 (1), B5 (3), B6 (r3), and B7 (4). B7 is last among the B-writes, so final x is 4 if A2 precedes B7, and 1 if B7 precedes A2.

**Feasibility**

- If A8 < B2, then A2 < A8 < B2 < B7, so final x = 4 is forced.
- If B2 < A8, then both final x = 1 and final x = 4 are achievable, for either value of r4. For example, with A1 < B1, the order A1, B1, B2, S, B3–B7, P, A2, A3–A8, Q, A9, R, B8, B9 gives final x = 1. Moving A2 before B7 gives final x = 4.

**Outcomes** (Q1 = r9, Q2 = final x, Q3 = final y, Q4 = final z)

| r4 | r2 | final x | Outcome |
|---|---|---|---|
| 1 | 0 | 1 | 0 1 1 0 |
| 1 | 0 | 4 | 0 4 1 0 |
| 1 | 1 | 4 | 1 4 1 1 |
| 6 | 0 | 1 | 0 1 6 0 |
| 6 | 0 | 4 | 0 4 6 0 |
| 6 | 6 | 4 | 6 4 6 6 |

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END