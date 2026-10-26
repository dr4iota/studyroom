Every execution gives B9 = 0 and a final z of 0. The final x is 1 or 4, and the final y is 1 or 6, in any combination.

**Ordering constraints**
- B1 ends before P, and A2 and everything after it in thread A start after P. So B1 takes effect before A2.
- A1 ends before S, and B5 and everything after it in thread B start after S. So A1 takes effect before B5.
- B2 ends before Q, and A9 starts after Q. B2 therefore precedes A8 and A9, since both come after Q.
- A9 ends before R, and B8 and B9 start after R. So all of thread A's writes to z precede B8 and B9.

**Question by question**
- **B2:** The only write to y is A8, which comes after Q, and B2 ends before Q. So B2 reads 0.
- **B8 and B9:** B8 writes 0 to z after all of A's operations. B9 reads z after B8, and nothing else writes z after R. So B9 returns 0 and the final z is 0 (Q1 and Q4).
- **A4:** Both A1 (writes 6) and B1 (writes 1) take effect before A4, in either order. A4 therefore reads 6 if B1 came first, or 1 if A1 came first.
- **A6 and A7:** A6 writes A4's value v to z. Nothing else can write z before A7, because B1 is before P and B8 is after R. So A7 reads v.
- **A8 and y:** A8 writes v to y, and it is the only write to y. The final y is 1 or 6, and both are possible since A1 and B1 can fall in either order (Q3).
- **Final x:** The last write to x is either B7 (writes 4) or A2 (writes 1). B7 is not constrained by R, so A2 can take effect after B7. The final x is therefore 1 or 4, independent of y (Q2).

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
END