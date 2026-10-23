The possible outcomes are 0 0 0 0, 0 3 0 3, 0 5 0 5, 0 5 5 5, and 5 5 5 5, in the order Q1 Q2 Q3 Q4.

**Constraints from the sync points**
- A1 and A2 take effect before P, and B2 onward take effect after P. So A2 < B2.
- A1 through A6 take effect before Q, and B8 and B9 come after Q. So A6 < B8.
- A1 through A6 take effect before S, and B4 onward come after S. So A6 < B4. This also implies A6 < B8.
- A1 and A2 take effect before R, and B6 onward come after R. This is implied by A2 < B2.

**Key facts**
- A2 always reads 0: every write to z by B comes after B2, which is after A2, and A6 comes after A2.
- B5 is after A6, so every read of y by A4 happens before any write to y by B. B9 reads y after B5, so B9 always equals the value B2 read.
- A3 always takes effect before B8, since A3 < A6 < B4 < B8.
- The writes to x are A1 (3), A3 (0), A7 (0) and B1 (5). B1 always precedes B2, and A1 always precedes B2.
- A8 is 0 or 5, since A7 always precedes A8 and A7 writes 0.
- B2 is 0, 3 or 5. It is 3 only if B1 precedes A1 and A3 comes after B2. It is 0 if A3 or A7 falls between B1 and B2.
- B8 is 0 or 5, since A3 always precedes B8, which rules out 3.

**Joint feasibility of (A8, B2, B8)**
- B2 = 0 forces A8 = 0 and B8 = 0. The combination (0, 0, 0) is achievable with B1, A3, B2 in that order.
- B2 = 3 forces A8 = 0 and B8 = 0. An example order is B1, A1, A2, B2, then A3 through A8, then B3 through B8.
- B2 = 5 gives four cases:
  - A8 = 5 forces B8 = 5, giving (5, 5, 5). Order: A1 through A7, B1, A8, B2, then the rest.
  - A8 = 0 with B8 = 0 is achievable with A3, B1, B2, then A4 through A7 placed before B8. This gives (0, 5, 0).
  - A8 = 0 with B8 = 5 is achievable with A1 through A8, then B1 through B8. This gives (0, 5, 5).
  - A8 = 5 with B8 = 0 is impossible.

BEGIN
0 0 0 0
0 3 0 3
0 5 0 5
0 5 5 5
5 5 5 5
END