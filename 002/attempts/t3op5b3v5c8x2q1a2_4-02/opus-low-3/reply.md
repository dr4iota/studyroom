**Q1 (the value returned by A2) can be 0 or 4.**

1. **Where A2's value can come from.** Three things could set x before A2 reads it:
   - A4 writes x, but it comes after A2 in thread A, so A2 can never see it.
   - Nothing has written x yet, so A2 reads **0**.
   - C5 writes x with whatever C4 read from y.

2. **What C4 can read from y.** C1 wrote 4 to y earlier in thread C, so C4 cannot see the initial 0. C4 reads either C1's value **4**, or B4's write, which is whatever B3 read from x.

3. **What B3 can read from x, when the chain C5 → A2 matters.**
   - If B3 read A4's write, the order would have to be A4 → B3 → B4 → C4 → C5 → A2. But A2 comes before A4 in thread A, so this is a cycle and is impossible.
   - If B3 read C5's write, C5 would have to happen before C4, which comes earlier in thread C. Also a cycle.
   - So B3 reads 0, B4 writes 0, C4 reads 0, and C5 writes 0. This only gives A2 = 0 again.

4. **Showing 4 can happen.** One valid run: C1 writes 4 to y. C4 reads 4. C5 writes 4 to x. Then A2 reads 4.

BEGIN
0
4
END