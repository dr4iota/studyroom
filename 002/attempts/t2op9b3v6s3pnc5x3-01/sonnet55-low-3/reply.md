Every outcome has A9 = 5. The final y is 4 or 6, and the final z is 4 or 6.

**Q1 (A9).** B1–B5 all end before P, and A7 starts after P. A8 ends before Q, and B7–B9 start after Q. A9 comes after A8 in thread A, so it also comes after A8 in time. The earlier x-writes (B2 and B4, both 1) take effect before A8, so they can't be the last write before A9. After A8 (x=5), the only other x-write is B9. B8 runs after Q, and therefore after A8, so it reads 5, and B9 writes 5 back. So every write to x that takes effect before A9 and after A8 is 5, and A9 returns 5.

**Q2 (final y).** The y-writes are A1 (5), A2 (4), B5 (6), and A6 (the value A4 read).
- A4 comes after A2, so it reads 4 or 6 and never 5.
- If A4 reads 6, then A6 writes 6 and the final y is 6.
- If A4 reads 4, then B5 can fall in one of three places:
  - before A2, or between A4 and A6, which leaves y at 4;
  - after A6, which makes y 6.

So the final y is 4 or 6.

**Q3 (final z).** The z-writes are B1 (2), B3 (6), A3 (1), and A5 (the value A4 read). B1 and B3 can never be last, because A3 and A5 can't both precede B3 and B1 in a way that leaves 1 or 2. In particular, A5 always writes after A3, so the final z is either B3's 6 or A5's value (4 or 6).

**Which combinations occur.**
- z=4, y=4: A4 reads 4, B3 comes before A5, and B5 is before A2.
- z=4, y=6: A4 reads 4, B3 comes before A5, and B5 comes after A6.
- z=6, y=4: A4 reads 4, the order is A5, B3, B5, A6.
- z=6, y=6: A4 reads 6.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END