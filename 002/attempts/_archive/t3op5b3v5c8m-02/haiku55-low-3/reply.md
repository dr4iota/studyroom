**Reasoning summary**

- **Q1 (A3's read of x):** x is written by C2 (2), C3 (1), and B4 (which writes B3's value). Possible values are 0, 1, 2, 4.
- **Q2 (B3's read of y):** y is written by B2 (1), A2 (1), and A1 (4). B3 follows B2, so it reads 1 or 4. It reads 4 only if A1 falls between B2 and B3.
- **Joint (Q1, Q2):** A3 sees B4's value only if B4 comes before A3. This gives the pairs (0,1), (0,4), (2,1), (2,4), (1,1), (1,4), (4,4).
- **Q3 (final z):** z is written by B1 (4), A4 (A3's value), C4 (C1's value), and C5 (4). C5 always comes after C4, so C4 can never be the last z-write. The final value is therefore 4 (C5 or B1 last) or A3's value (A4 last). Each of these is achievable for every pair above, because A4 and C5 can be placed freely relative to the x and y operations.

**Combinations**

BEGIN
0 1 0
0 1 4
0 4 0
0 4 4
1 1 1
1 1 4
1 4 1
1 4 4
2 1 2
2 1 4
2 4 2
2 4 4
4 4 4
END