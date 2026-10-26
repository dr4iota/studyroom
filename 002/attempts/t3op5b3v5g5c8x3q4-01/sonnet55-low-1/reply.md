Every possible combination has final y = 3 and Q3 equal to Q1; the reasoning follows.

**Constraints from the known reads**
- Only A1, A4 and B5 write x. B1 reads 0, so B1 takes effect before A1.
- Only B2 writes y, and it writes 3. A3 returns 3, so B2 takes effect before A3. Nothing else ever writes y, so the final y is always 3.
- A2 reads y and returns either 0 (before B2) or 3 (after B2).
- C2 returns 3, and only B3 writes 3 to z. So the order of z writes is C1 < B3 < C2 < C3, with no other z write between B3 and C2.
- C5 is the last write to z, and it writes the value C4 read. So the final z always equals Q1.

**Possible values of C4**
- **0:** C4 can take effect before A1, since A1 only needs to come after B1. Alternatively, A2 reads 0, A4 writes 0, and no later x write intervenes.
- **2:** A1 takes effect, then C4 reads, before A4 and B5.
- **1:** B5 takes effect after A1 and is the last x write before C4, with A4 after C4.
- **3:** A2 reads 3 (after B2), then A4 writes 3 as the last x write before C4, with B5 either earlier or after C4.

All four values are achievable.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END