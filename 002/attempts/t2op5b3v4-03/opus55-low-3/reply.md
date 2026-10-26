Every combination of the three values is possible, giving 12 outcomes. There are no sync points, so any interleaving that keeps each thread's own order is allowed.

**Q1 (value returned by A1).** A1 is thread A's first operation, so A's own writes to z (A2, A3) come after it. Only B's writes to z can come before it: B1 writes 3, then B3 writes 2.
- A1 takes effect before B1: it returns 0.
- A1 takes effect between B1 and B3: it returns 3.
- A1 takes effect after B3: it returns 2.

**Q2 (value returned by A5).** The only write to y is B5, which writes 4. A5 returns 4 if it takes effect after B5, otherwise 0.

**Q3 (value returned by B4).** The only write to x is A4, which writes 1. B4 returns 1 if it takes effect after A4, otherwise 0.

**Do the choices interfere?** Only the relative order of A4 and A5 against B4 and B5 matters for Q2 and Q3. All four orders are consistent with each thread's sequence:
- A5 = 4 and B4 = 1: A4 < B4 < B5 < A5.
- A5 = 4 and B4 = 0: B4 < A4, and B5 < A5.
- A5 = 0 and B4 = 1: A4 < B4, and A5 < B5.
- A5 = 0 and B4 = 0: B4 < A4, and A5 < B5.

Each of the three placements of A1 only fixes A1 relative to B1–B3. That happens before A4/A5 and does not constrain B4/B5. So each value of A1 combines with all four (A5, B4) pairs.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
3 0 0
3 0 1
3 4 0
3 4 1
2 0 0
2 0 1
2 4 0
2 4 1
END