The possible outcomes are below. Q4 always equals Q1, and Q3 always equals the value read by A4.

**Key facts:**
- B9 reads z after every other write to z, and B8 is the last write to z, so Q1 = Q4 = the value read by B2.
- A4 reads z after both A1 and B1, so it returns 6 if A1 is after B1 and 1 if A1 is before B1. Call this value a. A6, A7, A8 and A9 all carry a, so Q3 = a.
- B2 reads y, which only A8 writes, so B2 returns a if A8 is before B2 and 0 otherwise.
- The final x is either 1 (A2 after B7) or 4 (B7 last).
- If A2 is after B7, then B2 precedes B7, which precedes A2, which precedes A8. So B2 must come before A8 and returns 0. The combination with B2 returning a and final x = 1 is therefore impossible.

Each remaining combination has a schedule that satisfies all sync constraints. For example, a = 6 with B2 returning 6 and final x = 4 is achieved by B1, A1, A2 through A8, B2, A9, then the rest of B.

**Outcomes (Q1 Q2 Q3 Q4):**
- B2 returns 0, final x = 1, a = 1: `0 1 1 0`
- B2 returns 0, final x = 4, a = 1: `0 4 1 0`
- B2 returns 1, final x = 4, a = 1: `1 4 1 1`
- B2 returns 0, final x = 1, a = 6: `0 1 6 0`
- B2 returns 0, final x = 4, a = 6: `0 4 6 0`
- B2 returns 6, final x = 4, a = 6: `6 4 6 6`

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END