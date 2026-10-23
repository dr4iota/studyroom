Working through the constraints:

- **z at A4:** B1 (write 1) is before P, and A4 is after P; A1 (write 6) is before S but unordered with B1. So A4 returns v ∈ {1, 6}. A6 rewrites v, A7 reads v, A8 writes v to y, A9 writes v to z.
- **y:** the only write to y is A8 (value v), so final y = v. B2 reads y before Q; A8 may be before or after B2, so B2 returns 0 or v.
- **z after R:** B8 (after R) writes B2's value, after A9 (before R). B9 then reads that. So B9 = final z = B2's value ∈ {0, v}.
- **x:** A2 precedes A9 which precedes R, and B7 (write 4) is after R, so final x = 4.

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
END