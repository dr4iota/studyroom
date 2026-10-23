**Key facts:**

- **Final z = B9 = val(B2).** B8 writes val(B2), and it is the last z-write because A9 < R < B8.
- **Final y = val(A4) = v.** A8 is the only y-write and writes val(A7), which equals v. A4 reads z after B1 (since B1 < P < A3 < A4), so v is 1 if A1 < B1 and 6 if B1 < A1.
- **B2 ∈ {0, v}.** B2 reads y, so it sees 0 if B2 < A8 and v if A8 < B2.
- **Final x ∈ {1, 4}.** B7 writes 4 after B5 and B6, so only A2 (writes 1) can override it. Final x is 1 if B7 < A2 and 4 if A2 < B7.

**Constraints between the choices:**

- If B2 comes after A8, then B7 (later in thread B) comes after A2, so final x is forced to 4. This rules out (B2 = v, x = 1).
- If B2 < A8, all four combinations of v and x are feasible. For example, for v = 1, x = 1: A1, S, B1, B2, B3–B7, A2, P, A3–A9, R, B8, B9 gives B9 = 0, x = 1, y = 1, z = 0.

**Feasible outcomes (B9, final x, final y, final z):**

| B2 | v | x | Outcome |
|---|---|---|---|
| 0 | 1 | 1 | 0 1 1 0 |
| 0 | 1 | 4 | 0 4 1 0 |
| 0 | 6 | 1 | 0 1 6 0 |
| 0 | 6 | 4 | 0 4 6 0 |
| v = 1 | 1 | 4 | 1 4 1 1 |
| v = 6 | 6 | 4 | 6 4 6 6 |

Q1 and Q4 always match, since both equal val(B2).

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END