The reachable outcomes are the six combinations below. Q1 equals Q4, because B9 always reads the value B8 writes.

Key facts from the constraints:
- A1 precedes B5, B1 precedes A3, B2 precedes A9, and A9 precedes B8.
- A4 reads z as either 6 (A1 later than B1) or 1 (B1 later than A1), so Q3 is 1 or 6. A7 reads the same value, and A8 writes it to y, which is y's only write.
- B2 reads y as 0 (if A8 is after B2) or Q3 (if A8 is before B2). Call that value v.
- Final x is 1 (A2 after B7) or 4 (B7 after A2).
- Final z is v, because B8 comes after every other write to z. B9 reads that same value.
- If v = Q3 (A8 before B2), then B7 must come after A2, so final x is 4.

Each remaining combination is realized by an explicit interleaving. For example, (1 4 1 1) comes from A1, B1, A2–A8, B2, A9, B3–B9.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END