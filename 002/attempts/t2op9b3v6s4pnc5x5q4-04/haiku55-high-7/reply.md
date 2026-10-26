Under the rules, six outcomes are possible for (Q1, Q2, Q3, Q4).

**Key facts**

- Q1 = Q4: B8 is always the last write to z before B9, and it always comes after A9, B1, A6 and A1. So B9 and the final z both equal the value B2 read.
- Q3: A8 is the only write to y, and it always writes the value A4 read, so the final y equals that value.
- Q2: the final x is 4 if B7 comes after A2, and 1 if A2 comes after B7.
- The value A4 read is 6 if A1 comes before B1, and 1 if B1 comes before A1.
- B2 reads y, so it gets 0 if A8 comes after B2, and the value A4 read if A8 comes before B2.
- If A8 comes before B2, then A2 comes before B7, so final x cannot be 1 in that case.

**Feasible combinations**

- A4 read 1 (B1 before A1 is not this case; A1 before B1): (Q1, Q2) = (1, 4), (0, 1), (0, 4)
- A4 read 6 (B1 before A1): (Q1, Q2) = (6, 4), (0, 1), (0, 4)

Each is realized by an interleaving. For example, `0 1 1 0` comes from A1, B1, B2 (reads 0), B3, B4, B5, B6, B7, A2, A3–A9, B8, B9. Also (1, 1) for Q1 and Q2 is impossible, as noted above.

BEGIN
0 1 1 0
0 4 1 0
1 4 1 1
0 1 6 0
0 4 6 0
6 4 6 6
END