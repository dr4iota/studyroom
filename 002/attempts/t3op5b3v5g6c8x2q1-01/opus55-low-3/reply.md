**Final value of z: 2 or 4.**

1. **B1 reads 0.** Only B3 writes to y, and B3 comes after B1 in thread B. So B1 sees the initial 0, and B2 writes 0 to z.

2. **C2 lands between B2 and B4.** The writes to z are A1 (2), B2 (0), C1 (1) and C2 (4). B4 is known to return 4, so C2 must be the last write to z before B4. B2 comes before B4 in thread B, so B2 must take effect before C2.

3. **The final value can only be 2 or 4.**
   - It cannot be 0: B2 is always followed by C2.
   - It cannot be 1: C1 always comes before C2 in thread C.
   - It is 4 if A1 takes effect before C2.
   - It is 2 if A1 takes effect after C2. This is allowed because nothing orders thread A against B or C. For example, run A1 and the rest of thread A after B4 and C4 have finished. Every known result still holds: A3 and A4 read x = 1 from A2, and B4 has already read 4.

BEGIN
2
4
END