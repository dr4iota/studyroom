The possible combinations are (B2, C3, final z): 0 0 1, 0 0 5, 0 2 1, 2 0 1 and 2 0 5. There are no sync points, so any interleaving that respects each thread's order is allowed.

**Constraint from A5.** A3 writes 2 to x, and later A5 reads x and gets 0. So some write of 0 to x must take effect after A3 and before A5, and it must be the last write to x before A5. The only other writes to x are B4 (the value B2 read) and C5 (the value C3 read).

**Possible reads of x.** x only ever holds 0 or 2, so B2 and C3 each return 0 or 2.
- If B2 = C3 = 2, then B4 and C5 both write 2. No write of 0 can follow A3, so this case is impossible.
- (0,0) works. For example, C3 and C5 come after A3, with C3 reading 2 and C5 writing 2, then B4 writes 0 before A5.
- (2,0) works. B2 reads 2 after A3 and B4 writes 2, then C5 writes 0 (C3 read 0 before A3) before A5.

**Final z.** The writes to z are A4 (1), B1 (5), C1 (4) and C2 (1). C2 always follows C1, so 4 can never be final. The final value is 1 or 5.
- z = 1 is reachable for every allowed pair by making A4 the last write to z.
- z = 5 needs B1 to be the last write to z, after A4. Then B2 also comes after A3.
  - For (0,0): run C1, C2, C3 (reads 0) before A1; then A1–A4; then C4, C5 (writes 0); then B1, B2 (reads 0), B3, B4 (writes 0); then A5 reads 0. This works.
  - For (0,2): B2 after A3 needs a 0 already written, but C5 writes 2 and B4 comes after B2. This is impossible.
  - For (2,0): run C1, C2, C3 (reads 0); then A1–A4; then B1, B2 (reads 2), B3, B4 (writes 2); then C4, C5 (writes 0); then A5 reads 0. This works.

BEGIN
0 0 1
0 0 5
0 2 1
2 0 1
2 0 5
END