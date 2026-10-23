Each case below is a valid ordering of the operations.

**What B1 can read.** The only writes to x are B2 and B3, and both write the value B1 read from y. Call that value v.
- B4 comes after B1, so B1 can only see C2's 2 or C5's 1.
- So v is 0, 1 or 2.
- The final value of x is always v, because B3 is the last write to x.

**C3 and A3.** C3 reads x, so it returns either 0 or v. A3 returned 0, so either A3 takes effect before B2, or v = 0.

**Case v = 0.** Every write to x stores 0, so C3 = 0 and x ends at 0.
- A4 can return 0 if thread A finishes before C2.
- A4 can return 2 if it falls after C2 or B4 and before C5.
- A4 can return 1 if it falls after C5, with B4 before C5 or after A4.

**Case v = 2.** B1 must come after C2.
- C3 = 0 is possible if C3 falls before B2. C3 = 2 is possible if it falls after B2.
- A4 = 0: thread A runs entirely before C2. This also puts A3 before B2.
- A4 = 2: A4 falls after C2 and before C5.
- A4 = 1: A4 falls after C5. C5 comes after C3, so this works with either value of C3.
- All six pairs of A4 and C3 are possible, with x ending at 2.

**Case v = 1.** B1 must come after C5, which comes after C3. So C3 takes effect before B2 and returns 0.
- A3 must also come before B2.
- A4 = 0 if thread A runs early.
- A4 = 2 if A4 falls between C2 and C5, or after B4.
- A4 = 1 if A4 falls after C5 and before B4.

BEGIN
0 0 0
1 0 0
2 0 0
0 0 2
0 2 2
1 0 2
1 2 2
2 0 2
2 2 2
0 0 1
1 0 1
2 0 1
END