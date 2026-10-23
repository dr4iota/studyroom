**Key orderings from sync points:** B1 → A3.. (via P), A1 → B5.. (via S), B2 → A9 (via Q), A9 → B8 (via R).

- **A4** reads z after B1; only A1(6)/B1(1) precede it, in either order → A4 ∈ {1, 6}. A6/A7/A8 propagate it: A7 = A4, A8 writes A4 to y.
- **Final y** = A4 (A8 is the only y write).
- **B2** reads y before Q; it can be before or after A8 → B2 ∈ {0, A4}.
- **B8** (value B2) is the last z write (after A9, which is after A6), and B9 reads after it → B9 = final z = B2.
- **Final x**: B7(4) is last among B's; A2(1) may land after B7 → final x ∈ {1, 4}. But if A2 is after B7, then B2 (before B7) is before A8, forcing B2 = 0.

BEGIN
0 1 1 0
0 4 1 0
1 4 1 1
0 1 6 0
0 4 6 0
6 4 6 6
END