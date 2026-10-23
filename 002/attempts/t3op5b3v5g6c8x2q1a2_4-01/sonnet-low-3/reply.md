The final value of z can be 2 or 4.

**What B1 reads.** The only write to y is B3, and it comes after B1 in thread B. So B1 reads 0. That makes B2 write 0 to z and B3 write 0 to y.

**What B4 returning 4 implies.** The only write of 4 to z is C2. B4 returned 4, so C2 took effect after B2 and before B4. No other write to z took effect between C2 and B4.

**Which writes can come last.**
- B2 must come before C2, so it cannot be the last write to z.
- C1 comes before C2 in thread C, so it cannot be last either.
- C2 can be last if A1 takes effect before C2, or before B4 is forced to see 4. In that case the final value is 4.
- A1 can be last if it takes effect after B4. Thread A's later reads of x are unaffected, because x is only written by A2 and all of thread A's reads of x return 1. The final value is then 2.

Both outcomes are consistent with every known result.

BEGIN
2
4
END