**Reasoning**

- **Final x (Q2):** B7 (write 4) happens after R, and R is after A9, which is after A2 (A's only write to x). So B7 is the last write to x → **x = 4**.
- **Final z (Q4) and B9 (Q1):** B8 (write B2's value) happens after R, which is after A9; all of A's writes to z (A1, A6, A9) and B1 precede it. So B8 is the last write to z, and B9 (after B8 in the same thread) reads it → **z = B9 = value read by B2**.
- **A4:** reads z after P (so after B1 wrote 1) and after A1 wrote 6. A1 (before S) and B1 (before P) are unordered relative to each other, so A4 ∈ {1, 6}. A6 writes A4's value, A7 reads it back (B8 can't intervene), so A8 writes A4's value to y.
- **Final y (Q3):** A8 is the only write to y → **y = A4 ∈ {1, 6}**.
- **B2:** reads y before Q. A8 is not constrained relative to Q, so B2 may occur before A8 (returns 0) or after A8 (returns A4's value). Both are consistent with the sync points (e.g., A8 < B2 < Q < A9 < R).

So B9 = z ∈ {0, A4}, x = 4, y = A4.

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
END