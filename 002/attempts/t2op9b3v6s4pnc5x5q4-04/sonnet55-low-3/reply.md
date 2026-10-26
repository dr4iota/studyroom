Working through the constraints:

- **B2 and y:** B2 ends before Q, and A8 (the only write to y) starts after Q. So B2 reads 0.
- **B8 and B9:** B8 starts after R, and A9 ends before R, so every write by A is done before B8. B8 writes B2's value, 0, to z. After that, the only possible writer to z would be B, and B has no more z writes. So B9 reads 0 and the final z is 0.
- **Final x:** x is written by A2 (value 1) and by B5, B6, B7 (B7 writes 4). B6 writes B3's value, and B3 reads before B5. B7 is not ordered against A2, so either write can come last. The final x is 4 if B7 is last, or 1 if A2 comes after B7. Both orders are allowed.
- **Final y:** A8 writes A7's value. A7 reads z after A6 wrote A4's value, and the only other z writes (B1, A1) are earlier and B8 is later, so A7 equals A4.
  - A4 reads z after B1 (B1 is before P, A2 is after P) and after A1. It sees 6 if A1 is the later of the two writes, or 1 if B1 is later.
  - Both orders are allowed, so the final y is 6 or 1.

The two choices for x and the two for y are independent, giving four combinations.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
END