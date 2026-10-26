Each value read and each final value is fixed by the order in which the writes to `y` take effect.

**Timing constraints from the sync points**
- All of A1–A5 happen before P. A5 also happens after Q.
- B1–B4 happen before Q.
- B5 starts after B4 and before P, and ends after P. So B5 can take effect either before P or after P.

**Final value of y (Q3)**
- A4 (writes 2) always comes after A2, so the last write to `y` is either A4 or B5.
- So the final value of `y` is 2 (A4 last) or 1 (B5 last).
- If B3 returned 2, then A4 took effect before B3. That puts A4 before B4 and B5, so the final value must be 1.
- In every other case, A4 can take effect after B5, because B5 may take effect before P. In those cases both 1 and 2 are possible.

**Value returned by B3 (Q2)**
- B3 comes after B2, so it returns the last write to `y` before it: B2 (3), A2 (the value A1 read), or A4 (2).
- B3 cannot return the value written by B5, because B5 comes after B3.

**Value returned by A1 (Q1)**
- **A1 before B1:** A1 returns 0. B3 returns 3, 0 (if A2 falls between B2 and B3), or 2.
- **A1 between B1 and B2:** A1 returns 1. B3 returns 3, 1 (via A2), or 2.
- **A1 after B2:** A1 returns 3. B3 returns 3 or 2.
- **A1 after B4 or B5:** A1 runs after B3, so B3 must have returned 3. A1 then returns 3 or 1, both already covered above.

BEGIN
0 3 1
0 3 2
0 0 1
0 0 2
0 2 1
1 3 1
1 3 2
1 1 1
1 1 2
1 2 1
3 3 1
3 3 2
3 2 1
END