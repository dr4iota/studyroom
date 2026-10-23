Reading the sync lines gives these constraints:

- B1–B8 all finish before P, Q, R and S.
- A1 starts after Q and R, so A1 runs after B8.
- B9 is only ordered after B8. It can happen at any point after that, relative to thread A.

**Values of y and x**

- B2 reads y before B4 writes 3. Thread A can't have written y yet, because A4 comes after A1, which comes after B8. So B2 returns 0.
- B8 therefore writes 0 to y. A1 reads y = 0, and A2 writes 0 to z.
- After B8, x = 4, because B3 wrote 4 and B9 hasn't run yet.
- B9 writes B2's value, 0, to x at some later point.
- So A3, A5, A6 and A8 each read either 4 or 0. Once B9 has taken effect they all read 0, so the reads form a run of 4s followed by a run of 0s.

**Final y**

A4 is the last write to y and it writes A3's value, so the final y equals A3's value.

**Cases**

- A3 = 4: (A5, A6, A8) can be 444, 440, 400 or 000, and y = 4.
- A3 = 0: every later read of x must also be 0, so A5 = A6 = A8 = 0, and y = 0.

BEGIN
4 4 4 4
4 4 0 4
4 0 0 4
0 0 0 4
0 0 0 0
END