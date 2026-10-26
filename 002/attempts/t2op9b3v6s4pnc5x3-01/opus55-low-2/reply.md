**1. Thread B's operations B1–B7 all take effect before any of A's operations.**
- B1 and B2 finish before P, B3 before R, B4 before Q, and B5–B7 before S.
- Every step of Thread A happens after S, which is after P, Q and R, because of the "after S" line above A1.
- Only B8 and B9 can interleave with A's operations.

**2. B2 returns 0.**
- Before A runs, the only write to z is B7, which comes after B2.
- So B2 reads z = 0, and B8 writes 0 to y.

**3. A8 always returns 6.**
- A1 writes 6 to z after B7 wrote 1.
- Nothing writes z after A1, so both A6 and A8 return 6.

**4. Where B8 falls decides A3, A4, and what A5 writes to x.**
- B4 and B5 have already written y, so y is nonzero when A starts. B8's write of 0 is the only way A3 or A4 can return 0.
- **B8 between A2 and A3:** A3 = 0 and A4 = 0, so A5 writes 0 to x.
- **B8 before A2:** A2 then sets y to 6, so A3 = 6, A4 = 6, and A5 writes 6 to x.
- **B8 between A3 and A4:** A3 = 6, A4 = 0, and A5 writes 0 to x.
- **B8 after A4:** A3 = 6, A4 = 6, and A5 writes 6 to x.

**5. B9 returns either 5 or A5's value.**
- B9 runs after B8.
- If B9 takes effect before A5, it reads 5 from B1.
- If it takes effect after A5, it reads the value A5 wrote.

**Resulting combinations (A3, A8, B9):**
- A3 = 0: B9 is 0 or 5.
- A3 = 6: B9 is 0, 5 or 6.

BEGIN
0 6 0
0 6 5
6 6 0
6 6 5
6 6 6
END