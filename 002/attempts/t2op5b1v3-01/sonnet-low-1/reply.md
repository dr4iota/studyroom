With no sync points, the two threads can interleave freely, so I enumerated every interleaving of A1–A4 with B1–B5.

**Q1 (A1).** A1 is the first operation of thread A, so it runs before A3 and A4. It can only see 0 (before B1) or 1 (after B1). It cannot see 2 or 3.

**Q2 and Q3 (B3, B5).** B3 comes after B1, so it sees 1, 2 or 3. B5 comes after B4, so it also sees 1, 2 or 3.

- B3=2 needs A3 before B3 and A4 after B3.
- B3=3 needs A4 before B3.
- B5=1 needs no A write between B4 and B5.
- B5=2 needs A3 between B4 and B5, with A4 after B5.
- B5=3 needs A4 between B4 and B5.

Checking each pair (B3, B5):
- (1,1), (1,2), (1,3): possible.
- (2,1): possible. A3 before B3, and A4 either before B4 or after B5.
- (2,2): impossible. B3=2 needs A3 before B3, but B5=2 needs A3 after B4.
- (2,3): possible.
- (3,1): possible. A4 comes before B3, and B4 then rewrites 1.
- (3,2) and (3,3): impossible. B3=3 needs A4 before B3, which rules out A3 or A4 landing after B4.

So the valid (B3, B5) pairs are (1,1), (1,2), (1,3), (2,1), (2,3) and (3,1).

**Combining with A1.** For each valid pair, A1 can be 0 by placing A1 first, and 1 by placing A1 after B1 and before A3. So every pair works with both values of A1.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END