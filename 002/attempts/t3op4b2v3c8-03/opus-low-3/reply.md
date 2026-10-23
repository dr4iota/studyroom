Every read of y returns 0 or 3, and every combination of those with a final x of 0, 1 or 3 can happen. That gives all 12 combinations.

**Which values are possible at all**

- **Values in y:** A1 writes 3 to y. B3 and C4 each write back a value that was read from y. So y only ever holds 0 or 3.
- **Values in x:** B1 writes 1 and C3 writes the value C1 read (0 or 3).
  - If C3 takes effect before B1, the final x is 1.
  - Otherwise the final x is C1's value, 0 or 3.

**Final x = 1 (C1 reads 0 and C3 takes effect before B1)**

| A3 | B4 | Order |
|----|----|-------|
| 3 | 3 | C1=0, C2, C3, B1, C4, A1, A2, A3, B2=3, B3, B4 |
| 0 | 0 | C1=0, C2, C3, B1, A1, C4, A2, A3, B2=0, B3, B4 |
| 0 | 3 | C1=0, C2, C3, A1, B1, B2=3, B3, B4, C4, A2, A3 |
| 3 | 0 | C1=0, C2, C3, B1, B2=0, B3, C4, B4, A1, A2, A3 |

**Final x = 0 (C1 reads 0 and C3 takes effect after B1)**

Start with B1, C1=0, C2, C3. Then continue with the same orders as above for the remaining steps. All four (A3, B4) pairs occur.

**Final x = 3 (C1 reads 3, so C1 is after A1, and C3 is after B1)**

| A3 | B4 | Order |
|----|----|-------|
| 3 | 3 | All of A first, then all of B, then all of C. Every write to y is 3. |
| 0 | 0 | B1, B2=0, A1, C1=3, B3, B4, A2, A3, C2, C3, C4 |
| 0 | 3 | B1, B2=0, A1, C1=3, B3, A2, A3, C2, C3, C4, B4 |
| 3 | 0 | B1, B2=0, A1, A2, A3, C1=3, B3, B4, C2, C3, C4 |

BEGIN
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 0 0
3 0 1
3 0 3
3 3 0
3 3 1
3 3 3
END