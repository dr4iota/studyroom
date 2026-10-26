**Key observations**

- Thread A's last write to z (A9) finishes before R, and B8 (write B2's value to z) starts after R. So the final z = B9 = the value B2 read.
- B2 reads y, which is only written by A8. B2 must end before Q, A9 starts after Q, but A8 is unconstrained relative to B2, so B2 returns either 0 or A8's value.
- A4 reads z after both A1 (6) and B1 (1) took effect (B1 before P before A2 before A4; A1 is A's first op). Their mutual order is free, so A4 ∈ {1, 6}. A6 writes A4's value to z, A7 reads it back (no other z write can intervene), and A8 writes it to y. So final y = A4 ∈ {1, 6}.
- Final x: A2 (write 1) and B7 (write 4) are not ordered relative to each other (P can be placed after B7). So final x ∈ {1, 4}. But if B2 saw A8's value, then B7 comes after A2, forcing x = 4.

**Cases**

- B2 = 0: z = 0, B9 = 0, x ∈ {1,4}, y ∈ {1,6}.
- B2 = A4: z = y = A4, B9 = A4, x = 4.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END