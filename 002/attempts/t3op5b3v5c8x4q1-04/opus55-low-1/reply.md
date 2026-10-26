**Possible final values of z: 4 and 5.**

1. **Where A4's 5 comes from.** A4 reads z = 5, but A2 wrote 3 to z earlier in thread A. So some write of 5 to z must take effect after A2 and before A4. The candidates are:
   - **A1** writes 5, but it comes before A2, so it cannot be that write.
   - **B2** writes the value B1 read from x. x only becomes 5 through A5, which comes after A4. So B2 cannot write 5 in time.
   - **C5** writes the value C4 read from z. This is the only option, so C5 writes 5, and it takes effect between A2 and A4. No other z write falls between C5 and A4.

2. **Where C4's 5 comes from.** For C5 to write 5, C4 must have read 5. The only 5 available is A1's write. So C4 takes effect between A1 and A2, with no other z write in between.

3. **Which write to z is last.** The writes to z are A1, A2, B2, B3, C2 and C5. A1 and A2 come before C5. C2 comes before C4, so also before C5. B2 always comes before B3. So the last write is either C5 or B3.
   - **Final z = 4:** B3 takes effect after C5, for example after A4.
   - **Final z = 5:** B1, B2 and B3 all run before C2 and A1, so C5 is the last write.

BEGIN
4
5
END