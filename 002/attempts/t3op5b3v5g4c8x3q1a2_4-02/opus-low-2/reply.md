C4 can return 1, 2 or 4.

**Fixed constraints**
- B1 reads y = 1, so it takes effect after A1 (write 1 to y) and before C3 (write 4 to y).
- A4 reads y = 4, so it takes effect after C3.
- B2 reads y, so it returns 1 if it comes before C3 and 4 if it comes after.
- B3 writes the value B2 read to z, so it writes 1 or 4.
- C4 comes after C1, so it sees C1's 2 or a later write to z.
- The writes to z are A2 (1), C1 (2) and B3 (1 or 4). So C4 can only return 1, 2 or 4.

**C4 = 2:** A1, A2, B1, B2 (reads 1), B3 (z = 1), C1, C2, C3, C4, A3, A4, A5, B4. No write to z falls between C1 and C4.

**C4 = 1:** A1, C1, A2, B1, B2, B3, C2, C3, C4, A3, A4, A5, B4. A2 writes z = 1 after C1. B2 reads 1, so B3 also writes 1.

**C4 = 4:** A1, B1, C1, C2, C3, B2 (reads 4), B3 (z = 4), C4, A2, A3, A4, A5, B4. B3 writes 4 to z after C1 and before C4.

BEGIN
1
2
4
END