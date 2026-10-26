Only A3 and C6 are open: A3 can return 1 or 5, and C6 must return 4.

**Fixing the order of the threads.** The final value z = 1 can only come from B1, so B1 must be the last write to z. B1 is B's first operation, so the rest of B comes after it. A7 and C8 are also writes to z, and they are the last operations of A and C. Both must therefore take effect before B1. So every operation of A and C happens before every operation of B.

**Constraints on y.**
- B2 reads y as 4 after A and C have finished, so the last write to y in A and C must be 4. Only A4 writes 4, so A4 is the last write to y.
- C3 returns 5 and C4 returns 4. C1 is the only write of 5, so C1 comes before C3. Between C3 and C4 some write of 4 must occur, and that can only be A4. The order is therefore C1 < C3 < A4 < C4.
- A1 can take effect either before C1, or after C3 and before A4. It cannot fall between C1 and C3, because C3 must still read 5.
- A6 reads 4 after A4, and no y-write follows A4, so that holds.
- B3 reads 4 and rewrites 4, B7 reads 4, and x = 4 is written by A2 and C5, so the rest of B is consistent.

**A3.** It comes after A1 and before A4, so it reads the last of A1 and C1 before it. Both values are achievable:
- A3 returns 1 with the order A1, A3, C1, C3, A4, C4.
- A3 returns 5 with the order A1, C1, A3, C3, A4, C4.

**C6.** It comes after C4, which is after A4, and no write to y follows A4, so C6 returns 4.

BEGIN
1 4
5 4
END