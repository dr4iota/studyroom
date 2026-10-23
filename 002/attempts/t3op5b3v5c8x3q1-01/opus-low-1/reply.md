B3 can return 0, 1 or 5. It can never return 4.

**Step 1: What C2 returns.** Only thread C writes to x, with C1 writing 5 and C4 writing 4. C2 runs after C1 and before C4 in C's own order, so C2 always returns 5. That means C5 writes 5 to y.

**Step 2: Which writes to y can come before B3.**
- **A1** writes 1.
- **C5** writes 5.
- **B4** writes 4, but it is in B's own thread after B3, so B3 can never see it.
- **A5** writes whatever A3 returned. A3 runs after A1, so it returns 1 (from A1), 4 (from B4) or 5 (from C5).
  - If A3 returned 4, it read B4's write. B4 comes after B3, and A5 comes after A3, so A5 takes effect after B3. B3 cannot see that 4.
  - Otherwise A5 writes 1 or 5, which are values B3 can already get.

**Step 3: Each remaining value can actually happen.**
- **0:** B3 takes effect before A1 and C5.
- **1:** B3 takes effect after A1 and before C5.
- **5:** B3 takes effect after C5.

BEGIN
0
1
5
END