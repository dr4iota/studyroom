**Q1 (the value C2 returns) can be 0 or 5.**

1. **Values that can reach z.** The writes to z are B3 (writes 2) and C3 (writes C1's result, which is 0). So A2 returns either 0 or 2.

2. **A2 cannot return 2.**
   - If A2 returned 2, A2 comes after B3. B3 comes after B1 because they are in thread B's order. So A1, B1 and A2 all come before A3.
   - A3 would then write 2 to y, and no write to y comes after A3.
   - A4 would return 2, which contradicts the known result of 5.
   - So A2 returns 0 and A3 writes 0 to y.

3. **Writes to y.** The writes are A1 (5), B1 (5) and A3 (0). For A4 to return 5, B1 must take effect after A3. The value 2 never reaches y.

4. **C2 = 0 is possible.**
   - Order: C1 (reads z = 0), then C2 (reads y = 0, nothing written yet).
   - Then A1, A2 (reads z = 0), A3 (writes 0), B1 (writes 5), A4 (reads 5).
   - Then B2, B3, B4, C3, C4.

5. **C2 = 5 is possible.**
   - Order: A1 (writes 5), C1 (reads z = 0), C2 (reads y = 5).
   - Then A2 (reads z = 0), A3 (writes 0), B1 (writes 5), A4 (reads 5).
   - Then the remaining operations.

BEGIN
0
5
END