C4 can return 1, 2 or 4.

**Ordering forced by the known reads.** The writes to y are A1 (value 1) and C3 (value 4).
- B1 returns 1, so A1 takes effect before B1, and C3 takes effect after B1.
- A4 returns 4, so C3 takes effect before A4.
- Together: A1 < B1 < C3 < A4.

Thread C runs in order, so C1 < C2 < C3 < C4.

**C4 cannot return 0.** C1 writes 2 to z before C4 runs, so z is never 0 at C4.

**C4 returns 2.** Put A2 and B3 before C1, in the order A1 < A2, B1 < B2 < B3 < C1 < C3 < C4. C1 is then the last write to z before C4.

**C4 returns 1.** Let A2 take effect after C1 and before C4. B3 either happens earlier or writes 1 as well (B2 reads 1), so A2 is the last write to z.

**C4 returns 4.** Let B2 read y after C3, so it returns 4. Then B3 writes 4 to z. Put A2 before B3 and B3 before C4. B3 is then the last write to z.

BEGIN
1
2
4
END