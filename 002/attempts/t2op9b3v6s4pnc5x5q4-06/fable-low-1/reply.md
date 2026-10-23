**Key deductions**

- A4 and B1 both read y before any write to y takes effect (B4/B7 come later), so A4 = B1 = 0. Hence A6, B3 write 0 to z; A8 writes 0 to x; B4 writes 0 to y.
- A9 happens after A8 and after Q (so after B2), but before P (so before B9). It returns 4 if B2 took effect after A8, else 0.
- B5 reads either 4 (B2, before A8) or 0 (after A8); B9 copies B5, and B9 is the last write to x, so final x = B5.
- If A9 = 4 then B2 is after A8, forcing B5 = B8 = 4 and x = 4; also A6 < A8 < B2 < B6 forces z = 1.
- If A9 = 0 (A8 after B2): B5 = 4 allows B8 ∈ {4, 0} and z ∈ {0, 1} (A6 can land after B6 or before); B5 = 0 forces B8 = 0, x = 0, and since B6 is then after A8 > A6, z = 1.

BEGIN
4 4 4 1
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
0 0 0 1
END