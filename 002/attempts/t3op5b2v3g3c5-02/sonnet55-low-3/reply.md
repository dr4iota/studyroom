Because each operation takes effect at a single instant, every execution is some interleaving of the threads that keeps each thread's order. The two known results must also hold: A2 reads 2 and B5 reads 2.

**Q1 (A1).** The only values ever written to x are 2 (by C1) and copies of values read from x. So x is always 0 or 2, and A1 returns 0 or 2.

**Q2 (B3).** B1 has already written 1 to y, and y is never reset to 0. So B3 reads 1, 2 or 3.

**Q3 (final y).** The last write to y is A4 (3), C5 (a copy of what C4 read), or in principle B1 or C2. Because A2 reads 2, C2 comes before A2 and B1 cannot be last unless later writes follow it. The final value is therefore 1, 2 or 3.

**Final y = 3.** A4 is the last write to y. Here B3 can be 1, 2 or 3 and A1 can be 0 or 2.
- For B3=1, B1 and B3 come before C2, with A2 after C2.
- For B3=2, B3 falls between C2 and A4.
- For B3=3, B3 comes after A4, and C5 is already done.
- For A1=0, B2 reads 2 after C1, then B4 writes 2 and B5 reads 2 before A3 writes 0.

All 6 combinations work.

**Final y = 2.** C5 writes 2 after A4, because C4 read 2 before A4. The same reasoning allows B3 = 1, 2 or 3 and A1 = 0 or 2. For B3=3, B3 comes after A4 and before C5. All 6 combinations work.

**Final y = 1.** C5 must write 1 last, so C4 reads 1. That needs B1 after A4, which puts all of B after A4. A4 is after A2, which is after C2 and C1, and A3 comes before A4.
- If A1=0, A3 writes 0 to x after C1. Then B2 reads 0 and B5 reads 0, contradicting B5=2. So A1=0 is impossible.
- If A1=2, the order C1, A1, C2, A2, A3, A4, B1, B2, B3, B4, B5, C3, C4, C5 works. B3 reads 1 because only B1 has written y since A4.

So the only combination is A1=2, B3=1, final y=1.

BEGIN
0 1 2
0 2 2
0 3 2
0 1 3
0 2 3
0 3 3
2 1 1
2 1 2
2 2 2
2 3 2
2 1 3
2 2 3
2 3 3
END