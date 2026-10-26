**Constraints from the sync points**

- B1 < P < A3, so B1 ends before A3 starts.
- B2 < Q < A9.
- A1 < S < B5.
- A9 < R < B8. This means all of thread A has finished before B8.
- A2 itself has no sync constraint.

**What A4 and A7 return, and the final y**

- z is written only by A1 (6), B1 (1), A6, A9 and B8.
- Before A4, both A1 and B1 have already taken effect, because B1 < P < A3 < A4.
- So A4 returns whichever of A1 and B1 took effect later. That is 6 or 1, and both orders are possible.
- A6 writes that same value. No other write to z can fall between A6 and A7, so A7 also returns the A4 value.
- A8 writes it to y. Thread B never writes y, so the final y equals the A4 value (1 or 6).

**What B2 returns, B9, and the final z**

- B2 reads y. It returns 0, or it returns the A4 value if B2 comes after A8. That is allowed, since A8 < B2 < Q < A9 is consistent.
- B8 writes the B2 value to z after all of A has finished. B9 then reads it back.
- So B9 equals the final z, which equals the B2 value.

**Final x**

- The last write to x is either B7 (4) or A2 (1).
- A2 can come after B7: A1 < S < B5 < B6 < B7 < A2 is consistent.
- However, if B2 comes after A8, the chain B2 < … < B7 < A2 < … < A8 is impossible. So when B2 returns a nonzero value, the final x must be 4.
- When B2 returns 0, the final x can be 1 or 4.

**Combinations (B9, x, y, z)**

| A4 value | B2 returns | Possible final x | Combinations |
|---|---|---|---|
| 6 | 0 | 1 or 4 | 0 4 6 0, 0 1 6 0 |
| 6 | 6 | 4 | 6 4 6 6 |
| 1 | 0 | 1 or 4 | 0 4 1 0, 0 1 1 0 |
| 1 | 1 | 4 | 1 4 1 1 |

BEGIN
0 4 6 0
0 1 6 0
6 4 6 6
0 4 1 0
0 1 1 0
1 4 1 1
END