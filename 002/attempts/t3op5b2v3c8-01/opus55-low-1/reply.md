All 27 combinations are possible: every value of A1 from {0, 2, 3} pairs with every value of A2 and A3 from {0, 2, 3}. There are no sync points or known results, so any interleaving that keeps each thread's own order counts.

**Values each block can hold**
- **y** can hold 0, 3 (from B2), 2 (from B3), or whatever C4 copies from C3. C4 copies 0, 3 or 2.
- **x** can hold 0, 3 (from B1), whatever C2 copies from C1, or whatever B5 copies from B4.
  - C2 copies 0 (C1 runs before B1), 3 (C1 runs after B1), or B5's value.
  - B4 runs after B3, so it reads 2, or the 0, 3 or 2 that C4 wrote later. So B5 can write 2, 3 or 0.

**Why x stays flexible after A1, whatever A1 reads**
- If A1 reads 2 or 3, then B2 (and for 2, also B3) has already happened, so B1 is done and x has been 3.
- C2 can still be delayed until after A1, writing 0 if C1 ran before B1, or 3 if C1 ran after B1.
- B5 can still be pending and write 2, 3 or 0.
- So after A1, x can move through these values in any order needed. A2 and A3 can each read 0, 2 or 3.

**Example orders**
- **A1=3, A2=0, A3=3:** C1(read 0), B1, B2, A1(read 3), C3(read 3), C2(write 0), A2(read 0), B3, C4(write 3), B4(read 3), B5(write 3), A3(read 3).
- **A1=2, A2=3, A3=0:** C1(read 0), B1, B2, B3, A1(read 2), A2(read 3), C2(write 0), A3(read 0).
- **A1=0, A2=2, A3=3:** A1(read 0), B1, C1(read 3), B2, B3, B4(read 2), B5(write 2), A2(read 2), C2(write 3), A3(read 3).

The remaining combinations come from similar orderings.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END