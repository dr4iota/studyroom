Every combination of B2, C4, final y and final z that fits the known results is: B2 returns 2, C4 returns 2 or 5, y ends as 2, and z ends as 2 or 4.

**Known results**
- A2 reads y = 2. The only writes to y are C1 (value 2) and B4 (value of B1), and B1 can only read 0 or 2. So the value 2 can only come from C1, which takes effect before A2.
- C2 reads z = 3. The only write of 3 to z is A1, since B3 writes 0 or 2. So A1 takes effect before C2, and no other z-write lands between A1 and C2.
- B5 reads z = 2. The only write that can give z = 2 is B3, and only if B1 read 2. So B1 = 2, which means C1 takes effect before B1. B3 is then the last z-write before B5, so A4 cannot fall between B3 and B5.

**Q1 and Q3 (B2 and final y)**
- Every write to y is the value 2, and C1 takes effect before B1 and B2. B2 therefore reads 2.
- The final y is 2, since the only writes to y are C1 and B4, both writing 2.

**Q4 (final z)**
- B3 before A1 gives B3 < B5 < A1 < C2, and A4 comes last. The final z is 4.
- A1 before B3 gives A1 < C2 < B3 < B5. A4 can fall between C2 and B3, which leaves B3's 2 as the last write, so the final z is 2. A4 can also come after B5, which gives a final z of 4. A4 cannot fall between A1 and C2, so no other placement is possible.
- The final z is therefore 2 or 4.

**Q2 (C4)**
- C3 takes effect before C4, so C4 never reads 0. The only other write to x is A3 (value 2).
- C4 reads 5 if A3 is before C3 or after C4. It reads 2 if A3 falls between C3 and C4.
- A3 is unconstrained relative to C3 and C4 in every case above, so both 2 and 5 are possible with each final z.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END