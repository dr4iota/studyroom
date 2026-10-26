Reasoning:

- B1 to B7 all end before S, and A1 starts after S. So every one of B1 to B7 happens before every operation of A.
- B2 reads z before B7 and A1 write it, so B2 = 0. B3 and B8 therefore both write 0 to y.
- A1 writes 6 to z after B7 wrote 1, and nothing writes z afterwards. So A8 = 6.
- A3 reads y after A2 wrote 6. The only other write that can fall between A2 and A3 is B8 (0), because B3 to B5 finish before A1. So A3 is 6 or 0.
- A4 reads y the same way. It is 0 if B8 lands after A2 and before A4, and 6 otherwise. A5 copies that value into x.
- B9 comes after B8. It reads 5 if it precedes A5, or A5's value (6 or 0) if it follows.
- B9 = 6 needs A4 = 6, so B8 is not between A2 and A4. Since A3 is after A2 and before A4, A3 cannot be 0 in that case. So (A3, B9) = (0, 6) is impossible.
- All other combinations are achievable.

BEGIN
6 6 5
6 6 6
6 6 0
0 6 5
0 6 0
END