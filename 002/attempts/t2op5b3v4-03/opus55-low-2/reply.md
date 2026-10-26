There are no sync points, so any interleaving that keeps each thread's own order is allowed. All 3 × 2 × 2 = 12 combinations are possible.

**Q1 (A1 reads z).** A1 is Thread A's first operation, so A's own writes to z (A2, A3) cannot come before it. Only B's writes to z can precede it.
- 0 if A1 takes effect before B1.
- 3 if A1 takes effect after B1 but before B3.
- 2 if A1 takes effect after B3.

**Q2 (A5 reads y).** Only B5 writes y.
- 0 if A5 takes effect before B5.
- 4 if A5 takes effect after B5.

**Q3 (B4 reads x).** Only A4 writes x.
- 0 if B4 takes effect before A4.
- 1 if B4 takes effect after A4.

**These choices can be combined freely.** Program order gives A4 < A5 and B4 < B5. Every pairing of Q2 and Q3 has a valid ordering:
- (4, 0): B4 < A4 < B5 < A5.
- (4, 1): A4 < B4 < B5 < A5.
- (0, 0): B4 < A4 < A5 < B5.
- (0, 1): A4 < B4 < A5 < B5.

The Q1 choice only fixes where A1 sits relative to B1 and B3. A1 comes before all of A2–A5, and B1 and B3 come before B4 and B5. So A1 can be placed in the chosen position, and any of the four orderings above can follow it.

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