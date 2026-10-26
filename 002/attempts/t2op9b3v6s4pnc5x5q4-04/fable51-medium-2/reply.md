**Analysis**

- Final **z** and **B9**: B8 (write B2's value to z) comes after everything in thread A (A9 < R < B8), so B9 = final z = value read by B2.
- **A4** reads z after both A1 (z=6) and B1 (z=1) have taken effect (B1 < P < A3 < A4), in either order, so A4 ∈ {1, 6}. A6 writes that value back to z, A7 reads it (nothing else can touch z in between), and A8 writes it to y. So final **y** = A4's value ∈ {1, 6}.
- **B2** reads y either before A8 (returning 0) or after A8 (returning A4's value); both are allowed since B2 only needs to precede Q, which precedes A9.
- Final **x**: last write is either B7 (4) or A2 (1). A2 can come after B7 (A1 < S < B5–B7 < A2 < A3…A9 < R < B8), or before it. So x ∈ {1, 4}.

These choices are independent.

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