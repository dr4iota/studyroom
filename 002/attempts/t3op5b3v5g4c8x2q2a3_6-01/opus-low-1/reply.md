C3 always returns 0, and the final value of z can be 0, 1 or 5.

**C3 is always 0.**
- The only write to z is B5, so a read of z returns 0 unless it comes after B5 and B5 wrote something other than 0.
- C3 runs before C4, and C4 is known to return 0.
- If B5 writes 0, every read of z returns 0, including C3.
- If B5 writes a nonzero value, C4 must take effect before B5. C3 comes before C4, so it is also before B5 and returns 0.

**The final z equals the value B4 read from y.** B4 runs after B3, so it sees one of three writes:
- **1** comes from B3, or from C1 if C1 takes effect between B3 and B4.
- **A4's value** is possible if A4 takes effect between B3 and B4. A4 writes what A1 read from x, which is 0 (A1 before B2) or 5 (A1 after B2).

So z ends as 0, 1 or 5. Each case must also fit the known results, and each does:
- **z = 5:** B1, B2, then A1 reads 5, A2 reads 0 and A3 reads 5. Then B3, then A4 writes 5, then B4 reads 5. C3 and C4 run before B5, and B5 writes 5.
- **z = 0:** A1 reads 0 before B2. B1, B2, B3 follow, then A2 reads 0 and A3 reads 5. A4 writes 0 to y, then B4 reads 0 and B5 writes 0, so A2 and C4 read 0 whenever they run.
- **z = 1:** B4 reads B3's 1. A2, C3 and C4 all take effect before B5.

BEGIN
0 0
0 1
0 5
END