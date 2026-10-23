**B4 can return 0 or 4. It cannot return 3.**

**What is forced**

1. B5 returns 0, and the only write to z is C5 (3). So C5 takes effect after B5. B1 comes before B5, so B1 reads z = 0. B3 therefore writes 0 to x.
2. B4 reads y. The writes to y are A1 (4), C4 (4) and A4. A4 writes whatever A3 read from z, which is 0 or 3.

**B4 = 3 is impossible**

For A4 to write 3, A3 must take effect after C5. C5 is after B5, and B5 is after B4, so A4 is after B4. B4 can never see the value 3.

**B4 = 4 is possible**

Run C1, C2, A1, C3 (y=4), A2 (x=3), B1 (z=0), B2 (y=4), B3, B4 (y=4), B5 (z=0), C4, C5, A3, A4. Every known result matches.

**B4 = 0 is possible**

Run A1, C1, C2, C3 (y=4), A2 (x=3), B1 (z=0), B2 (y=4), A3 (z=0), A4 (y←0), B3, B4 (y=0), B5 (z=0), C4, C5. Every known result matches.

BEGIN
0
4
END