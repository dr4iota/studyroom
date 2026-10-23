Only B1 writes x, so every read of x returns 0 or 3. B3 comes after B1 in thread B, so B3 returns 3. Hence B4 writes 3 to y.

The writes to y are B4 (value 3) and C5 (value 4), so the final y is 3 or 4, depending on which comes last.

The writes to z are A1 (1), B2 (1) and A4 (the value A2 read, which is 0, 3 or 4). So C3 can return 0, 1, 3 or 4.

**C3 = 0.** The order C1, B1, C2, C3 works, with A1 and B2 both after C3. B4 and C5 can then fall in either order, so the final y can be 3 or 4. This gives (0,3) and (0,4).

**C3 = 1.** A1 or B2 writes 1 before C3. C5 comes after C4, which is after C3, so C5 can come before or after B4. This gives (1,3) and (1,4).

**C3 = 3.** A4 must write 3, so A2 read 3, which means B4 came before A2. The chain is B4 < A2 < A4 < C3 < C4 < C5, so C5 is last and the final y is 4. This gives (3,4). Final y = 3 is impossible here.

**C3 = 4.** A4 would have to write 4, so A2 read 4, which needs C5 before A2. But C5 comes after C3, which comes after A4 and A2. This is impossible.

BEGIN
0 3
0 4
1 3
1 4
3 4
END