All 12 combinations of (A3, B4, final x) are possible: A3 and B4 can each be 0 or 3, and x can be 0, 1 or 3, independently.

**What values can appear?**
- Block y is written by A1 (3), B3 (the value B2 read) and C4 (the value C1 read).
- C1 can only read 0, 3, or B3's value. B2 can only read 0, 3, or C4's value.
- They cannot read from each other in both directions. That would need B3 < C1 < C4 and C4 < B2 < B3, which is a cycle.
- So C1 and B2 each return 0 or 3, and every write to y stores 0 or 3. A3 and B4 are therefore 0 or 3.
- Block x is written by B1 (1) and C3 (C1's value). So the final x is 1, 0 or 3.

**Case: C1 and B2 both read 0.** Then A1 is the only write of 3, and x can end as 0 or 1 by ordering B1 and C3 either way.
- A3 = 3, B4 = 3: C1, B2, B3, C4, A1, A2, A3, B4.
- A3 = 0, B4 = 3: B1, B2, C1, B3, A1, B4, C4, A2, A3. B4 sees A1; A3 sees C4's 0.
- A3 = 3, B4 = 0: A1, A2, A3, then C4, then B4, with B3 earlier. B4 sees C4's 0.
- A3 = 0, B4 = 0: both reads come after A1 and after a later write of 0.

This gives all four (A3, B4) pairs with x = 0 and with x = 1.

**Case: final x = 3.** This needs C1 to read 3 and C3 to come after B1.
- Example with A3 = 0 and B4 = 0: B1, B2 (reads 0), A1, C1 (reads 3), C2, C3, C4, B3 (writes 0), A2, A3, B4.
- The pairs involving 3 are just as easy to arrange.

So all four (A3, B4) pairs also occur with x = 3.

BEGIN
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 0 0
3 0 1
3 0 3
3 3 0
3 3 1
3 3 3
END