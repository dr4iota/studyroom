**Key deductions**

- z before A4: only A1 (6) and B1 (1) can precede A4 (B8 comes after R, which is after A9, after A4), so A4 returns v ∈ {1, 6}. A6, A7, A9 just propagate v, so A7 = v, A8 writes v to y, A9 writes v to z.
- Final y = v (A8 is the only write to y).
- B2 reads y before Q; A8 is also before Q, so B2 returns 0 (before A8) or v (after A8). B8 writes that to z after R, i.e. after every A write to z, so B9 = final z = B2's value ∈ {0, v}.
- Final x: B7 (4) is last of B's x writes; A2 (1) is only constrained to follow A1 and precede A3, so it can land after B7. Final x ∈ {1, 4}, independent of the rest.

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