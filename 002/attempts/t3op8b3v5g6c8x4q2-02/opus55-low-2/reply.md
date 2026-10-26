**Possible outcomes:** y = 0 with z = 3, and y = 4 with z = 3.

**1. A1 must return 0.**
- A3 reads z = 0. A2 is A's own write to z and takes effect before A3.
- So A2 must have written 0, with no other write to z between A2 and A3.
- A2 writes the value A1 read, so A1 returned 0.
- As a result, A4 writes 0 to x, and A5 and A7 each write 0 to y.

**2. Order of the writes to x.**
- The writes to x are A4 (0), C4 (5) and C7. C5 reads 4, so C7 writes 4.
- A8 reads x = 4. Only C7 writes 4, so C7 comes before A8.
- A4 must come before C7. If A4 came after C7, then A4's 0 would be the last write before A8.
- A1 read 0, but C4 and C7 both write nonzero values. So A1 comes before C4.

**3. Final y.**
- The writes to y are B4 (4), A5 (0) and A7 (0).
- C5 reads 4, so B4 comes before C5, with no write by A in between.
- B2 reads 0 before B4.
- A6 reads 0, so B4 does not fall between A5 and A6.
- There are two ways A7 can sit relative to B4:
  - All of A5, A6 and A7 happen before B4. Then the final y is 4.
  - A5 and A6 happen before B4, and A7 happens after C5 but before A8. Then the final y is 0.
- Both orderings fit every known result, so the final y is 0 or 4.

**4. Final z.**
- C1 (4) and C2 (5) come before C3 (3), and C6 reads 3 after C3.
- B1 (2) comes before B5 (3).
- The only write that could end up last with a value other than 3 is A2.
  - If A2 were last, A3 (which follows A2) would come after B8.
  - B8 is after B7, which is after C7. So A4 (after A3) would come after C7.
  - That contradicts step 2, where A4 must come before C7.
- So the last write to z is B5 or C3, and both write 3. The final z is 3.

BEGIN
0 3
4 3
END