All 27 combinations are possible, since every operation is a single instant and there are no sync points. The argument below checks the extremes and then shows the intermediate cases follow the same pattern.

**Possible values of each quantity**

- B1 reads y, which can be 0, 2 or 3 depending on whether A2 or D2 has run. So B's value b1 is 0, 2 or 3.
- C1 reads x, which can also be 0, 2 or 3, so C2 can write 0, 2 or 3 to x.
- A3 comes after A1, but a later write of 0 by B4 or C2 can still leave x at 0. It can also see 2 (A1, C3, D1) or 3 (D3, D4, or a copied 3). So Q1 is 0, 2 or 3.
- Final x is decided by the last x-write. D4 gives 3, C3 gives 2, and B4 can give 0, 2 or 3. So Q2 is 0, 2 or 3.
- Final y is decided by the last y-write among A2 (2), B2 (b1) and D2 (3). So Q3 is 0, 2 or 3.

**Checking the hardest combinations**

- **Final y = 0 requires b1 = 0.** B1 must run before A2 and D2, and B2 must be the last y-write.
- **A3 = 0 with final x = 0, y = 0.** Order: B1(0), C1(0), A1, A2, C2(0), A3(0), D1, D2, B2(0), B3, D3, D4, C3, B4(0). B4 writes 0 last, so x ends at 0 and y ends at 0.
- **A3 = 0 with final x = 0, y = 2.** Order: B1(0), C1(0), D1, D2, A1, B2(0), A2, C2(0), A3(0), B3, D3, D4, C3, B4(0). The y-writes run D2 (3), B2 (0), A2 (2), so y ends at 2. B4 writes 0 last, so x ends at 0.
- **Other combinations.** The other cases are variations on these orders. For example, reordering so D2 is last gives y = 3, and ending with C3 or D4 gives x = 2 or 3.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END