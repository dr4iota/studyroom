Each asked value is limited by which writes can come before it.

- **Q1 (A1 reads z):** A1 is the first operation in A, so none of A's own writes to z have happened yet. The only other writes to z are B1 (3) and B3 (2). A1 can therefore return 0, 3 or 2.
- **Q2 (A5 reads y):** The only write to y is B5 (4). A5 returns 4 if B5 takes effect before it, otherwise 0.
- **Q3 (B4 reads x):** The only write to x is A4 (1). B4 returns 1 if A4 takes effect before it, otherwise 0.

Every combination of these three values can occur. Each ordering below is a consistent interleaving of the operations. The pairs below are (Q2, Q3), and the same orderings work for each Q1 value:

- **(0, 0):** Run B1–B4, then A2–A5, then B5. B4 reads x before A4, and A5 reads y before B5.
- **(0, 1):** Run all of A, then all of B. A4 comes before B4, and A5 comes before B5.
- **(4, 0):** Run B1–B5, then A2–A5. B4 reads x before A4, and A5 reads y after B5.
- **(4, 1):** Run A2–A4, then B2–B5, then A5. B4 reads x after A4, and A5 reads y after B5.

The Q1 value is set by where A1 falls relative to B1 and B3:

- **A1 = 0:** Put A1 before B1.
- **A1 = 3:** Put A1 after B1 and before B3, with A2 and later after B3. Each pair is still possible because B4 and B5 come later and can be ordered either way against A4 and A5.
- **A1 = 2:** Put A1 after B3, with B1–B3 before it. Each pair is still possible because B4 and B5 come later and can be ordered either way against A4 and A5.

That gives 3 × 2 × 2 = 12 combinations.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
3 0 0
3 0 1
3 4 0
3 4 1
2 0 0
2 0 1
2 4 0
2 4 1
END