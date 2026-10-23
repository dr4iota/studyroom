B3 can return **0**, **1** or **5**.

1. C2 reads x after C1 (which wrote 5) and before C4. No other thread writes x, so C2 returns 5. That means C5 writes 5 to y.
2. B3 reads y. The writes to y are:
   - A1 writes 1.
   - C5 writes 5.
   - A5 writes the value read by A3.
   - B4 writes 4, but B4 comes after B3 in thread B, so B3 cannot see it.
3. A3 runs after A1, so A3 returns 1, 4 (from B4) or 5 (from C5). A5 writes that value.
   - A5 could only write 4 if B4 took effect before A3. B4 comes after B3, so that A5 write would also come after B3. B3 therefore cannot see a 4 from A5.
   - A5 writing 1 or 5 before B3 is possible, but those values are already covered by A1 and C5.
4. The possible values for B3 are:
   - 0, if B3 reads before A1 and C5 take effect.
   - 1, from A1 (or from A5 copying 1).
   - 5, from C5 (or from A5 copying 5).

BEGIN
0
1
5
END