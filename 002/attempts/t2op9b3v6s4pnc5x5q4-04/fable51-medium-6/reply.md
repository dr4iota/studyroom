**Key constraints**

- Final x: B7 (write 4) is after R, R is after A9, which is after A2 (write 1). So B7 is the last write to x → **x = 4**.
- Final z and B9: B8 (writes B2's value) is after R > A9 > A6, and after A1/B1 (which precede A2 < A9). So B8 is the last write to z, and B9 reads after it → **z = B9 = value of B2**.
- A4 reads z after both A1(6) and B1(1) have taken effect (B1 < P < A2 < A4; A1 < A2 < A4), in either order → A4 ∈ {1, 6}.
- A7 reads z after A6 (which wrote A4's value); no other z write can land between A6 and A7 → A7 = A4, so **y = A4**.
- B2 reads y before Q; A8 (the only write to y) is unordered w.r.t. B2 → B2 ∈ {0, A4}.

Combining: (B9, x, y, z) = (B2, 4, A4, B2).

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
END