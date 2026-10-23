The possible outcomes are 0 0 0 0, 6 0 6 6, 6 6 6 6, 4 0 4 6, and 4 6 4 6.

**Key constraints**
- B2 is followed by B5 in thread B, so B2 always reads 0. That makes the value written by A6 (`a2`) equal to the value read by A2, which is 0 or 6.
- A2 comes after Q and R, so the only writes to y that can precede it are B1 (6), B8 (6), and B9 (0). A2 reads 0 only if B9 precedes A2, which forces B5 before A2.
- Z is written by B4 (3, before P) and A3 (`a2`, after P), so the final z is always `a2`.
- The writes to x are A4 (1), A5 (6), A6 (`a2`), and B5 (4). A6 is the last of A's writes, and every x-write precedes A8, so the final x always equals the value A8 reads.
- Final x is 4 only if B5 comes after A6, which forces B5 after A2 and so `a2` = 6. Otherwise final x = `a2`.
- A9 reads 0 if B9 precedes it and 6 otherwise, since B1 and B8 both write 6.

**Cases**
- `a2` = 0: B9 precedes A2, so B9 precedes A9 and A9 reads 0. Final x = 0. Result: `0 0 0 0`.
- `a2` = 6, B5 before A6: final x = 6. A9 reads either 0 (B9 between A2 and A9) or 6 (B9 after A9). Results: `6 0 6 6` and `6 6 6 6`.
- `a2` = 6, B5 after A6: final x = 4. A9 again reads 0 or 6. Results: `4 0 4 6` and `4 6 4 6`.

Q1 and Q3 always match, and each combination above is realized by a valid interleaving.

BEGIN
0 0 0 0
6 0 6 6
6 6 6 6
4 0 4 6
4 6 4 6
END