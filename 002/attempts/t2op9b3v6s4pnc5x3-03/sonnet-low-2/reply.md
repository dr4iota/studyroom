Reading the sync points shows that every operation of thread B finishes before Q. Q comes before A2 starts, so A2 through A8 all run after all of B. Only A1 can interleave with B.

**Thread B**
- B1 and B2 both read x, which is still 0, because the only writes to x are B5 and A5, and both come later.
- B3 reads y. It returns 1 if A1 has already happened, otherwise 0. Call this value v.
- B4 writes 6 to z.
- B5 writes v to x.
- B6 writes B2's value (0) to y.
- B7 writes 6 to y.
- B8 reads y. It returns 6, unless A1 takes effect between B7 and B8, in which case it returns 1.
  - If v = 1, A1 came before B3, so B7 overwrites it and B8 must be 6.
  - If v = 0, B8 can be 6 or 1.

**Thread A (after all of B)**
- A2 reads x, which holds v from B5.
- A3 writes 2 to z.
- A4 writes v to y.
- A5 writes v to x.
- A7 reads z. B4 wrote 6 earlier, but A3 overwrote it with 2, and nothing writes z afterwards, so A7 = 2.
- A8 reads y. A1 came before A2, and A4 is the last write to y, so A8 = v.

**Cases**
- v = 1: A7 = 2, A8 = 1, B8 = 6.
- v = 0: A7 = 2, A8 = 0, and B8 is either 6 or 1.

Answer, in the order A7, A8, B8:

BEGIN
2 1 6
2 0 6
2 0 1
END