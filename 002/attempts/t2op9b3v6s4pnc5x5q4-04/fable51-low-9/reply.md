**Key deductions**

- **z / B9:** B8 (after R) is the last write to z, since A9 is before R. So final z = value of B2, and B9 returns the same. Q1 = Q4 = B2.
- **y:** only A8 writes y, with A7's value. B1 (before P) precedes A4 (after P), so A4 reads 1, or 6 if A1 already happened. A7 reads 1 or 6 (6 if A1 lands between A6 and A7, or A4 was already 6). Final y ∈ {1, 6}.
- **B2:** reads 0, or A7's value if A8 precedes it (both before Q, either order allowed). B2 ∈ {0, y}.
- **x:** B7 (4) is last among B's writes, but A2 (after P) can come after B7 (B7 is before R, A2 only needs to precede A3…A9 and Q). Final x ∈ {1, 4}. If x = 1, then A1 < S < B7 < A2 < A4, so A4 = A7 = 6, y = 6, B2 ∈ {0, 6}.

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
0 1 6 0
6 1 6 6
END