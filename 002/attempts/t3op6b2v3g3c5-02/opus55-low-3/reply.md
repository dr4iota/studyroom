**B1 always returns 0.** The only writes to x are A3 and B3. Each of them writes a value that was read from x, and x starts at 0, so x is 0 at every moment. That makes A1 and B1 both return 0, and B4 returning 0 always holds.

**Writes to y, with their values:**
- C1 writes 2.
- A4 writes 3.
- A5 writes the value read by A1, which is 0.
- B5 writes 1.
- C4 and C6 write the value read by C3.
- C5 writes 2.

**What A2 returning 2 requires.** A2 runs before A4 and A5 in thread A. C3 runs before C4, C5 and C6 in thread C, so those three writes cannot affect what C3 returns.
- If C3 returns 2, the only 2 that can be in y before C3 is C1's. A2 can then read 2 from C1, or later from C4, C5 or C6.
- If C3 returns 0, 1 or 3, A2 can read 2 from C1, placing A2 after C1 and before A4.

**Q2 (B2) can be 0, 2 or 3, but not 1.**
- B2 runs before B5 in thread B, so B2 cannot see B5's 1.
- The only other way y holds 1 is through C4 or C6 copying a 1 that C3 read. C3 can only read 1 after B5, which is after B2, so B2 cannot see that either.

**Q3 (C3) can be 0, 1, 2 or 3.** Every pairing with B2 = 0, 2 or 3 works:
- **C3 = 0:** use the order C1, A2, A4, A5, C3. B2 reads 0 if it runs before C1, 2 if it runs between C1 and A4, or 3 if it runs between A4 and A5.
- **C3 = 1:** use the order C1, A2, then B2, then B5, C3. B2 can read 0 (if placed before C1), 2 (after C1), or 3 (after A4, if A4 is placed before B2).
- **C3 = 2:** use the order C1, C2, C3 with no other write to y between C1 and C3. B2 reads 0 if it runs before C1, or 2 if it runs right after C1. For B2 = 3, use C1, C2, C3, A2, A4, B2.
- **C3 = 3:** C3 runs after A4 and before A5 and B5. B2 can read 0 (before C1), 2 (after C1, before A4), or 3 (after A4).

So there are 3 × 4 = 12 combinations, with Q1 always 0.

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