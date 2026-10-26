A2 can only have returned **0**.

1. A5 is known to return 0, so the last write to z before A5 must write 0. If no write to z came before A5, A5 would read 0 as well. But A3 is a write to z in thread A and comes before A5, so some write always precedes it.
2. The writes to z are:
   - B1 writes 4.
   - C5 writes the value read by C3. C3 comes after C2 (which writes 1 to y). The only other write to y that could come later is B3, which also writes 1. So C3 returns 1 and C5 writes 1.
   - A3 writes the value read by A2.
3. So the last write to z before A5 must be A3, and A3 must write 0. That means A2 returned 0. B1 must take effect before A3, and C5 must take effect after A5.
4. One execution shows this works: B1, A1, A2 (reads y = 0), A3 (writes 0 to z), C1, C2, B2, B3, A4 (reads y = 1), A5 (reads z = 0), then B4, C3, C4, C5.

BEGIN
0
END