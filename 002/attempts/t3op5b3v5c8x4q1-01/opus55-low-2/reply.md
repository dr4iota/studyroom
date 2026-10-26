**C4 can only return 2.**

1. **What C3 tells us.** C3 reads z = 2, so A4 or A5 wrote 2. Both write the value read by A3, so A3 read 2.

2. **What C4 can see.** C4 comes after C3, and C3 comes after A4 at the earliest. So C4 happens after A3, A2 and C2. The writes to y are A2, B3 (writes 4) and C2 (writes 2). Since C2 is before C4, C4 cannot read 0. C4 can only read 2 or 4.

3. **C4 cannot read 4.** For C4 to read 4, B3 must be the last write to y before C4. Then A2 and C2 both take effect before B3, so no write to y takes effect after B3. B4 comes after B3, so B4 would read 4. That contradicts B4 returning 2.

4. **C4 can read 2.** One valid order is: C2 (y = 2), A1 (reads 2), B3 (y = 4), A2 (y = 2), B4 (reads 2), A3 (reads 2), A4 (z = 2), A5 (z = 2), C3 (reads 2), C4 (reads 2). B1 and C1 can go anywhere before B3 and C2, since x is never read.

BEGIN
2
END