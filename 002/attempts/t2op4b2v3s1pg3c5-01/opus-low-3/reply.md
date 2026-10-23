A2 can read 0, 3, 2 or 1, and A3 can only return the value A2 saw or a later write. The final value of x is either A4's write or B4's 1.

**Timing constraints**
- B1 and B2 finish before P, and A2 ends after P.
- A2's start has no constraint, so A2 can take effect at any time before it ends. That includes before B2.
- B3 and B4 have no constraint relative to P. They only have to follow B2 in B's order.
- The writes to x take effect in the order B2 (3), then B3 (2), then B4 (1). A4 writes the value A3 read, and it takes effect after A3.

**Q1 (A2):** A2 can take effect before B2, between any two of B's writes, or after B4. So it can return 0, 3, 2 or 1.

**Q2 (A3):** A3 takes effect after A2. It returns the value A2 saw or the value of a later write.
- If A2 = 0, A3 can be 0, 3, 2 or 1.
- If A2 = 3, A3 can be 3, 2 or 1.
- If A2 = 2, A3 can be 2 or 1.
- If A2 = 1, A3 must be 1.

**Q3 (final x):** A4 writes A3's value v.
- If A4 takes effect after B4, the final value is v.
- If A4 takes effect before B4, B4 overwrites it and the final value is 1.
- If A3 read 1, B4 has already happened, so the final value is 1.

So the final value is v or 1 when v is 0, 3 or 2, and it is 1 when v = 1.

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END