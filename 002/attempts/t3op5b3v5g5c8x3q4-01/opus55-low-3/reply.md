Every possible combination of (C4, final y, final z) is listed at the end. Since there are no sync points, only the program order within each thread and the known read results limit the interleavings.

**Fixed orderings from the known results**
- B1 reads x = 0, so B1 takes effect before A1. Otherwise it would see A1's write of 2.
- A3 reads y = 3, so B2 takes effect before A3.
- C2 reads z = 3, so the last write to z before C2 is B3. With program order this gives C1 < B3 < C2.

**Final y (Q2)**
B2 is the only write to y. A3 already depends on B2 having happened, so the final y is always **3**.

**Final z (Q3)**
The writes to z are C1, B3, C3 and C5. They must occur in the order C1 < B3 < C2 < C3 < C5. So C5 is always the last write, and the final z equals the value read by C4.

**Value read by C4 (Q1)**
- **0:** C4 can take effect before A1 and B5. This works because A1 only has to follow B1, which comes earlier than B3 and C4. C4 also reads 0 if it follows A4 when A2 read 0, which happens if A2 ran before B2.
- **2:** C4 takes effect after A1 and before the other writes to x.
- **1:** C4 takes effect right after B5.
- **3:** A2 runs after B2, so A4 writes 3 to x, and C4 takes effect right after A4.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END