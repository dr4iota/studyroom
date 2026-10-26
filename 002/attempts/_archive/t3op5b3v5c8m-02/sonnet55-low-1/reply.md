Since no operation has a sync point, each operation takes effect at one instant, and every outcome comes from some interleaving of the three threads' program orders.

**Q2, the value B3 returns.** B3 comes after B2, which writes 1 to y, so it never reads 0. It reads 4 only if A1 falls between B2 and B3 and A2 comes after B3. So B3 is 1 or 4.

**Q1, the value A3 returns.** The writes to x come from C2 (2), C3 (1) and B4 (the value of B3, which is 1 or 4). A3 can also read the initial 0.
- A3 = 0 is possible when A3 runs before any write to x. This works with either value of B3.
- A3 = 2 is possible when A3 runs between C2 and C3, with B4 after A3. This also works with either value of B3.
- A3 = 1 is possible through C3 or through B4 with B3 = 1, and it also works with B3 = 4.
- A3 = 4 is possible only when B3 = 4. B4 must write 4 to x and finish after C2 and C3, before A3. B3 = 4 forces A2 after B3, so A3 comes after B4, and that order is consistent.
- A3 = 4 is impossible when B3 = 1, because nothing else can write 4 to x.

**Q3, the final value of z.** The writes to z are B1 (4), C4, C5 (4) and A4 (the value of A3).
- If C5 is last, or if A4 writes 4, the final value is 4. C5 can always be placed last, so 4 is always reachable.
- If A4 runs after C5, the final value is whatever A3 read. A3 only needs to read early enough, and A4 can be delayed until after C5, so this is always achievable.
- So for each (A3, B3) pair the final z is 4 or A3's value.

Combined, with B3 = 1 the A3 values are 0, 1 and 2. With B3 = 4 the A3 values are 0, 1, 2 and 4.

BEGIN
0 1 0
0 1 4
1 1 1
1 1 4
2 1 2
2 1 4
0 4 0
0 4 4
1 4 1
1 4 4
2 4 2
2 4 4
4 4 4
END