**Q1 (A2) is always 0.**
- The only write to y is A3, which writes 4.
- A2 runs before A3 in thread A, so no write to y has taken effect when A2 reads.

**Q3 (C3) can be 0 or 4.**
- C3 returns 4 if A3 takes effect before C3, and 0 otherwise.

**What A1 = 3 and C2 = 3 force.**
- The writes to x are B1 (4), C1 (3) and C4 (the value C3 read, so 0 or 4).
- A1 returns 3, so C1 is the last write to x before A1.
- So B1 is either before C1 or after A1, and C4 is after A1.
- C2 also returns 3, so B1 does not fall between C1 and C2.

**Q2 (A4), when C3 = 0.** C3 is before A3, so C4 writes 0.
- A4 = 0: order B1, C1, A1, C2, C3, A2, A3, C4, A4.
- A4 = 3: order B1, C1, A1, C2, C3, A2, A3, A4, C4.
- A4 = 4: order C1, C2, C3, C4, A1, B1, A2, A3, A4.
  - Here C4 writes 0 before A1, so this breaks A1 = 3 as written. A valid order is C1, A1, C2, C3, C4, B1, A2, A3, A4: C4 writes 0 after A1, then B1 writes 4 before A4.

**Q2 (A4), when C3 = 4.** A3 is before C3, so C4 writes 4.
- A4 = 3: order B1, C1, A1, A2, A3, C2, C3, A4, C4.
- A4 = 4: order B1, C1, A1, A2, A3, C2, C3, C4, A4.
- A4 = 0 is impossible, because no write of 0 to x happens in this case.

BEGIN
0 0 0
0 3 0
0 4 0
0 3 4
0 4 4
END