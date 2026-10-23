Reading the sync points as ordering constraints gives the following timeline:

- A1–A3 end before Q, and A3 reads z.
- B2 starts after Q, and B3 starts after S, which is after A1. So B4 is the first write to z by thread B, and it happens after A3.
- B1–B5 end before R, and A4 onward starts after R.
- B6 ends before P, and A9 starts after P.

**A3 and B1.** A3 always returns 1, because only A1 has written z by then. B1 returns 0 or 4, which doesn't affect the asked values.

**Q1 (A7).** A7 reads z after A6 has written 1. The only other write that can land between A6 and A7 is B8 (writing 3). B4 happens before R, so it is overwritten by A4 and A6. So A7 is 1 or 3.

**Q2 (B6).** B3 has already written 3 before B6, so B6 is never 0. B6 can see A8's value only if A8 comes before B6.
- If A7 = 3, then B6 < B7 < B8 < A7 < A8, so A8 cannot precede B6. Hence B6 = 3.
- If A7 = 1, B6 can be 3, or 1 if A8 precedes B6.

**Q3 and Q4 (final x and z).**
- The final x is decided by A9 (writes 1) versus B7 (writes 5), since A8 comes before A9. So x is 1 or 5.
- The final z is decided by A6 (1) versus B8 (3). So z is 1 or 3.

**Cases:**
- **A7 = 1, B6 = 1.** A8 precedes B6, so B8 cannot come before A6, since that would force B6 < B8 < A6 < A8 < B6. B8 therefore comes after A7, giving z = 3. x can be 1 or 5.
- **A7 = 1, B6 = 3.**
  - If B8 comes before A6, then z = 1. B7 comes before A6 and A9 follows, so x = 1.
  - If B8 comes after A7, then z = 3, and x can be 1 or 5.
- **A7 = 3, B6 = 3.** B8 lies between A6 and A7, so B7 and B8 both precede A9. Thus x = 1 and z = 3.

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
3 3 1 3
END