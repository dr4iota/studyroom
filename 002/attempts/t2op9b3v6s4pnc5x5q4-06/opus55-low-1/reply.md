**Fixed values**

1. **A4 returns 0.** A4 comes before S. B1 comes after S. B4 and B7 come after B1. So no write to y can take effect before A4.
2. **B1 returns 0** for the same reason: the only writes to y (B4 and B7) come after B1.
3. Therefore A6 writes 0 to z, A8 writes 0 to x, B3 writes 0 to z, and B4 writes 0 to y.

**Ordering constraints from the sync points**

- A5 < S < B1, and B1 < R < A8.
- B4 < Q < A9, and A9 < P < B9.
- A1–A3 come before B2, so B2's write of 4 replaces A3's 2.
- B9 is the last write to x, because A8 < A9 < B9 and B2 < B9. So the final x equals the value B5 returned.

**Case 1: B2 takes effect before A8**

- A9 comes after A8 and before B9, so it reads 0.
- If B5 comes after A8, then B5 = 0 and B8 = 0. This gives final x = 0.
  - Here A6 < A8 < B5 < B6, so B6 writes z last and final z = 1.
- If B5 comes before A8, then B5 = 4 and final x = 4. B8 reads either 4 (before A8) or 0 (after A8).
  - A6 can take effect after B6, so final z can be 0 or 1.

**Case 2: A8 takes effect before B2**

- After B2, x stays 4 until B9.
- B5 and B8 both come after B2, so both read 4, and final x = 4.
- A9 comes after B4, which comes after B2, so A9 reads 4.
- A6 < A8 < B2 < … < B6, so final z = 1.

BEGIN
0 0 0 1
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
4 4 4 1
END