Every execution has A3 = 1, because A1 is the only z-write that can precede A3, so A9 writes 1 to x.

**Constraints**
- A1 and A3 finish before Q, and B2 starts after Q.
- B2 and B3 start after Q and S respectively, and B1–B4 finish before R, so B3 (x=3) precedes B6.
- A4–A8 start after R, and B5 and B6 also come after R.
- B6 finishes before P and A9 starts after P, so B6 precedes A9.

**Q1: A7**
- A7 reads the last z-write before it. A4, A5 and A6 write 1, 6 and 1, so A6 overwrites 6.
- B8 can only write 3 after B7, which is after B6.
- So A7 is 1, or 3 if B8 lands between A6 and A7.

**Q2: B6**
- B3 has already written 3 to x, so B6 is not 0. B6 reads either 3 or A8's value if A8 came first.
- A8 can precede B6 only if A7 precedes B6, so B8 has not run yet and A7 = 1. Then B6 = 1.

**Case A7 = 3**
- Then B6 < B7 < B8 < A7 < A8 < A9, so B6 = 3.
- A9 is the last x-write, so x = 1.
- B8 is the last z-write after A6, so z = 3.
- Result: (3, 3, 1, 3).

**Case A7 = 1, B6 = 3**
- Final x is 1 if B7 precedes A9, otherwise 5.
- z = 1 is possible when B8 runs before A4, which needs x = 1.
- z = 3 is possible with B8 last.
- If x = 5, B7 comes after A9, so B8 is last and z = 3.
- Results: (1, 3, 1, 1), (1, 3, 1, 3), (1, 3, 5, 3).

**Case A7 = 1, B6 = 1**
- A8 precedes B6, so B8 comes after A7, which forces z = 3.
- x can be 1 or 5.
- Results: (1, 1, 1, 3), (1, 1, 5, 3).

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
3 3 1 3
END