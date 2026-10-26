Writes to x, in time order:
- B2 writes 3 and takes effect before P.
- B3 writes 2 and B4 writes 1, both after P, with B3 before B4.
- A4 writes A3's value after A3, and after P.

A2 takes effect somewhere in its start-to-end window, which straddles P. A3 takes effect after A2 and after P. B1 always reads 0, and A1 always reads 0 because y is never written.

Working through the cases:
- **A3 = 3** (A3 before B3): A2 can be 0 or 3. The final value is 1 if A4 lands before B4, or 3 if A4 lands after B4.
- **A3 = 2** (between B3 and B4): A2 can be 0, 3, or 2. The final value is 1 if A4 lands before B4, or 2 if after.
- **A3 = 1** (after B4): A2 can be 0, 3, 2, or 1. A4 writes 1, so the final value is 1.

That gives 14 outcomes.

BEGIN
0 1 1
0 2 1
0 2 2
0 3 1
0 3 3
1 1 1
2 1 1
2 2 1
2 2 2
3 1 1
3 2 1
3 2 2
3 3 1
3 3 3
END