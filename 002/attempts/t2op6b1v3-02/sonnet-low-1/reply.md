Sync points aren't used here, so every operation takes effect at its own instant. The possible executions are therefore all interleavings of the two threads' operation orders. The writes are A3=2, A4=3, A5=2 in that order, and B3=1, B5=1 in that order.

**Q1 (B1):** B1 comes before both of B's writes, so it can't return 1. It returns 0, 2 or 3, depending on how many of A's writes have happened.

**Q2 (B4):** B4 comes after B3 and before B5. It returns 1 if no A write lands between B3 and B4. Otherwise it returns the last A write in that window, which is 2 or 3.

**Q3 (final x):** The last write overall is either A5 (2) or B5 (1), and both are possible.

**Combinations by B1:**
- **B1=0:** None of A's writes have happened yet, so B4 and the final value are unconstrained. All six pairs (B4 in {1,2,3}, final in {1,2}) are possible.
- **B1=2:** A3 is done and A4 is not, so only A4 and A5 remain.
  - B4=1 works with final 1 or 2.
  - B4=2 needs A5 between B3 and B4, so B5 comes after A5 and the final value must be 1.
  - B4=3 works with final 1 or 2.
- **B1=3:** A4 is done, so only A5 remains.
  - B4=1 works with final 1 or 2.
  - B4=2 needs A5 before B4, so the final value must be 1.
  - B4=3 is impossible, because A4 is already used.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END