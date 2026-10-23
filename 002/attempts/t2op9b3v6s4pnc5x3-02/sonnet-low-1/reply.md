Every combination of A2 in {0, 4} and A3 in {0, 4} is possible, and A7 is always 4.

**Constraints from the sync points**
- A1–A3 must end before R. A4 onward must start after P and S. A7 and A8 must start after Q.
- B1–B4 must end before S. B1–B6 must end before P. B7 onward must start after R. B1–B8 must end before Q. B9 is unconstrained.

**B5 and B6.**
- B5 ends before P, and A's writes to x (A4, A6) start after P, so they cannot affect B5.
- B3 writes 4 to x before B5 in B's program order.
- So B5 reads 4, and B6 writes 4 to z.

**A2 (z).**
- A2 ends before R, so it cannot see B9's write of 3, because B9 starts after R.
- A2 also cannot see A5's write of 2, because A5 comes after A2 in A's program order.
- The remaining writes to z are B1 and B6, both 4. So A2 is 0 or 4.

**A3 (x).**
- A's own writes to x come after A3.
- The only other write to x is B3, which writes 4. So A3 is 0 or 4.

**Independence of A2 and A3.**
- A2 = 0 with A3 = 0: A1–A3 run before B1 and B3.
- A2 = 0 with A3 = 4: A2 runs before B1, then B3 runs before A3.
- A2 = 4 with A3 = 0: B1 runs, then A2 and A3, then B3.
- A2 = 4 with A3 = 4: B1 and B3 both run before A2 and A3.
- So all four combinations are possible.

**A7 (y).**
- A7 starts after Q, and B8 ends before Q, so B8 has already written.
- B8 writes B5's value, which is 4, and it comes after B2 (which writes 2) in B's program order.
- A8 comes after A7. So A7 always reads 4.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END