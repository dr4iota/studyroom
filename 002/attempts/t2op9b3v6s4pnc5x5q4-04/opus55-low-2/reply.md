**Ordering constraints from the sync points**
- B1 and B2 come before Q, and Q comes before A9. A9 comes before R, and R comes before B8 and B9. So all of Thread A finishes before B8.
- B1 comes before P, and P comes before A3.
- A1 comes before S, and S comes before B5.

**z and B9.** B8 writes the value read by B2 to z. B8 is the last write to z, and B9 runs right after it with no other writes to z in between. So B9 = final z = the value read by B2.

**The value v read by A4.** B1 happens before A3, and A1 also happens before A4. The two can be in either order, so A4 reads either 6 (from A1) or 1 (from B1). Call this value v.
- A6 writes v to z.
- The next write to z after A6 is A9 or B8, so A7 reads v.
- A8 writes v to y.
- A8 is the only write to y, so final y = v.

**B2.** B2 only has to come before Q. A8 also comes before Q, so B2 can happen before or after A8. B2 therefore reads 0 or v.

**Final x.** B7 writes 4 to x and must come after S. A2 writes 1 to x and only has to come before R. A2 may come after S, so it can follow B7. Final x is therefore 4, or 1 if A2 takes effect after B7.

**Possible outcomes.** Final x is 1 or 4. For each choice of x:
- With v = 1: (B9, z) = (0, 0) or (1, 1), and y = 1.
- With v = 6: (B9, z) = (0, 0) or (6, 6), and y = 6.

BEGIN
0 1 1 0
1 1 1 1
0 4 1 0
1 4 1 1
0 1 6 0
6 1 6 6
0 4 6 0
6 4 6 6
END