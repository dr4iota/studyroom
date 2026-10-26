Final values: x is 4 or 1, y is 6 or 1, and z equals what B9 read, which is 0 or y.

**Ordering constraints.** B1 < P < A3 and A1 < S < B5. B2 < Q < A9 and A9 < R < B8. A2 is only constrained to come after A1 and before A3.

**A4.** z is written only by A1 (6), B1 (1), A6, A9 and B8. A4 runs after B1 and A1, before A6, A9 and B8. So A4 reads 6 or 1, depending on whether A1 or B1 took effect last. Call this value a.

**The z chain in A.** A6 writes a to z, so A7 reads a, since no B write to z can fall between them. A8 writes a to y, so y is a. A9 writes a to z.

**Final y.** A8 is the only write to y, so y = a, which is 6 or 1.

**B2.** B2 reads y before Q. A8 may happen before or after B2, so B2 returns 0 or a. Both are possible, because A8 can take effect before Q.

**Final z and B9.** B8 comes after R, which is after A9, so B8 is the last write to z. It writes B2's value, so the final z is B2's value. B9 reads that same value, so Q1 = Q4 = B2's value.

**Final x.** B3 reads 0 or 1. B7 writes 4, but A2 can take effect after B7. It only needs to come before A3, which can be late. So the final x is 4 or 1. This is independent of the other choices.

**Combinations (Q1 Q2 Q3 Q4).**
- B2 = 0: Q1 = Q4 = 0, with x in {4, 1} and y in {6, 1}.
- a = 6 and B2 = 6: Q1 = Q4 = 6, y = 6, x in {4, 1}.
- a = 1 and B2 = 1: Q1 = Q4 = 1, y = 1, x in {4, 1}.

BEGIN
0 4 6 0
0 1 6 0
0 4 1 0
0 1 1 0
6 4 6 6
6 1 6 6
1 4 1 1
1 1 1 1
END