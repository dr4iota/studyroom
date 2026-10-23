Every operation here is a plain read or write with no sync points, so the possible outcomes are exactly the sequential interleavings of the two threads. Reads and writes of x and y don't affect z, so only the z operations matter.

**Q3 (final z):** The last write to z is either A5 (value 2) or B5 (value 1). Both can come last.

**Q2 (B4):** B4 runs after B3 and before B5. B5 is the only write of 1, so B4 can't return 1. It returns whichever write came last before it:
- B3 gives 2.
- A3 gives 3.
- A4 gives 4.
- A5 gives 2.

So B4 can be 2, 3 or 4.

**Q1 (A1):** A1 is A's first operation, so only B's writes can precede it. It can return 0 (before B1), 3 (after B1), 2 (after B3) or 1 (after B5).

**Combinations:**
- **A1 = 0, 3 or 2:** B4 can be 2, 3 or 4, and the final value can be 1 or 2. A3, A4 and A5 can each be placed before or after B4 and B5 as needed. For example, A1 = 0, B4 = 4, final = 2 comes from A1, B1, B2, B3, A3, A4, B4, B5, A5. That gives 3 × 3 × 2 = 18 combinations.
- **A1 = 1:** A1 must come after B5, so B4 has already run. A hasn't written yet, because A1 precedes A3, so B4 reads 2 from B3. A5 then comes last, so the final value is 2. This gives one combination, (1, 2, 2).

BEGIN
0 2 1
0 2 2
0 3 1
0 3 2
0 4 1
0 4 2
3 2 1
3 2 2
3 3 1
3 3 2
3 4 1
3 4 2
2 2 1
2 2 2
2 3 1
2 3 2
2 4 1
2 4 2
1 2 2
END