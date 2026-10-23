Reading the sync points: B1–B4 all finish before Q, and A5 starts after Q, so A4 ends before A5 starts. B5 starts after B4 and before P, so it can take effect before or after A4.

**Q1 (A1).** A1 can see 0 (before B1), 1 (after B1), or 3 (after B2). It can never see 2, because the only write of 2 is A4, which comes after A1. A2 only copies A1's value, so it cannot create a 2 either.

**Q2 (B3).** B3 reads after B2, so it sees 3 unless an A write lands between B2 and B3.
- A2 can land there, giving B3 the value A1 read (0 or 1, but not 3, which is already B2's value).
- A4 can land there, giving B3 the value 2.

So the possible (Q1, Q2) pairs are:
- a=0: B3 can be 0, 3 or 2.
- a=1: B3 can be 1, 3 or 2.
- a=3: B3 can be 3 or 2.

**Q3 (final y).** The last write to y is either A4 (value 2) or B5 (value 1).
- If B3 read 2, then A4 took effect before B3. B5 comes after B4, which comes after B3, so B5 is later than A4 and the final value is 1.
- Otherwise B5 can take effect either before or after A4, so the final value can be 1 or 2.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
1 3 1
1 3 2
1 1 1
1 1 2
1 2 1
3 3 1
3 3 2
3 2 1
END