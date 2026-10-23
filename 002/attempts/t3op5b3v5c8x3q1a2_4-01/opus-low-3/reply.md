**Possible values of B3: 0, 1, 5**

Before B4 (its own later write), B3 can only see writes to y from threads A and C, or the initial value.

1. **C5 always writes 5.** C2 reads x after C1 wrote 5, and C4 (write 4) comes after C2 in thread C. No other thread writes x, so C2 returns 5 and C5 writes 5 to y.

2. **A5 writes 1, 5 or 4**, depending on what A3 read:
   - A3 returns 1 if A1's write is still the latest.
   - A3 returns 5 if C5 took effect between A1 and A3.
   - A3 returns 4 only if B4 took effect before A3. Since B3 comes before B4, A5 then happens after B3, so this value can never reach B3.

3. **Each candidate value for B3 can actually occur:**
   - **0:** B3 runs before A1 and C5.
   - **1:** B3 runs after A1 and before C5.
   - **5:** B3 runs after C5. This works whether C5's own write or A5 copying 5 was the latest.

BEGIN
0
1
5
END