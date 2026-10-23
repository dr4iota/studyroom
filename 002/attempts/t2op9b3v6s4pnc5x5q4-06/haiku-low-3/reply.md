The possible outcomes are six. Read values are fixed by which writes can precede them:

- **y is always 0.** The only write to y is B4, which writes B1's read of y, and B1 precedes it. So A4 and B1 both read 0.
- **z:** A5's write is overwritten by A6 (which writes 0, after S). Final z is 0 if A6 is the last z-write, or 1 if B6 is.
- **x:** The writes after S are B2 (writes 4), A8 (writes 0, after R), and B9 (writes B5's read, after P). B9 is always last.
- Let α be the time of A8 and β the time of B2. Then:
  - A9 reads 0 if β < α, and 4 if α < β.
  - B8 reads 0 if β < α < B8, and 4 otherwise.
  - B5 reads 0 if β < α < B5, and 4 otherwise. Final x equals B5's read.
  - A6 precedes B6 gives final z = 1; B6 precedes A6 gives final z = 0.

Checking which combinations are jointly realizable gives six outcomes, each verified with an explicit ordering. For example, (0 0 4 0) comes from S, B1, R, B2, B3, B4, Q, B5, B6, A6, A7, A8, A9, B7, B8, P, B9.

Asked: Q1 = A9, Q2 = B8, Q3 = final x, Q4 = final z.

BEGIN
0 0 0 1
0 0 4 0
0 0 4 1
0 4 4 0
0 4 4 1
4 4 4 1
END