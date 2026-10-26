Each operation takes effect at a single instant, so an execution is a total order of all operations that keeps each thread's program order.

**Constraints**
- A2 returns 1. Only B1 or B4 (with B4 writing 1) can write 1 to y before A2, and A4 writes 3 after A2. B1 precedes B4 anyway, so B1 < A2 in every case.
- Thread A's order is A1 < A2 < A3 < A4 < A5 < A6.
- Thread B's order is B1 < B2 < B3 < B4 < B5.

**Q1: A5**
- A1 is always overwritten by A3 before A5.
- So A5 reads either A3's value 2 or B5's value b3, if B5 falls between A3 and A5.

**Q3: final y**
- The final y is 3 if A4 is the last write to y.
- Otherwise it is b2, the value B2 read, written by B4 after A4.

**Case B3 = 0**
- B3 precedes A1, so b2 = 0 and b3 = 0.
- A5 is 2 or 0. A5 = 0 needs B5 between A3 and A5.
- B4 writes 0, so it must come after A2. The final y is 0 or 3.
- This gives A5 ∈ {0, 2} and y ∈ {0, 3}: four combinations.

**Case B3 = 1**
- B3 reads A1's write, so A3 comes after B3.
- b3 = 1, so A5 is 1 or 2.
- b2 is 0 or 1, so the final y is 3, 0 or 1. All of these are achievable.
- This gives A5 ∈ {1, 2} and y ∈ {0, 1, 3}: six combinations.

**Case B3 = 2**
- A3 comes before B3, and b3 = 2, so A5 = 2.
- b2 can be 0, 1 or 2, so the final y is 0, 1, 2 or 3.
- This gives four combinations.

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