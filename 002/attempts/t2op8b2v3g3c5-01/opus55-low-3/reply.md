Every execution is a single ordering of all operations by the instants at which they take effect.

**1. A3 sits after B1.** A3 returned 2. Only B1 or B3 can put 2 into x, and A's own writes come after A3. So A3 takes effect after B1, and therefore after B1 as the first 2 written to x.

**2. Values of y over time.** y starts at 0. It becomes 2 at B2, stays 2 through B4, and becomes 1 at B7. So y goes through 0, then 2, then 1, in that order.

**3. Q1 and Q2 (A2 and A4).** A2 can return 0, 2 or 1. A4 comes later than A2, so its value can only be the same or later in the sequence 0 → 2 → 1. That gives six possible pairs: (0,0), (0,2), (0,1), (2,2), (2,1), (1,1).

None of these choices conflicts with A3. Any orderings that satisfy the y values can also place B1 before A3. For example, A2 = A4 = 0 works with A1, A2, B1, A3, A4, B2, … in that order.

**4. Q3 (final x).** The last write to x is B3 (value 2), A5, A6 or A7. A5, A6 and A7 write what A1 read.
- A1 reads either 0 (before B1) or 2 (after B1). So the final x is 0 or 2.
- **Final x = 0** needs A1 to take effect before B1 and A7 to come after B3. A7 already follows A4, so this works with each of the six (A2, A4) pairs. For example, with A2 = 1: A1, B1, B2, B3, B4, B5, B6, B7, A2, A3, A4, A5, A6, A7.
- **Final x = 2** is always possible. Let A1 read 2, or let A5–A7 all take effect before B3.

That gives 6 × 2 = 12 combinations.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END