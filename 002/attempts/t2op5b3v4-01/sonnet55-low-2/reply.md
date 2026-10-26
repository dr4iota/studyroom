Every operation takes effect at a single instant, so the possible outcomes are exactly those of the interleavings of the two threads' operation sequences. The reads of x (A2) don't affect z.

**Q1 (A1):** A1 is Thread A's first operation, so only Thread B's writes can come before it. It can return 0 (before any B write), 3 (after B1), 2 (after B3), or 1 (after B5).

**Q2 (B4):** B4 comes after B3 (writes 2) and before B5 (writes 1), so it can never see 0 or 1. It returns 2 if no A write lands between B3 and B4. It returns 3 if A3 is the latest write, and 4 if A4 is the latest write. So B4 is 2, 3, or 4.

**Q3 (final z):** The last write overall is either B5 (value 1) or A5 (value 2). Both orders are possible.

**Feasibility:**
- If A1 returns 0, 3, or 2, A1 can sit before B4 with Thread A's writes after it. Then B4 can be 2, 3, or 4, and either B5 or A5 can be last. A1 = 3 needs A1 between B1 and B3. A1 = 2 needs A1 between B3 and B5. For example, with B4 = 3 and final 2, the order is B3, A3, B4, B5, A5. This gives 6 combinations for each of these three values of A1.
- If A1 returns 1, B5 has already happened, so all of A3, A4, and A5 come after B5. B4 must then precede B5 and see B3's 2, so B4 = 2. The last write is A5, so the final value is 2. This gives only (1, 2, 2).

That makes 18 + 1 = 19 combinations.

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