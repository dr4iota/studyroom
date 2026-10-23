**Possible values of C2: 0 and 5.**

1. **Values y can hold.** The writes to y are A1 (5), B1 (5) and A3, which writes whatever A2 read from z. The writes to z are B3 (2) and C3, which writes C1's value, 0. So A2 returns 0 or 2, and C2 can only see 0, 5, or A2's value.

2. **How A4 can return 5.** A3 takes effect after A1 and before A4, and A3 writes 0 or 2, never 5. So a write of 5 must land between A3 and A4. A1 comes before A3, so that write has to be B1. Therefore B1 takes effect after A3.

3. **A2 cannot return 2.** If A2 returned 2, then B3 took effect before A2. B1 comes before B3 in thread B, so B1 < B3 < A2 < A3 < B1. That is a contradiction. So A2 returns 0, and A3 writes 0.

4. **Each remaining value has a valid execution.**
   - **C2 = 0:** C1 reads z = 0 and C2 reads y, both before A1 and B1. Then A1, A2 (z = 0), A3 (y = 0), B1 (y = 5), A4 reads 5, and B2, B3, C3, B4, C4 follow in any order.
   - **C2 = 5:** C1 first, then A1 (y = 5), then C2 reads 5. Then A2 (z = 0), A3 (y = 0), B1 (y = 5), A4 reads 5, and the rest follow.

C2 cannot be 2, because y never holds 2.

BEGIN
0
5
END