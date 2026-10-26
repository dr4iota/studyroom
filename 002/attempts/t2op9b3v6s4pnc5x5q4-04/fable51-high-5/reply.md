**Analysis**

- **z and A4:** Both A1 (z=6) and B1 (z=1) take effect before A4 (B1 < P < A2 < A4; A1 < A4 by thread order), and nothing else writes z before A4 (B8 comes after A9). A1 and B1 are unordered, so A4 ∈ {1, 6}.
- **A7, A8, A9:** A6 writes A4's value to z; nothing can intervene before A7, so A7 = A4, A8 writes A4's value to y, A9 writes A4's value to z.
- **Final y:** A8 is the only write to y, so final y = value of A4.
- **B2:** reads y; it must finish before Q, but A8 is not constrained to be after Q (only A9 is), so B2 can be before or after A8 → B2 ∈ {0, A4}.
- **B8/B9/final z:** B8 (after R) comes after A9 (before R), so B8 is the last write to z; B9 reads it → B9 = final z = B2's value.
- **Final x:** last write is B7 (4) unless A2 (x=1) lands after B7. A2 only needs to be after P and before A9 (< R < B8), so it can come after B7 → final x ∈ {1, 4}.

All eight combinations are independently achievable.

BEGIN
0 1 1 0
0 4 1 0
1 1 1 1
1 4 1 1
0 1 6 0
0 4 6 0
6 1 6 6
6 4 6 6
END