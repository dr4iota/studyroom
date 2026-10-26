Every outcome has A9 = 0. The other three values vary, giving five combinations.

**Values forced by the sync points**
- A1–A5 all end before S, and B1 starts after S. No write to y has happened by then, so A4 = 0 and B1 = 0.
- Therefore A6 and B3 write 0 to z, A8 writes 0 to x, and B4 writes 0 to y.
- B2 (write 4 to x) ends before R, and A7 starts after R, so A7 reads 4.
- A8 comes after A7, so B2 is before A8.
- A9 comes after A8 and ends before P. B9 starts after P, so B9 is after A9. Between A8 and B9, nothing writes a non-zero value to x, so A9 = 0.

**B5 and B8**
- B5 comes after B2, so it reads 4 if it runs before A8, or 0 if it runs after A8.
- B8 comes after B5 and before B9, so B9 has not yet written. B8 therefore reads 4 or 0.
- If B5 = 0, A8 has already happened, so B8 = 0.
- If B5 = 4, B8 can be 4 (before A8) or 0 (after A8).

**Final x**
B9 is the last write to x and writes B5's value, so x is 4 if B5 = 4 and 0 if B5 = 0.

**Final z**
The writes to z are A5 (3), A6 (0), B3 (0) and B6 (1).
- If B5 = 0, then B6 comes after A8, which comes after A6, so z = 1.
- If B5 = 4, B6 can be either before or after A6.
  - B6 before A6 gives z = 0, which is possible because B5 and B6 can both run before R.
  - B6 after A6 gives z = 1.
- This holds for B8 = 4 and for B8 = 0. For B8 = 0, B6 can still run before A6 and B8 after A8.

BEGIN
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
0 0 0 1
END