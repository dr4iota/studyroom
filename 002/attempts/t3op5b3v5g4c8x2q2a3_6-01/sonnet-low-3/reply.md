C3 must return 0, and the final value of z can be 0, 1 or 5.

**C3.** The only write to z in the whole problem is B5, so z is 0 until B5 takes effect. C4 reads z after C3 and is known to return 0. If C3 had returned a nonzero value, B5 would already have written it. z would then stay at that value, and C4 could not return 0. If B5 writes 0, C3 still returns 0. So C3 is always 0.

**Final z.** B5 always runs, so the final z is the value B4 read from y. The writes to y are B1 (2), C1 (1), B3 (1), and A4 (the value A1 read from x).

- B4 cannot read 2, because B3 takes effect after B1 and B4 runs after B3. Any later write to y is 1, 0 or 5, never 2.
- A3 returned 5, so B2 took effect before A3. A1 is before A3, so A1 reads either 0 (before B2) or 5 (after B2). So A4 writes 0 or 5.
- **z = 1:** B4 reads y right after B3 or C1 wrote 1, with no later overwrite.
- **z = 0:** A1 reads 0 before B2. Then A3 reads 5, and the order is B3, A4 (writes 0), B4. B4 reads 0.
- **z = 5:** A1 reads 5 after B2. Then A3 reads 5, and the order is B3, A4 (writes 5), B4. B4 reads 5.
- A2 reading 0 and C4 reading 0 are both satisfied by placing them before B5.

BEGIN
0 0
0 1
0 5
END