C3 is always 0, and the final z can be 0, 1 or 5.

**Final z.** The only write to z is B5, which writes whatever B4 read from y. So the final z equals the value B4 read.

**Values B4 can read.** B4 runs after B3 (which wrote 1 to y). The other writes to y are B1 (2), C1 (1) and A4 (the value A1 read).
- B1 runs before B3, so B4 cannot read 2.
- A1 reads x, which holds 0 before B2 and 5 after it. A4 writes that value, so B4 can read 1, 0 or 5.

**Constraints from the known results.**
- A3 reads 5, so B2 takes effect before A3.
- A2 returns 0, so A2 reads z before B5 writes a nonzero value.
- A4 runs after A3.
- A1 runs before A2, so A1 is also before A3.

**Each final z is achievable.**
- z = 1: B4 reads B3's write or C1's write of 1.
- z = 0: A1 reads 0 before B2. One valid order is A1, A2, B1, B2, A3, B3, A4 (writes 0), B4 (reads 0), B5.
- z = 5: A1 reads 5 after B2. A4 then writes 5 after B3 and before B4, so B4 reads 5.

**C3.** C4 returned 0 and runs after C3. If B5 writes a nonzero value, C4 must come before B5, so C3 does too and reads 0. If B5 writes 0, z is 0 throughout. Either way C3 = 0.

BEGIN
0 0
0 1
0 5
END