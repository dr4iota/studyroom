Possible values of B4: **0** and **4**. The value 3 is impossible.

**Key constraints**

- Only C5 writes z (to 3), and B5 reads z = 0, so B5 takes effect before C5. Since B1 precedes B5, z is still 0 at B1, so B3 writes 0 to x.
- A2 reads x = 3, so C2 is the last write to x before A2, which means C1 and B3 do not fall between C2 and A2.
- The only writes that can put 3 into y come from A4, which copies A3's read of z. Reading 3 requires A3 to come after C5. But B4 comes before B5, which comes before C5, and A4 must come before B4 for y to show 3 there. That would force A3 after C5 and before B4, which contradicts B4 < B5 < C5. So B4 = 3 is impossible.

**Value 0 is achievable.** Schedule:
A1 (y=4) at t=1, C1 at 2, C2 (x=3) at 3, A2 (reads 3) at 4, C3 (reads y=4) at 5, B1 (reads z=0) at 6, B2 (reads y=4) at 7, B3 (x=0) at 7.5, A3 (reads z=0) at 8, A4 (y=0) at 9, B4 (reads y=0) at 10, B5 (reads z=0) at 12, C4 (y=4) at 14, C5 (z=3) at 15.

**Value 4 is achievable.** Same schedule, but C4 (y=4) happens at 9.5, between A4 and B4, so B4 reads 4.

BEGIN
0
4
END