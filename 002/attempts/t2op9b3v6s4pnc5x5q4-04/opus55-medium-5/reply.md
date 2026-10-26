Only five combinations are possible. B9 and the final z always equal what B2 read, and the final y always equals what A7 read.

**Ordering facts from the sync points**
- **R:** All of thread A happens before R, and B8 and B9 happen after R. So B8 is the last write to z, and B9 reads the value B8 wrote. That value is what B2 read. So Q1 = Q4 = (B2's value).
- **P:** B1 happens before P, and A3 happens after P. So both writes A1 (z=6) and B1 (z=1) happen before A4.

**Value read by A4 and A7 (gives Q3)**
- A4 returns 6 if B1 took effect before A1. It returns 1 if A1 took effect before B1. Both orders are allowed.
- A6 writes A4's value to z, and A7 then reads z. The only write that could fall between them would be B1 or B8. B1 is before P, and B8 is after R, so neither can. So A7 = A4 = v, where v is 1 or 6.
- A8 is the only write to y. So the final y = v.

**Value read by B2 (gives Q1 and Q4)**
- y is written only by A8. B2 is only required to be before Q, and A8 is not tied to Q. So A8 can fall either before or after B2.
- So B2 returns either 0 or v.

**Final x (gives Q2)**
- B7 (x=4) comes after B5 and B6, so B6 is never the last write to x.
- A2 (x=1) is not ordered against B5 to B7 by any sync point. So A2 can come after B7, which makes the final x = 1. Otherwise the final x = 4.
- If the final x is 1, then B2 < B7 < A2 < A3 < A8. So B2 reads 0.
- In that case B5 must follow S, which follows A1. Both orders of A1 and B1 still work: A1, S, B1, B2–B7, A2 gives v = 1, and B1, A1, S, B2–B7, A2 gives v = 6.

**Feasible combinations**
- x = 1 needs B2 = 0, and works with v = 1 or v = 6.
- x = 4 works with B2 = 0 or B2 = v, for v = 1 or v = 6.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END