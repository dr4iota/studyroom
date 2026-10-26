Each operation takes effect at a single instant, so every outcome comes from some interleaving of the two threads' operations. A1 returns v, and A4 later writes that same v to x.

**v = 0 (A1 runs before B1):** A4 writes 0 to x, and it can land anywhere after A1.
- A3 can return 0 (before B1, or after A4 while x is still 0), 1 (between B1 and B2), or 3 (after B2).
- If A4 lands before B3, B3 and B4 both return 0 (A4 after B2) or both return 3 (A4 before B2).
- If A4 lands between B3 and B4, then B3 = 3 and B4 = 0.
- If A4 lands after B4, then B3 = 3 and B4 = 3.
- So (B3, B4) ∈ {(3,3), (0,0), (3,0)}, and each is compatible with any A3 ∈ {0, 1, 3}.

**v = 1 (A1 runs between B1 and B2):** A4 writes 1 to x.
- A3 can only return 1 or 3, never 0.
- If A4 lands before B2, B3 and B4 both return 3.
- If A4 lands after B2 and before B3, then B3 = 1 and B4 = 1.
- If A4 lands between B3 and B4, then B3 = 3 and B4 = 1.
- If A4 lands after B4, B3 and B4 both return 3.
- So (B3, B4) ∈ {(3,3), (1,1), (3,1)}, with A3 ∈ {1, 3}.

**v = 3 (A1 runs after B2):** A4 writes 3, which changes nothing. So A3 = 3, B3 = 3 and B4 = 3.

Combining the cases gives the list below, in the order A3, B3, B4.

BEGIN
0 3 3
0 0 0
0 3 0
1 3 3
1 0 0
1 3 0
1 1 1
1 3 1
3 3 3
3 0 0
3 3 0
3 1 1
3 3 1
END