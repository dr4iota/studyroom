**Key deductions**

- **B2** reads y before Q; the only write to y (A8) is after Q → B2 = 0.
- **B8** writes B2's value (0) to z after R; every other z‑write (A1, B1, A6, A9) is before R → final z = 0 and **B9 = 0**.
- **A4** reads z after both A1 (6) and B1 (1) have taken effect (B1 < P < A2 < A4), and no other z‑write can precede it → A4 ∈ {6, 1} depending on A1/B1 order. A6 writes A4 back to z, so **A7 = A4**, and A8 makes **final y = A4 ∈ {6, 1}**.
- Final x: A2 (1) and B7 (4) are unordered (both only need to precede R), so **final x ∈ {4, 1}**; this is independent of the A1/B1 ordering.

BEGIN
0 4 6 0
0 4 1 0
0 1 6 0
0 1 1 0
END