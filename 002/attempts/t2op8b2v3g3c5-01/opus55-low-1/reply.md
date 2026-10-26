No sync points are used here, so every interleaving of the two threads' steps is allowed, as long as A3 reads x = 2.

**Constraint from A3.** A3 returned 2, so B1 (write 2 to x) takes effect before A3.

**Q3 (final x).**
- A1 returns 0 if it runs before B1, or 2 if it runs after B1. A5, A6 and A7 all write that value to x.
- The last write to x is either A7 or B3. If B3 is last, x ends at 2. If A7 is last, x ends at A1's value, which is 0 or 2.
- So the final x can be 0 or 2.

**Q1 and Q2 (A2 and A4).** The writes to y happen in the order 2 (B2), 2 (B4), 1 (B7). Starting from 0, y takes the values 0 → 2 → 2 → 1. Since A4 runs after A2, A4 sees the same value as A2 or a later one in that sequence.

- **A2 = 1:** B1 through B7 all take effect before A2, including B3. A5–A7 come after B3, so x ends at A1's value. A1 can run before B1 (giving 0) or after it (giving 2). A4 must be 1. Results: (1,1,0), (1,1,2).
- **A2 = 2:** A4 can be 2 or 1.
  - If A4 = 2, B3 can come after A7, giving final x = 2. Otherwise x ends at A1's value, 0 or 2.
  - If A4 = 1, B7 is before A4, so B3 is too. Then x ends at A1's value, 0 or 2.
  - Results: (2,2,0), (2,2,2), (2,1,0), (2,1,2).
- **A2 = 0:** A4 can be 0, 2 or 1.
  - If A4 = 0, B2 comes after A4, so B3 does too. B3 can then fall before A5 (x ends at 0 when A1 = 0) or after A7 (x ends at 2).
  - If A4 = 2 or A4 = 1, both final values 0 and 2 are reachable in the same ways.
  - Results: (0,0,0), (0,0,2), (0,2,0), (0,2,2), (0,1,0), (0,1,2).

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END