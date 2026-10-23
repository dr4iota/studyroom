**Analysis**

- B5 returns 2, so the last z-write before B5 must be B3 writing 2 → B1 read 2 (C1 precedes B1). All y-writes are 2 (C1, B4), so B2 = 2 and final y = 2.
- Final z: either A4 is after B5 (final z = 4) or A1, A4 both precede B3 (final z = 2); both are consistent with C2 reading 3 (A1 before C2, no A4/B3 in between).
- C4 returns 5 unless A3 lands between C3 and C4, giving 2; both are possible in either z case.

BEGIN
2 5 2 4
2 2 2 4
2 5 2 2
2 2 2 2
END