Notation: v is the value A2 returns (y is read, then A3 writes v to z and A6 writes v to x).

**Ordering constraints**
- B4 ends before P and before Q. A2 starts after Q, so B4 comes before A2.
- B1 comes before R, so B1 also comes before A2.
- B2 ends before R, and R comes before A2 starts. B5 comes after B4 and B4 comes after B2. A's writes to x all come after A2, so nothing has written x when B2 reads it. B2 therefore returns 0, and B9 later writes 0 to y.
- The writes to y are B1 (6), B8 (6) and B9 (0), in that order. A2 reads 6 or 0, so v is 0 or 6. The value 0 is possible only if B5 through B9 all come before A2, which the constraints allow.

**Final z**
- B4 writes 3 before A3 does. A3 writes v after that, and no other write to z follows. So the final z equals v.

**A8 and the final x**
- A6 writes v to x before A7, and A7 comes before A8.
- B5 writes 4 to x and must end before S. A8 starts after S.
- If B5 comes before A6, then A6 is the last write to x. A8 returns v and the final x is v.
- If B5 comes after A6, then A8 returns 4 and the final x is 4. B5 would then be after A2, so B8 and B9 are too. The y that A2 read still holds 6, so v = 6.

**A9**
- If v = 0, B9 came before A2, so y stays 0 and A9 returns 0.
- If v = 6, A9 returns 6 if it reads before B9, or 0 if B9 has already written.

**Combinations (A8, A9, final x, final z)**
- v = 0: (0, 0, 0, 0)
- v = 6, B5 before A6: (6, 6, 6, 6) and (6, 0, 6, 6)
- v = 6, B5 after A6: (4, 6, 4, 6) and (4, 0, 4, 6)

BEGIN
0 0 0 0
6 6 6 6
6 0 6 6
4 6 4 6
4 0 4 6
END