Each operation takes effect at a single instant, so the possible executions are the interleavings of the two threads that keep each thread's order. The only extra constraint is that A2 reads y = 1. Because A4 comes after A2, that 1 must come from B1, or from B4 after B2 read 1.

B2 can read 0, 1 or 2. B5 writes B3's value to x. The final y is 3 if A4 is the last write to y. Otherwise it is B2's value, which needs B4 after A4.

**B3 = 0**
- B2 must also be 0, since both reads come before A1.
- A5 can be 0, if B5 writes 0 after A3 and before A5. It can also be 2, if B5 comes after A5 or A3 is the last write.
- y can be 0 (B4 after A4) or 3.
- All four combinations of A5 ∈ {0, 2} and y ∈ {0, 3} are achievable.

**B3 = 1**
- B2 is 0 or 1.
- A5 can be 1, if B5 writes 1 after A3 and before A5. It can also be 2.
- y can be 0 (B2 = 0), 1 (B2 = 1) or 3.
- All six combinations of A5 ∈ {1, 2} and y ∈ {0, 1, 3} are achievable. For example, A5 = 1 with y = 0 follows B1, B2 (0), A1, A2, B3 (1), A3, A4, B4, B5, A5.

**B3 = 2**
- A3 must come before B3, so every write to x that could be last is 2, and A5 = 2.
- B2 can be 0, 1 or 2, so y can be 0, 1, 2 or 3.

BEGIN
0 0 0
0 0 3
2 0 0
2 0 3
1 1 0
1 1 1
1 1 3
2 1 0
2 1 1
2 1 3
2 2 0
2 2 1
2 2 2
2 2 3
END