**Analysis**

Ordering constraints from sync points:
- B1 < P < A3…A9
- A1 < S < B5…B9
- B2 < Q < A9
- A1…A9 < R < B8, B9

**z and A4/A7:** Both A1 (6) and B1 (1) take effect before A4, in either order, so A4 ∈ {1, 6}. A6 writes A4's value to z, and nothing else (B8 is after R) can intervene before A7, so A7 = A4. Hence A8 writes A4 to y → **final y = A4 ∈ {1, 6}**.

**Final z / B9:** The last write to z is B8 (after R, after all of A's writes), which writes B2's value; B9 then reads that same value. So **Q1 = Q4 = B2**. B2 reads y, written only by A8, and A8 can be either before or after B2, so B2 ∈ {0, A4}.

**Final x:** B7 (4) is the last of B's writes; A2 (1) can land before or after B7, so final x ∈ {1, 4}. But if A2 is after B7, then B2 < B7 < A2 < A8, forcing B2 = 0. So x = 1 is only possible together with Q1 = Q4 = 0.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END