**Ordering constraints from the sync points**
- B1 < P < A3 (and everything after A3 in thread A).
- B2 < Q < A9 < R < B8, B9. So all of thread A finishes before B8.
- A1 < S < B5, B6, B7.

**Value of y**
- Only A8 writes y. It writes A7's value.
- A6 writes A4's value to z. Before A7, no other write to z can take effect between A6 and A7:
  - B1 is before P, and A1 comes earlier in thread A.
  - B8 is after R.
- So A7 = A4 = v.
- A4 reads z after both A1 (6) and B1 (1). Either of these two writes can be the later one, so v ∈ {1, 6}.
- Final y = v.

**B2, B9 and final z**
- B2 reads y, so it returns 0 or v. It returns v only if A8 takes effect before B2.
- B8 writes B2's value to z after all of thread A is done. Nothing writes z after that, so B9 = final z = B2's value.

**Final x**
- B7 (writes 4) can be the last write to x. That gives x = 4.
- A2 (writes 1) has no constraint against B7, so it can come after B7. That gives x = 1.
- If A2 is after B7, then B2 < B7 < A2 < A8. So B2 reads 0 in that case.
- Therefore x = 1 forces B9 = 0.

**Combinations (B9, x, y, z)**
- With B9 = 0: x ∈ {4, 1} and y ∈ {1, 6}, with z = 0.
- With B9 = v: x = 4, y = v, z = v.

BEGIN
0 4 1 0
0 4 6 0
0 1 1 0
0 1 6 0
1 4 1 1
6 4 6 6
END