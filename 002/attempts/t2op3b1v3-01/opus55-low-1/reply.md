Since x is a single block and every operation takes effect at one instant, each execution is one total order of the six operations. B's operations stay in the order B1, B2, B3, and A's stay in the order A1, A2, A3.

**Q3 (B1).** B1 comes before both of B's writes, so the only write that can precede it is A1.
- If A1 takes effect before B1, then B1 returns 1.
- If A1 takes effect after B1, then B1 returns 0.

**Q1 and Q2 (A2, A3).** A2 and A3 both come after A1, so neither can return 0. Each returns the latest of the writes A1 (1), B2 (3) and B3 (2) that took effect before it. A3 comes after A2, so A3 sees the same write as A2 or a later one. The write order depends on where A1 falls relative to B2 and B3:

| Where A1 takes effect | Write order | Possible (A2, A3) |
|---|---|---|
| Before B2 | 1, 3, 2 | (1,1), (1,3), (1,2), (3,3), (3,2), (2,2) |
| Between B2 and B3 | 3, 1, 2 | (1,1), (1,2), (2,2) |
| After B3 | 2, 1 | (1,1) |

In the last two rows A1 comes after B1, so B1 = 0 there. Those rows add no new pairs, because the first row already contains all of them.

**Combining.** The first row allows A1 either before B1 (so B1 = 1) or between B1 and B2 (so B1 = 0). In both cases A2 and A3 can still land anywhere among the writes. So all six (A2, A3) pairs occur with B1 = 0 and with B1 = 1. That gives 12 combinations.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END