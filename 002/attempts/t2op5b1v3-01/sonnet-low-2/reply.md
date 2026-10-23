Neither thread has sync points, so every interleaving that preserves each thread's own order is allowed.

**Q1 (A1):** A1 runs before A3 and A4, so it cannot see 2 or 3. The only other writes are B's writes of 1, so A1 is 0 or 1. Both are always possible, because A1 can be placed before or after B1 without affecting the other reads.

**Q2 (B3):** B1 has already taken effect, so B3 sees the last write, which is 1, 2 or 3.
- B3 = 1: B1 is the last write before it, or B1 overwrote earlier A writes.
- B3 = 2: A3 has taken effect and A4 has not.
- B3 = 3: A3 and A4 have both taken effect.

**Q3 (B5):** B4 has written 1 before B5, so B5 depends on A writes landing after B4.
- B5 = 1 is possible whenever no A write falls between B4 and B5.
- B5 = 2 needs A3 between B4 and B5 and A4 after B5. That forces B3 = 1, since A3 has not happened before B3.
- B5 = 3 needs A4 between B4 and B5.

**Combined with B3:**
- B3 = 1: B5 can be 1, 2 or 3.
- B3 = 2: A3 is already done, so B5 = 2 is impossible. B5 can be 1 or 3.
- B3 = 3: both A writes are done before B3, so only B4's write remains. B5 = 1.

A1 can be 0 or 1 in every case. That gives 6 + 4 + 2 = 12 combinations.

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