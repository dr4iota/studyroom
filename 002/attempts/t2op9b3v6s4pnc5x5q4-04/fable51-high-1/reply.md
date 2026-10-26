**Key observations**

- **Final z and B9**: B8 occurs after R, which is after A9, so B8 is the last write to z and B9 reads it. B8 writes the value B2 read from y. B2 (before Q, before A9) can run either before A8 (reads 0) or between A8 and A9 (reads A8's value).
- **Final y**: Only A8 writes y, and A8 writes what A7 read. Between A6 and A7 no other thread writes z (B1 is before P, B8 is after R), so A7 = A4's value. Hence final y = A4.
- **A4**: Reads z after A1 (6) and B1 (1), which can occur in either order → A4 ∈ {1, 6}.
- **Final x**: Last of A2 (1) vs B7 (4). A2 can precede or follow B7 — but if B2 happened after A8 (so B2 = A4 ≠ 0), then B7 > B2 > A8 > A2, forcing final x = 4.

**Combinations (B9, x, y, z):**

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END