Block x always holds 0, so B1 always returns 0. Every write to x writes a value read from x, and by induction that value is 0.

Block y has these writes: C1 writes 2, A4 writes 3, A5 writes 0 (the value A1 read), B5 writes 1, C5 writes 2, and C4 and C6 copy C3's value. A2 must return 2, so a 2 is written before A2, and A4 and A5 come after A2.

**B2 can be 0, 2 or 3, but not 1.**
- The only source of a 1 is B5, which comes after B2. C4 and C6 can copy a 1 only after C3 has read it, which itself needs B5 first.
- Reading 0 is possible before C1, or after A5.
- Reading 2 is possible after C1.
- Reading 3 is possible after A4.

**C3 can be 0, 1, 2 or 3, and each pairs with every possible B2.**
- 0 comes from A5 after A2.
- 1 comes from B5 after B2.
- 2 comes from C1 or C5.
- 3 comes from A4.

One example schedule for each of the four C3 values with B2=0:
- B2 reads 0, then C1, A2, A4, A5, then C3 reads 0.
- B2 reads 0, then C1, A2, B5, then C3 reads 1.
- B2 reads 0, then C1, then C3 reads 2.
- B2 reads 0, then C1, A2, A4, then C3 reads 3.

For B2=2 and B2=3, the same four C3 values are reached by placing the needed write after B2. For B2=3, A4 has already happened, and C5 can restore 2.

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END