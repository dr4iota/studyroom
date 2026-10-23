B9 always equals the final z, z is 0 or the value A4 read, y is always the value A4 read (1 or 6), and x ends at 4 or 1.

**Ordering constraints from the sync points**
- B1 < P < A3
- B2 < Q < A9
- A1 < S < B5
- A9 < R < B8, so every A operation takes effect before B8 and B9.

**y and z inside thread A**
- The only writes to z that can come before A4 are A1 (6) and B1 (1). Both happen before A3, so A4 returns 6 or 1, depending on which of A1 and B1 takes effect last.
- B1 cannot fall between A6 and A7, because B1 is before A3. Therefore A7 returns what A6 wrote, which is A4's value.
- A8 is the only write to y, so the final y equals A4's value.

**B2, B9 and the final z**
- B2 returns 0 if it runs before A8. It returns A4's value if it runs after A8. Both are allowed, since only B2 < Q < A9 is required.
- B8 writes B2's value to z after every A write. B9 then reads z with no later writes, so B9 = final z = B2's value.

**Final x**
- B7 writes 4. Nothing forces A2 to come before B7, so A2 may take effect last and the final x may be 1.
- If A2 comes last, the chain B2 < B5 < B7 < A2 < A8 holds. B2 is then before A8 and returns 0. So final x = 1 forces z = 0.
- With final x = 4, every combination above is possible.

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
0 1 1 0
0 1 6 0
END