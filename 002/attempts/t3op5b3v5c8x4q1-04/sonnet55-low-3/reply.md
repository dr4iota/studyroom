Only two final values of z are possible: 4 and 5.

**Which write supplies the 5 that A4 reads.** A1 writes 5 and A2 then writes 3, both before A4. So A4 can read 5 only if another write of 5 to z takes effect after A2 and before A4. There are two candidates:

- **B2** writes whatever B1 read from x. The only way x can hold 5 is through A5, which runs after A4. So B2 cannot supply a 5 before A4.
- **C5** writes whatever C4 read from z. This works if C4 reads 5 while A1's write is still in place, between A1 and A2, with C2 already done. C5 then takes effect between A2 and A4.

So C5 must write 5 after A2 and before A4. The order is: C1, C2, A1, C4 (reads 5), A2, C5 (writes 5), A4 (reads 5).

**Final value of z.**

- A2 takes effect before C5, so 3 cannot be the last write. A1 and A2 cannot be last either.
- B2 and B3 cannot take effect between C5 and A4, or A4 would not read 5.
- The final value is 4 if B3 is the last z write, with B2 and B3 both after A4. This is feasible.
- The final value is 5 if C5 is the last z write, with B2 and B3 before it, for example before A1. This is feasible.
- B2 cannot be the last write because B3 always follows it.

BEGIN
4
5
END