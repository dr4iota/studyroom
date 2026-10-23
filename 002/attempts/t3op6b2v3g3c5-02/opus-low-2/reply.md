**Answer: B1 always returns 0. B2 can return 0, 2 or 3. C3 can return 0, 1, 2 or 3. Every pairing of these is possible, giving 12 combinations.**

**Block x is always 0.**
- Only A3 and B3 write to x. They write the values that A1 and B1 read from x.
- x starts at 0. So the first write to x can only write 0, and by induction every later write to x also writes 0.
- Therefore A1 and B1 both return 0, and B4 returning 0 is always satisfied. **Q1 = 0.**

**Writes to y and their values:**

| Write | Value |
|---|---|
| C1 | 2 |
| C5 | 2 |
| C4, C6 | whatever C3 returned |
| A4 | 3 |
| A5 | 0 (A1's value) |
| B5 | 1 |

A2 must return 2. That only requires C1 (or C5) to take effect before A2, which is easy to arrange.

**Q3 (C3).** C3 happens after C1, so it can see any write to y that takes effect between C1 and C3:
- **2:** C1 is the last write before C3.
- **3:** order C1, A2, A4, C3.
- **0:** order C1, A1–A5, C3. A2 reads 2 from C1, then A5 writes 0.
- **1:** B5 takes effect before C3.

**Q2 (B2).**
- **0:** B2 takes effect before C1.
- **2:** B2 reads C1's value.
- **3:** B2 takes effect after A4.
- **1 is impossible.** It would need B5 or C4 writing 1 before B2. But B5 comes after B2 in thread B. C4 can only write 1 if C3 read 1, which requires B5 first, which again comes after B2.

**Combining Q2 and Q3.** Every pairing works. B2 can always be placed in the right spot without blocking the order that gives C3 its value. Example for the trickiest pair, B2=3 and C3=1: C1, A2, A4, B2 (reads 3), B5, C3 (reads 1).

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END