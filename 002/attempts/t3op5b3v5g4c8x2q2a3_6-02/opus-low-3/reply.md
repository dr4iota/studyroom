**Facts that follow from the rules**
- Only B1 writes x, and it writes 3. C1 returned 0, so C1 takes effect before B1. C2 returned 3, so C2 takes effect after B1.
- B3 comes after B1 in thread B, so B3 reads 3. Therefore B4 writes 3 to y.
- y is written only by B4 (value 3) and C5 (value 4). So A2 returns 0, 3 or 4.
- z is written by A1 (value 1), B2 (value 1) and A4 (the value A2 returned).

**Q1: what C3 can return**
- **0:** C3 takes effect after C2, but A1 and B2 can both take effect after C3. Then no write to z precedes C3, so it reads 0.
- **1:** A1 or B2 takes effect before C3, and A4 does not come between that write and C3.
- **A4's value:** this needs A4, and therefore A2, to take effect before C3.
  - C5 comes after C3 in thread C, so A2 cannot see C5's 4.
  - A2 cannot return 0 here, because A4 would then write 0. That outcome is already counted as "C3 returns 0".
  - A2 can return 3 if B4 takes effect before A2.
  - This forces the order B4 < A2 < A4 < C3 < C5. It agrees with A3 reading 3, since B1 took effect earlier. C3 returns 3.
- **4:** impossible, because that would need C5 before C3.

So C3 returns 0, 1 or 3.

**Q2: the final value of y**
- When C3 returns 0 or 1, B4 and C5 can take effect in either order. The final y is 3 or 4.
- When C3 returns 3, the order above puts C5 after B4. The final y is 4.

BEGIN
0 3
0 4
1 3
1 4
3 4
END