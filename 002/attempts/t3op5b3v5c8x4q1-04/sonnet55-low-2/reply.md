Only 4 and 5 are possible for the final value of z.

**What A4 = 5 forces.** A1 writes 5 and A2 then writes 3, so A4 can only read 5 if some later write put 5 back into z. The candidates are:
- B2 writes the value B1 read from x, which is 0 or 3, never 5.
- B3 writes 4, C2 writes 3 and A2 writes 3, so none of these is 5.
- C5 writes whatever C4 read, so it can write 5 if C4 read A1's 5.

So C4 must read z after A1 and before any other write changes it, and C5 must then take effect after A2 and before A4. Program order gives C2 before C4, so C2 takes effect before A1 or at least before C4's read. B2 and B3 cannot take effect between C4's read and A4's read, because that would overwrite the 5 that A4 must see.

**Where B2 and B3 can go.** B2 and B3 must each fall either before A1 or after C5. B2 comes before B3 in program order, so there are two cases:
- **B3 after C5:** B3 writes 4 and is the last write to z, so the final value is 4. This is possible, for example with B2 and B3 both after A4.
- **B2 and B3 both before A1:** C5 is then the last write to z, so the final value is 5.

A final value of 3 or 0 would need B3 to precede some write of 3 or 0, but B3 always comes after B2 and cannot land in the forbidden window. No other write ends up last with those values.

BEGIN
4
5
END