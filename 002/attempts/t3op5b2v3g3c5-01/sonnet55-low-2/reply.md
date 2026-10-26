All outcomes below are written as A4, C3, final x.

Every execution has the same two parts: B1 reads some value v from y, and B2 and B3 write v to x. The final value of x is therefore v. A4 is the y-read and C3 is the x-read.

**Which values v can B1 read?**
- B1 runs before B4, so it can only see values written by C2 (2) or C5 (1), or the initial 0.

**Case v = 0.**
- B1 read 0, so every write to x is 0. Hence C3 = 0 and the final x = 0.
- A4 can read 0, 2 (after C2 or B4) or 1 (after C5).
- Outcomes: (0,0,0), (1,0,0), (2,0,0).

**Case v = 1.**
- B1 read 1, so C5 came before B1, and so did C2. C3 comes before C5 in thread C, so C3 is before B2 and reads 0.
- Final x = 1. A3 = 0 is consistent because A3 can run before B2.
- A4 can still read 0 (before C2), 2 (after C2), or 1 (after C5, before B4's write).
- Outcomes: (0,0,1), (1,0,1), (2,0,1).

**Case v = 2.**
- B1 read 2, which can only come from C2, so C2 came before B1. The final x = 2.
- C3 can read 0 (before B2) or 2 (after B2).
- A3 = 0 forces A3 before B2, but A4 can still read 0 (before C2), 2, or 1 (C5 after C3).
- All six combinations of A4 ∈ {0,1,2} and C3 ∈ {0,2} are possible.

BEGIN
0 0 0
1 0 0
2 0 0
0 0 1
1 0 1
2 0 1
0 0 2
1 0 2
2 0 2
0 2 2
1 2 2
2 2 2
END