B4 can return **3** or **5**.

**1. Final y = 0.** Three operations write to y: A1 writes 3, C1 writes 3, and B2 writes whatever B1 read. For y to end at 0, the last write to y must be B2, and B1 must have read 0. For B1 to read 0, it must take effect before both A1 and C1. So B2 takes effect after A1 and after C1.

**2. Final x = 3.** Two operations write to x: C2 writes 5, and C5 writes whatever C3 read. For x to end at 3, C5 must be the last write and C3 must have read 3. C3 takes effect after C1, so it sees y = 3 only if it takes effect before B2, which writes 0. So C3 is before B2.

**3. What B4 can see.** Thread C's order puts C2 before C3, and step 2 puts C3 before B2. Thread B's order puts B2 before B4. So C2 (x = 5) always takes effect before B4.
- C5 (x = 3) comes after C3 and C4, but nothing ties it to B4.
- If C5 takes effect after B4, then B4 returns 5.
- If C5 takes effect before B4, then B4 returns 3.

BEGIN
3
5
END