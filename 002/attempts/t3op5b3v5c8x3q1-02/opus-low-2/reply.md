**Q1 (the value read by A2) can be 0 or 2.**

1. **What writes y.** Only C4 writes to y. It writes the value C1 read from z. So A2 returns either 0 (if no write to y has taken effect yet) or whatever C1 read.

2. **What C1 can read from z.** Three writes could come before C1:
   - B1 writes 2.
   - A4 writes 4.
   - A5 writes the value A3 read from x. Only A1 writes x, and A1 comes before A3, so A3 returns 2 and A5 writes 2.

   C5 also writes z, but it comes after C1 in thread C. So C1 returns 0, 2 or 4.

3. **A2 = 4 is impossible.** For C1 to read 4, A4 must take effect before C1. But A2 comes before A4 in thread A, and C4 comes after C1 in thread C. So the order would have to be A2 → A4 → C1 → C4. C4 then writes y after A2 has already read it, so A2 cannot see the 4.

4. **A2 = 2 is possible.** Use the order B1 → C1 (reads 2) → C4 (writes 2 to y) → A2. A2 then returns 2.

5. **A2 = 0 is possible.** Let A2 take effect before C4. No write to y has happened yet, so A2 returns 0.

BEGIN
0
2
END