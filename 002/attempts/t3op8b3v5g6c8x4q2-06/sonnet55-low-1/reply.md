Q1 can be 0, 1 or 3. Q2 is always 2.

**Ordering of the x operations.**
- A3 reads 3, so a 3-write (C1 or C3) lands after A2 and before A3.
- B4 reads 1, so the last write to x before B4 is A2.
- B7 reads 3 after B4, so a 3-write comes after A2 and B4.
- Together these force A2 < C3. B4 falls between A2 and the next x write, and C6 comes after B7.

**What B1 read.** B1 happens before B4, and B2 and B3 each read z = 2.
- B1 is a read of x, and its value v is written to y by B5 and to z by B6.
- A6 reads z = 0, even though A1 and A5 have already written 2 and 4 to z. So B6 must be the last write to z before A6, and v = 0.
- Hence B1 read x = 0, so B1 precedes A2 and C1.
- B5 therefore writes 0 to y. Since y ends at 1, B5 must come before C7.

**Q2, the final z.**
- A1 is the last z-write before B2 and B3, since they read 2.
- C8 reads z = 2 after C5 wrote 4. The 2 must come from A8, because A1 is already before C5.
- So the last write before C8 is A8, and C5 comes before A8.
- All other z-writes (A5, A7, B6) also come before A8, so the final z is 2.

**Q1, the value A4 reads from y.** A4 comes after A3 and before A5, and A5 is before B6.
- 0 is possible, from the initial value or from B5.
- 3 is possible if A4 falls after C2 and before B5 and C7.
- 1 is possible if A4 falls after C7. C7 can come early enough, since C7 only needs to follow B7 and C6.

BEGIN
0 2
1 2
3 2
END