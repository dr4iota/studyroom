Every B operation through B8 must take effect before Q, and every A operation must take effect after Q. So B1 through B8 all precede every A operation. B9 is the only operation that can interleave with A.

**Fixed values from B1–B8:**
- B1 sets x=2, and B3 sets x=4. B2 reads y before any write to y, so b2=0.
- B5 reads x=4, so B6 writes z=4. B7 writes z=1. B8 writes y=0.
- After B8: x=4, y=0, z=1.

**A's reads:**
- A1 reads y=0, so A2 writes 0 to z.
- Nothing writes x during A except B9, which writes b2=0 to x. So x is 4 until B9 takes effect and 0 afterward.
- A4 writes a3 to y, and it is the only write to y after B8, so the final y equals a3.

**Where B9 can fall in A's sequence** (reads of x are a3, a5, a6, a8):
- Before A3: 0 0 0 0
- Between A3 and A5: a3=4, a5=0, a6=0, a8=0
- Between A5 and A6: a3=4, a5=4, a6=0, a8=0
- Between A6 and A8: a3=4, a5=4, a6=4, a8=0
- After A8: all 4

Each row gives Q1=a5, Q2=a6, Q3=a8, Q4=a3.

BEGIN
0 0 0 0
4 0 0 4
4 4 0 4
4 4 0 4
4 4 4 4
END