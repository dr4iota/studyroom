**Analysis**

- **x**: Written by A2 (1), B5 (3), B6 (B3's value), B7 (4). B7 is the last of B's writes; A2 can fall before or after B7 (A2 isn't tied to S or P). Final x ∈ {1, 4}.
- **z at A4**: A4 runs after P (so after B1) and after A1, so z is 1 or 6 depending on A1/B1 order. A6 re-writes that same value, so A7 reads it too, and A8 writes it to y. Final y = A4 ∈ {1, 6}.
- **B2**: reads y before Q, and A9 is after Q; A8 can be either side of B2, so B2 ∈ {0, A4}.
- **B8** writes B2's value to z after R (after A9, the last A-write to z), and B9 reads it with nothing in between. So B9 = final z = B2 ∈ {0, final y}.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 1 1 1
1 4 1 1
6 1 6 6
6 4 6 6
END