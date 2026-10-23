**x is always 0.** The only writes to x are A3 and B3. A3 writes the value A1 read from x, and B3 writes the value B1 read from x. Since x starts at 0, no write can ever introduce a value other than 0. So A1 = 0 and B1 = 0, which also matches B4 returning 0.

**Writes to y:**
- C1 writes 2.
- A4 writes 3.
- A5 writes the value A1 read, which is 0.
- B5 writes 1.
- C4 and C6 write the value C3 read.
- C5 writes 2.

A2 returning 2 is consistent, because A2 can read the 2 from C1.

**Q3, the value C3 reads.** C3 comes after C1, so it cannot see the initial 0. It also cannot see C4, C5 or C6, which come after it. So it reads from C1, A4, A5 or B5:
- **2**: C3 reads C1's write.
- **3**: C3 reads A4's write.
- **0**: A2 reads C1's 2, then A4 and A5 take effect, then C2 and C3 read A5's 0.
- **1**: B5 takes effect before C3.

**Q2, the value B2 reads.** B2 comes before B5, so it can see the initial 0, C1's 2, A4's 3, A5's 0, or a C4/C6 write. The C4/C6 writes only repeat C3's value, which is already covered. So B2 can be 0, 2 or 3.

**Every pair of Q2 and Q3 is possible.** Each of the 12 pairs can be scheduled. Two examples:
- B2 = 3 and C3 = 0: A2, then A4, then B2, then A5, then C3.
- C3 = 1: A2 reads C1's 2, then A4, then B2, then B5, then C3. B2 still gets 0, 2 or 3 depending on where it falls.

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END