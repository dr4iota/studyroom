C3 is always 0, and the final z can be 0, 1 or 5.

**Q1 (C3).** The only write to z is B5, so z holds 0 until B5 takes effect and a single value afterward. C4 reads z after C3 and returned 0, so B5 had not yet taken effect when C4 read. C3 comes before C4, so it also sees 0.

**Q2 (final z).** B5 is the only write to z, so the final z is whatever B4 read. B4 comes after B3, which writes 1 to y. It can read:

- **1:** B3's write, or C1's write, which is also 1. Nothing else needs to intervene.
- **0:** this needs A1 to have read x before B2, so A1 returned 0. A4 then writes 0 to y after B3 and before B4. A3 returned 5, so B2 precedes A3 and hence A4. The order A1, B1, B2, A2, A3, B3, A4, B4, B5 satisfies every constraint.
- **5:** this needs A1 to have read x after B2, so A1 returned 5. A4 then writes 5 to y after B3 and before B4.
- **2:** this is impossible, because B3 overwrites B1's 2 before B4 runs, and no other thread writes 2.

A2 must read z before B5 takes effect. That is consistent with all of these cases, because B5 can be delayed until after A2 and C4.

BEGIN
0 0
0 1
0 5
END