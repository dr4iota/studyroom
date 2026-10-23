**Answer: C4 can return 0, 1, 2 or 3. The final y is always 3, and the final z always equals C4's value.**

**Ordering forced by the known reads**
- **B1 returned 0 from x.** So B1 takes effect before A1, the first write to x.
- **A3 returned 3 from y.** B2 is the only write to y, so B2 takes effect before A3.
- **C2 returned 3 from z.** C1 comes before C2 in thread C. The last write to z before C2 must be B3, so C1 < B3 < C2.

**Q2: final y.** The only write to y is B2 (value 3), and it must happen. So y ends as 3.

**Q3: final z.** C3 comes after C2, and C2 comes after B3. So C3 and C5 are both after C1 and B3. C5 is the last write to z, so the final z equals the value C4 returned.

**Q1: value returned by C4.** The writes to x are A1 (2), B5 (1) and A4. A2 may read y before or after B2, so A4 writes either 0 or 3. Each candidate value is reachable:
- **0:** C4 takes effect before A1. This is possible because only B1 must precede A1, and C4 only needs to follow B3.
- **2:** C4 takes effect after A1 and before A4 and B5.
- **1:** C4 takes effect right after B5, which follows A1 and A4.
- **3:** A2 takes effect after B2 and reads 3. Then B5 takes effect, then A4 writes 3, then C4 reads it.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END