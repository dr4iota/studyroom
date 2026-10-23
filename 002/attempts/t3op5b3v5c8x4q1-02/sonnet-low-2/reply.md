A2 can only return 0.

- A3 writes A2's value to z, and A5 (which comes after A3) reads z as 0.
- The only other writes to z are B1 (writes 4) and C5 (writes C3's value). C3 reads y after C2 has written 1. Every later write to y is also 1 (B3 writes 1), and C1's 5 is overwritten by C2 before C3, so C3 returns 1. C5 therefore writes 1.
- Every write to z is therefore nonzero except possibly A3's. If A3 wrote a nonzero value, z would stay nonzero afterward, and A5 could not read 0. So A3 must write 0, which means A2 returned 0.
- This is achievable: A2 reads y before any write to y, and A4 later reads 1 after C2 or B3 has written y.

BEGIN
0
END