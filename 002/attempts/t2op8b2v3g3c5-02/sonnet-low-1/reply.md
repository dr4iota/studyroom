Only A writes to x, and only after A1, so A1 reads 0. Every write to x is therefore 0, and B1 returning 0 is consistent.

For y, A2 returned 2. The only writes of 2 are B4 and B7, and B7 comes after B4, so B4 takes effect before A2. A2 comes before A4 and A5. Let v5 be the value B5 reads. It can only be 2, 3 or 0. B7 writes v5 and comes after B5.

**v5 = 2.** B5 reads 2, so it comes before A4. The writes after A2 are A4 (3), A5 (0) and B7 (2).
- If B7 comes before A5, the last write is A5, so A7 = 0 and the final y is 0. B6 can be 2, 3 or 0.
- If B7 comes after A5, B7 is the last write, so the final y is 2. A7 is 0 if it precedes B7, or 2 if it follows. B6 can be 2, 3 or 0.

**v5 = 3.** B5 reads 3, so it falls between A4 and A5. B6 is 3 or 0.
- If B7 comes before A5, A7 = 0 and the final y is 0.
- If B7 comes after A5, the final y is 3. A7 is 0 or 3.

**v5 = 0.** B5 comes after A5, so everything reads and writes 0. A7 = 0, B6 = 0, and the final y is 0.

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