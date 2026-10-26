**Approach.** There are no sync points, so any interleaving that keeps each thread's order is allowed. I first find which values each write can carry, then check each combination.

**What can be written.**
- The writes to y are A1 (1) and B1 (2).
- B2 reads y after B1, so b, the value B2 returns, is 1 or 2.
  - b = 1 when A1 falls between B1 and B2.
  - b = 2 otherwise.
- C1 reads x, so c, the value C4 writes, is 0, 2 or b.
- C2 returns:
  - 0 if it runs before A1 and B1;
  - 2 if it runs after B1 and before A1, or when y ends up holding 2;
  - 1 if it runs after A1 and A1 is the last y write before it.
- A3 runs after A2, so it returns 2, b or c, whichever x write took effect last before it.
- The final x is the value of the last write among A2, B4 and C4.

**Final x = 0.** C1 must run before both A2 and B3, and C4 must be the last x write. Because C1 can be scheduled at the very start, C2 can be placed to read 0, 1 or 2. A3 can return:
- 0, if C4 lands between A2 and A3;
- 1, if b = 1 and B3 lands between A2 and A3, with C4 after A3;
- 2, if A3 runs before any later x write.

So every A3 value combines with every C2 value.

**Final x = 1.** Here b = 1 and the last write is B4, or C4 with c = 1. All values of A3 (0, 1, 2) and C2 (0, 1, 2) are reachable. For example, A3 returns 0 if C4 writes 0 between A2 and A3 and B4 comes afterwards.

**Final x = 2.**
- A3 = 2: every C2 value works.
- A3 = 0: works with every C2 value. An example for C2 = 2 is: C1, A1, B1, C2, C3, A2, C4, A3, B2, B3, B4.
- A3 = 1: this needs b = 1, and the final 2 must come from C4 with c = 2. That means C1 ran after A2, and so after A1. Since b = 1 requires B1 to come before A1, C2 must return 1. So C2 = 0 and C2 = 2 are impossible here.

**Summary.** All 27 combinations are possible except (A3=1, C2=0, final 2) and (A3=1, C2=2, final 2), which leaves 25.

BEGIN
0 0 0
0 1 0
0 2 0
0 0 1
0 1 1
0 2 1
0 0 2
0 1 2
0 2 2
1 0 0
1 1 0
1 2 0
1 0 1
1 1 1
1 2 1
1 1 2
2 0 0
2 1 0
2 2 0
2 0 1
2 1 1
2 2 1
2 0 2
2 1 2
2 2 2
END