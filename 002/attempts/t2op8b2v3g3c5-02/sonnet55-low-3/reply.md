Every x write stores the value A1 read. A1 can only see 0, because B1 reads 0 and the only writes to x (A3 and A6) store A1's own value. So A1 = 0, and A3 and A6 write 0 to x. A5 writes 0 to y.

The writes to y are B3 (1), B4 (2), B7 (the value B5 read), A4 (3) and A5 (0).

A2 returns 2 and comes before A4 and A5. The only source of a 2 is B4, or B7 after B4. So B3 < B4 < A2 < A4 < A5 < A7 in the order the operations take effect. B5, B6 and B7 all come after B4.

**Case 1: B7 takes effect before A5.**
- B5 reads 2 or 3, and B6 comes before B7, so B6 cannot see A5's 0.
- If B5 = 2, B6 can be 2 or 3. If B5 = 3, B6 = 3.
- A5 is the last write, so A7 = 0 and the final y is 0.
- Combinations (A7, B6, final y): 0 2 0 and 0 3 0.

**Case 2: B7 takes effect after A5.** The final y is B7's value, which is B5's value.
- B5 = 2, so B5 is before A4. B6 can be 2, 3 or 0. A7 is 0 if it is before B7 and 2 if it is after. Final y is 2. This gives 0 2 2, 0 3 2, 0 0 2, 2 2 2, 2 3 2 and 2 0 2.
- B5 = 3, so B5 is between A4 and A5. B6 is 3 or 0. A7 is 0 or 3. Final y is 3. This gives 0 3 3, 0 0 3, 3 3 3 and 3 0 3.
- B5 = 0, so B5 is after A5. B6 = 0, A7 = 0 and the final y is 0. This gives 0 0 0.

BEGIN
0 2 0
0 3 0
0 0 0
0 2 2
0 3 2
0 0 2
2 2 2
2 3 2
2 0 2
0 3 3
0 0 3
3 3 3
3 0 3
END