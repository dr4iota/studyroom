Q1 can be 0, 1 or 3. Q2 is always 2.

**Final z is 2.**
- A6 read 0, but A1 and A5 already wrote 2 and 4 to z. The only write that can produce a 0 is B6, so B1 must have read 0.
- B6 therefore falls between A5 and A6, in the order A5 < B6 < A6.
- B2 and B3 read 2 in the window after A1 and before A5, which gives B3 < A5 < B6 < A6 < A7 < A8.
- C8 read 2, so some write of 2 comes after C5 and before C8. If C5 came after A8 there would be no such write, so C5 comes before A8.
- A8 is therefore the last write to z, and z ends at 2.

**A4 can be 0, 1 or 3.**
- B1 read 0, so B5 writes 0 to y. Final y = 1 forces C7 to come after B5.
- The x constraints force the order B1 < A2 < C3 < C4. A3 reads 3 after A2 and B4 reads 1 after A2, so A4 comes after A2.
- A4 comes before A5, but nothing ties it to C's progress or to B5, so it can see any of three values:
  - 0: A4 runs before any write to y, or after B5.
  - 3: A4 runs after C2 and before B5 and C7.
  - 1: A4 runs after C7. This is allowed because C7 only needs to follow C4, and A3 and B7 only need to read 3 before C6.

BEGIN
0 2
3 2
1 2
END