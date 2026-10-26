These are all 22 combinations of (A1, B4, C4) that can happen. I found them by checking where each read can get its value. There are no sync points, so any interleaving that keeps each thread's own order is allowed.

**Q1: what A1 can return.** A1 reads x, and A5 comes after A1 in thread A, so A5 cannot affect it.
- A1 = 0 if it runs before both B2 and C1.
- A1 = 1 if it reads the value B2 wrote.
- A1 = 2 if it reads the value C1 wrote.

Let a be the value A1 returned. A3 writes a to y.

**Q2: what B4 can return.** B4 runs after B3, which writes 1 to y. So B4 sees B3 or a later write to y:
- 1 from B3 or C3,
- a from A3,
- 3 from A4,
- 2 from C2,
- whatever C4 returned, if C5 runs before B4.

So B4 can be 1, 2, 3 or a. C5 only copies a value that is already in this set.

**Q3: what C4 can return.** C4 runs after C3, which writes 1 to y. So C4 sees C3 or a later write to y:
- 1 from C3 or B3,
- a from A3,
- 3 from A4 or B1,
- whatever B4 returned, if B5 runs before C4.

C2 always comes before C3, so C4 can never read C2's 2. That means C4 can be 2 only if A1 = 2 (through A3) or B4 = 2 (through B5).

**Can these choices be combined?** Yes. All the write events can be placed freely, as long as each thread keeps its own order. Both reads can see the same write, or different writes, as needed. The two copies cannot depend on each other in a loop: C4 → C5 → B4 → B5 → C4 would be impossible, but each combination needs at most one copy.

Some checks on the less obvious cases:
- (0, 2, 2): A1 runs first. C2 runs after B3 and B4 reads its 2. Then C3 runs, then B5 writes 2, then C4 reads 2.
- (0, 0, 0): A3 writes 0 after both B3 and C3, and both B4 and C4 then read it.
- (2, 1, 2): B4 reads 1. Later A3 writes 2 after C3, and C4 reads it.

**Combinations:**
- A1 = 0: B4 can be 0, 1, 2 or 3. C4 can be 0, 1 or 3, and also 2 when B4 = 2.
- A1 = 1: B4 can be 1, 2 or 3. C4 can be 1 or 3, and also 2 when B4 = 2.
- A1 = 2: B4 and C4 can each be 1, 2 or 3, in any pair.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 3
1 1 1
1 1 3
1 2 1
1 2 2
1 2 3
1 3 1
1 3 3
2 1 1
2 1 2
2 1 3
2 2 1
2 2 2
2 2 3
2 3 1
2 3 2
2 3 3
END