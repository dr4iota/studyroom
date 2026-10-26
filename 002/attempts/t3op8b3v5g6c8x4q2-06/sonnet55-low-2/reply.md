Every consistent execution ends with z = 2, and A4 can return 0, 1 or 3.

**Constraints on x, z and B1**

- A6 reads z = 0, yet A1 and A5 (earlier in thread A) both wrote nonzero values to z. So some write of 0 must land after A5 and before A6. The only candidate is B6, which writes B1's value. So B1 read 0, and A5 < B6 < A6 with no other z write in between.
- B1 read 0, so B1 comes before A2 and before every other write to x. B5 therefore writes 0 to y.
- B2 and B3 read z = 2. The only write of 2 that can be the latest write at that point is A1, because A8 comes after A6. So A1 < B2 < B3 < A5.
- B4 reads x = 1, so A2 is the last x-write before B4. B7 reads 3 later, so a write of 3 comes after B4, and C6 (which writes 4) comes after B7.
- C5 comes after C4, which comes after B4, so C5 comes after A1.
- C8 reads z = 2. Every z-write other than A8 is ruled out as the latest write at that point: A1 is overwritten by A5, and C5, A5 and B6 all write other values. So A8 is the latest write before C8.
- A8 is the last z write before C8, and C5, A5, A7, B6 all come before A8. Hence the final z is 2.

**Constraints on y**

- The final y = 1. B5 writes 0, so C7 (which writes 1) must be the last write to y, with C2 (3) before it.
- A4 comes after A3, which comes after C1.

Each value of A4 has a valid execution:

- A4 = 0: A4 runs after A3 and before C2.
- A4 = 3: A4 runs after C2 and before C7.
- A4 = 1: A4 runs after C7, and C8 comes later.

For example, for A4 = 0 an order of A1, B1, B2, B3, A2, B4, C1, A3, A4, A5, B6, A6, … works, with A7, A8, C2 through C8 placed to meet the constraints above.

BEGIN
0 2
1 2
3 2
END