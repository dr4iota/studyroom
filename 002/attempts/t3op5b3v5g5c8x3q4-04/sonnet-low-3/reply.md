Q2 must be 0. If B2 read a nonzero value, A3 would have written it to x, because A3 is the only other writer of x. B3 would then write that same nonzero value, and B4 would read a nonzero value unless a later write overwrote it. The only possible later write is A3, which is already used up. So B2 returns 0.

Q1 and Q3 follow from the other constraints:

- **C2 before C3:** z goes 0 → 5 → 1, so it only ever holds 0, 5 or 1. A1 and A4 read one of those, and a1 below means the value A1 reads.
- **Nonzero a1:** C4 reads 0, so A3 must take effect after C4. C4 is after C3, which has already set z to 1. Then A4 is after A3, so A4 returns 1.
- **a1 = 0:** A3 writes 0, which breaks nothing. A4 can return 0, 5 or 1.
- **A4 = 1:** A4 is after C3, which is after C1. A5 follows A4, so A5 is after C1 and the final y is 3.
- **A4 = 0 or 5:**
  - If A5 comes before C1, the final y is 4.
  - If A5 comes after C1, the final y is 3.
  - Both orders are possible.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END