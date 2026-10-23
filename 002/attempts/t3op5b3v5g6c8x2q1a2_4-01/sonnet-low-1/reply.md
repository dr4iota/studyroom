The possible final values of z are 2 and 4.

**Values of y.** Only B3 writes y, and it writes the value B1 read. B1 runs before B3, so B1 reads 0. Therefore B2 writes 0 to z, B3 writes 0 to y, and C3 reads 0.

**What "B4 returned 4" forces.** The only write of 4 to z is C2. So C2 must be the last write to z before B4 takes effect. This gives these constraints:
- C2 takes effect before B4.
- B2 (which writes 0) takes effect before C2. B2 precedes B4 in program order, so it cannot fall between C2 and B4.
- C1 (which writes 1) takes effect before C2, by program order.
- A1 (which writes 2) either takes effect before C2 or after B4. It cannot fall between them.

**Final value of z.** The final value is the last write to z overall.
- If A1 takes effect before C2, then C2 is the last z write, so the final value is 4.
- If A1 takes effect after B4, then A1 is the last z write, so the final value is 2.
- The final value cannot be 0 or 1, because B2 and C1 both precede C2.

Both cases are consistent with the other known results. A2 writes x=1, and the reads A3 and A4 of x can return 1 after it. Nothing else writes x. Thread A's operations are ordered A1, A2, and so on, so A1 can happen late as long as A3 and A4 come after it. This is compatible with A1 taking effect after B4.

BEGIN
2
4
END