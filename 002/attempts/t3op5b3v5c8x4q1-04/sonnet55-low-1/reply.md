The final value of z can only be 5 or 4.

**How A4 can return 5.** A1 writes 5 and A2 writes 3, and A2 comes before A4. So A4 can return 5 only if another write of 5 to z lands after A2 and before A4. The candidates are:
- B2 writes whatever B1 read from x. That is 0 or 3 before A5 runs. It could be 5 only if A5 had already run, but A5 comes after A4, so B2 cannot supply the 5.
- C5 writes whatever C4 read from z. C4 can read 5 if A1 writes after C2 and C4 reads before A2. C5 then writes 5 after A2 and before A4. One valid order is C2, A1, C4, A2, C5, A4.

So C5 must be the write that makes A4 return 5. It lands before A4.

**What can follow A4.** Thread C has no writes to z left after C5. A5 writes only to x. The only remaining writes to z are from thread B, and B2 always comes before B3.
- If B3 comes after A4, it is the last write to z, so the final value is 4.
- If B2 and B3 both come before C5, which is possible, nothing writes to z after C5. The final value is then 5. For example, run B2 and B3 first, then C2, A1, C4, A2, C5, A4.
- B2 or B3 cannot fall between C5 and A4, because that would change what A4 reads.
- B2 cannot be the last write to z, because B3 always follows it. So 0 and 3 are impossible.

BEGIN
4
5
END