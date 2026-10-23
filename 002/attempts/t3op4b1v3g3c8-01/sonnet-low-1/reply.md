Q1 is B2's returned value and Q2 is the final value of x.

**Q1 (B2's value).** B1 runs before B2, so B2 can never read 0. It can read 1 (from C4), 2 (from B1, C1 or C3), or 3 (from C2), so Q1 ∈ {1, 2, 3}.

**What the known results force.**
- B3 returns 1, so a write of 1 must be the latest one before it. That write is either C4 or A3 with A1 having read 1.
- A2 returns 2, so some write of 2 must precede it with no later write in between.
- B4 writes B2's value, and A3 writes A1's value.

**Q1 = 3.**
- B4 writes 3, and B3 reads 1 before B4. The 1 must therefore come from C4, because the A3 route leaves no 2 for A2 to read.
- The last write is then either B4 (3) or A3 (A1's value).
- A1 can be 0, 2 or 3. It cannot be 1: A1 would have to read C4's 1, and then A2 could not read 2 afterwards.
- So the final value is 0, 2 or 3.
- Final 1 is impossible. C4 would have to be last, but B4 comes after the write of 1 that B3 read, and B4 writes 3.

**Q1 = 2.**
- Final 2: B4 is the last write.
- Final 0 or 3: A3 is last, with A1 having read 0 or 3.
- Final 1 works with this order: B1, B2 (2), C1 to C4, B3 (1), A1 (1), B4 (2), A2 (2), A3 (1).
- So the final value can be 0, 1, 2 or 3.

**Q1 = 1.**
- Final 1: the C writes finish, then B2, B3 and B4, with A2 having read 2 before C4.
- Final 0, 2 or 3: A3 is last, with A1 having read 0, 2 or 3.
- So the final value can be 0, 1, 2 or 3.

BEGIN
1 0
1 1
1 2
1 3
2 0
2 1
2 2
2 3
3 0
3 2
3 3
END