All 27 combinations of (A1, A2, A3) are possible. There are no sync points, so the only ordering limits are each thread's own program order and that each read returns the latest write before it.

**Which values each block can hold**
- **y:** B2 writes 3, then B3 writes 2. C4 writes back whatever C3 read, which is 0, 3 or 2. So A1 can return 0, 3 or 2.
- **x:** B1 writes 3. C2 writes back whatever C1 read, which is 0 or 3. B5 writes whatever B4 read from y. B4 runs after B3, so it reads 2, or 3 if C4 wrote back a 3. So x can hold 0, 3 or 2 at different times.

**Every ordered pair (A2, A3) is reachable**
- **Going down to 0 later:** C1 reads 0 before B1, and C2 writes that 0 back later. This gives 3→0 and 2→0.
- **Going up to 2 later:** B4 reads 2 and B5 writes it to x. This gives 0→2 and 3→2.
- **Going from 2 to 3:** C1 reads 3 after B1, and C2 writes 3 after B5 has written 2.
- **Repeats and 0→3:** pairs with the same value twice, and 0→3, are also easy to arrange.

**A1 can be anything, whatever A2 and A3 return**
- **A1 = 0:** A1 runs before everything else. All later x values are still reachable.
- **A1 = 3 or 2:** A1 runs after B2 or B3, and x can still go through any pair afterward. The hardest case is A2 = 0 then A3 = 3. One valid order:
  C1(0), B1, B2, C2(writes 0), C3(reads 3), B3, A1(2), A2(0), C4(writes 3), B4(reads 3), B5(writes 3), A3(3).
  For A1 = 3, place A1 before B3 instead.

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