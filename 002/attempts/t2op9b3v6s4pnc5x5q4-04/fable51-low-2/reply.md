**Key dependencies**

- Sync constraints: B1 < P < A2…A9; A1 < S < B5…B9; A9 < R < B8,B9; B2 < Q < A9.
- **A4 (read z):** both A1 (6) and B1 (1) are before A4 (B1 precedes P which precedes A2), and no other z-write can intervene, so A4 ∈ {1, 6} depending on A1/B1 order. Call it v.
- **A7 = v**, since A6 writes v to z and B8 (the only other later z-write) comes after all of A. So A8 writes v to y → **final y = v** (only write to y).
- **A9** writes v to z, then **B8** (after R, hence after all A) writes B2's value to z last → **final z = B2**, and **B9 = B2**.
- **B2 (read y):** B2 is not ordered relative to A8, so B2 ∈ {0, v}.
- **Final x:** B7 writes 4 after B5/B6; A2 writes 1. A2 is only required after P and A1, while B7 only after S — so A2 may come before or after B7. Final x ∈ {1, 4}.

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