A2 reads y, and y is only written by C4, which writes the value C1 read from z.

C1 reads z, which can be 0, 2 (from B1) or 4 (from A4 or C5). C5 comes after C1 in thread C, so C5 cannot affect C1. A4 can write 4 to z before C1 reads it.

So C4 can write 0, 2 or 4 to y, and A2 can read 0 (before C4) or any value C4 wrote.

Check each value for A2:
- 0: A2 reads y before C4 takes effect. Possible.
- 2: C1 reads z = 2 after B1 and before any write of 4 to z. Then C4 writes 2 to y, and A2 reads after that. Nothing else constrains this. Possible.
- 4: A4 writes 4 to z, and C1 reads z afterward, so C1 returns 4 if B1 does not overwrite it afterward. A4 comes after A2 in thread A, so A2 must come before A4. But C4 must take effect before A2, and C1 must read 4 before C4. That requires A4 to take effect before C1, which is before C4, which is before A2. This contradicts A2 before A4.
- The other source of 4 is C5, but C5 comes after C4 in thread C, so it cannot feed C1.

So A2 cannot return 4.

BEGIN
0
2
END