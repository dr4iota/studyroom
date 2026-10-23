**Approach.** There are no sync points, so any interleaving that keeps each thread's order is allowed. I first find what A1 can return, then check the constraint on B3, then list the orderings of the writes to y.

**What A1 can return.** A1 runs before A2, so it cannot see A2's write. It returns the last write to x before it: 0 (none yet), 1 (from B1) or 3 (from B2). Call this value v.

**The constraint "B3 returned 3".** The last write to x before B3 must be B2 or A5. That means A2 cannot fall between B2 and B3, unless A5 also comes after A2 and before B3. This constraint never removes a whole value of v:
- If v = 0 or 1, A2 can run before B2. After that, A3 and A4 can be placed freely against B4–B6.
- If v = 3, A1 runs after B2. B3 can still run between A1 and A2, which again leaves A3 and A4 free against B4–B6.

**Writes to y.** A3 writes v, B5 writes 2, and B6 writes whatever B4 read.
- B4 reads 0 if it runs before A3, and v if it runs after A3.
- If B4 runs after A3, then B6 also writes v.
  - The final value of y is v.
  - A4 returns 2 if it falls between B5 and B6, and v otherwise.
  - This gives (v, v, v) and (v, 2, v).
- If B4 runs before A3, then B6 writes 0. Then:
  - A3 before B5, A4 before B5: A4 = v, final y = 0.
  - A3 before B5, A4 between B5 and B6: A4 = 2, final y = 0.
  - A3 before B5, A4 after B6: A4 = 0, final y = 0.
  - A3 between B5 and B6, A4 before B6: A4 = v, final y = 0.
  - A3 between B5 and B6, A4 after B6: A4 = 0, final y = 0.
  - A3 after B6: A4 = v, final y = v.
- So the new combinations are (v, v, 0), (v, 2, 0) and (v, 0, 0).

**Result.** For v = 0, (0, v, 0) and (0, 0, 0) are the same combination, so there are two outcomes. For v = 1 and v = 3 there are five each.

BEGIN
0 0 0
0 2 0
1 1 1
1 2 1
1 1 0
1 2 0
1 0 0
3 3 3
3 2 3
3 3 0
3 2 0
3 0 0
END