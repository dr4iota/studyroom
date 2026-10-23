**Key constraints**

- B1 (z=1) happens before P, hence before A3–A9; A1 (z=6) is before A2 which is before A4. So A4 reads z ∈ {1, 6}.
- A6 writes A4's value to z; nothing else can write z before A7 (B8 is after R, after A9), so A7 = A4, and A8 writes y = A4 ∈ {1, 6}. y's only writer is A8, so **final y ∈ {1, 6}**.
- B2 reads y before Q (before A9), but A8 may or may not have already happened: B2 ∈ {0, A8's value}.
- B8 (after R, after A9) is the last write to z, writing B2's value; B9 reads after it. So **B9 = final z = B2's value**.
- x: B7 writes 4 after S (after A1), but A2 (x=1) is unconstrained relative to B7 (only A1 < A2 < A3). So **final x ∈ {1, 4}**, independent of the rest.

Combining: either B2 = 0 (z = B9 = 0, y = 1 or 6), or B2 = y (z = B9 = y).

BEGIN
0 1 1 0
0 4 1 0
0 1 6 0
0 4 6 0
1 1 1 1
1 4 1 1
6 1 6 6
6 4 6 6
END