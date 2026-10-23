**Key deduction: x always holds 0.** The only writes to x are A3 and A6, and both come after A1 in thread A. So A1 reads 0, A3 and A6 write 0, and x stays 0. This agrees with B1 returning 0.

**Constraint from A2 returning 2.** Thread A does not write y before A2. So A2 must come after B4 (which writes 2). If B7 comes before A2, B7 must also write 2. After B4, y = 2, and the rest is an interleaving of two sequences:
- **Thread A:** A4 writes 3 → A5 writes 0 → A7 reads y.
- **Thread B:** B5 reads v → B6 reads y → B7 writes v.

A7 always comes after A5. So A7 returns 0, unless B7 takes effect between A5 and A7, in which case it returns v. The final y is v if B7 is the last write, and 0 if A5 is the last write.

**Case v = 2 (B5 before A4):**
- B6 before A4 (B6 = 2):
  - B7 before A5 gives (0, 2, 0).
  - B7 between A5 and A7 gives (2, 2, 2).
  - B7 after A7 gives (0, 2, 2).
- B6 between A4 and A5 (B6 = 3):
  - B7 before A5 gives (0, 3, 0).
  - B7 between A5 and A7 gives (2, 3, 2).
  - B7 after A7 gives (0, 3, 2).
- B6 after A5 (B6 = 0):
  - B7 before A7 gives (2, 0, 2).
  - B7 after A7 gives (0, 0, 2).

**Case v = 3 (B5 between A4 and A5):**
- B6 = 3:
  - B7 before A5 gives (0, 3, 0).
  - B7 between A5 and A7 gives (3, 3, 3).
  - B7 after A7 gives (0, 3, 3).
- B6 = 0:
  - B7 before A7 gives (3, 0, 3).
  - B7 after A7 gives (0, 0, 3).

**Case v = 0 (B5 after A5):** B6 reads 0 and B7 writes 0, which gives (0, 0, 0).

BEGIN
0 2 0
2 2 2
0 2 2
0 3 0
2 3 2
0 3 2
2 0 2
0 0 2
3 3 3
0 3 3
3 0 3
0 0 3
0 0 0
END