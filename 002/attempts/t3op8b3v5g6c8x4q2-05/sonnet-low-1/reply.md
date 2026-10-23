Only A6 and the final z depend on the constraints, and both reduce to short ordering arguments.

**Q1 (A6).**
- A3 reads y = 2, so C3 has taken effect, and therefore C2 as well, before A3. A4 comes after A3, and A8 comes after A6.
- So after A3 the only write to y before A6 is A4, which writes 1, and A6 returns 1 in every valid execution.

**Q2 (final z).** The writes to z are A1 (2), A2 (5), B8 (the value read by B3) and C6 (1).
- B4 reads z = 2, so B4 falls after A1 and before A2.
- C8 reads z = 3. The only write that can put 3 in z is B8, whose value is the one read by B3, and B3 does return 3 because B2 is known to return 3 and B3 follows it.
- So the order is C6 < B8 < C8, B8 comes after B4, and A2 cannot fall between B8 and C8.
- That leaves two cases for A2:
  - A2 before B8: B8 is the last write, so z ends at 3.
  - A2 after C8: A2 is the last write, so z ends at 5.
- Both cases are consistent with the other constraints:
  - A3 needs C3 before it, and A2 comes before A3 in thread A. A2 after C8 is still possible because C8 can happen after C3 and before A2.
  - Final x = 3 holds as long as the last x write is C7 or one of B5–B7, all of which write 3.

BEGIN
1 3
1 5
END