Each operation takes effect at a single instant, so the possible outcomes are the sequentially consistent interleavings of the two threads' operations.

**Q1 (A1 reads z).** Thread A's own writes to z (A2, A3) come after A1, so only thread B's writes can affect it. B writes 3 (B1) and then 2 (B3). So A1 can return 0 (before B1), 3 (after B1, before B3), or 2 (after B3). It cannot return 4.

**Q2 (A5 reads y).** The only write to y is B5, which writes 4. So A5 returns 0 if it takes effect before B5, or 4 if after.

**Q3 (B4 reads x).** The only write to x is A4, which writes 1. So B4 returns 0 if it takes effect before A4, or 1 if after.

**Checking that all 12 combinations are achievable.** The three answers are almost independent, since the ordering constraints can all be satisfied together.
- B4 = 1 needs A4 < B4. B5 comes after B4, so B5 is after A4.
- A5 = 4 needs B5 < A5. With B4 = 1 this gives A4 < B4 < B5 < A5, which is consistent.
- A5 = 0 needs A5 < B5. With B4 = 1 the order A4 < A5 < B4 < B5 works, since A5 only needs to come after A4 and before B5.
- A1 = 2 needs B3 < A1. Since A1 < A2 < A3 < A4, this also works with B4 = 1, for example B1 < B2 < B3 < A1 < ... < A4 < B4. With B4 = 0, B4 < A4 and B3 < B4 still leave room for A1 between B3 and A4.
- A1 = 0 and A1 = 3 are placed before B1 or between B1 and B3, which constrains nothing else.

So every combination of A1 ∈ {0, 2, 3}, A5 ∈ {0, 4}, B4 ∈ {0, 1} is possible.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
2 0 0
2 0 1
2 4 0
2 4 1
3 0 0
3 0 1
3 4 0
3 4 1
END