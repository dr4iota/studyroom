Four values are asked, so each combination is written as (Q1 Q2 Q3 Q4).

**Key facts from the constraints:**

- **B2 always reads 0.** B2 is before R, and the first write from A to x (A4) comes after P, which is after B4, which is after B2. So B9 writes 0 to y.
- **y is 6 or 0 at A2.** B1 (y=6) is before R, which is before A2, so y is never still 0 when A2 reads it. A2 reads 0 only if B9 has already run. So A2 returns v ∈ {0, 6}, and Q4 (final z) = v, because A3 comes after P, which is after B4.
- **A8 and final x.** Thread A's writes to x (A4, A5, A6) finish before A8. Only B5 (x=4) can land after A6, and it must come before S, which precedes A8. So A8 and the final x are either both v (if B5 is before A6) or both 4 (if B5 is between A6 and A8). Q1 = Q3 always.
- **A9 reads 0 or 6.** It reads 0 exactly when B9 is before A9. B9 comes after B5, so if B9 is before A2 then B5 is before A6, which rules out the case v=0 with B5 after A6.

**Cases:**

1. B9 before A2: v=0, A9 reads 0, and B5 must precede A6 → (0, 0, 0, 0).
2. A2 before B9, B9 before A9: v=6, A9 reads 0. B5 before A6 → (6, 0, 6, 6); B5 after A6 → (4, 0, 4, 6).
3. B9 after A9: v=6, A9 reads 6. B5 before A6 → (6, 6, 6, 6); B5 after A6 → (4, 6, 4, 6).

Each case has a concrete timeline that satisfies all sync constraints.

BEGIN
0 0 0 0
4 0 4 6
6 0 6 6
4 6 4 6
6 6 6 6
END