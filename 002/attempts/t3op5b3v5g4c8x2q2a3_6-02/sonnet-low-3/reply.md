Q1 can be 0, 1 or 3. Q2 is 3 or 4 except when Q1 is 3, where it is always 4.

**Fixed facts**
- Only B1 writes x, so x is 0 before B1 and 3 after it.
- C1 returned 0 and C2 returned 3, so C1 < B1 < C2 in effect order.
- A3 returned 3, so B1 < A3. B3 comes after B1, so B3 reads 3, and B4 writes 3 to y.
- C5 comes after C3, which comes after B1.
- y is written only by B4 (value 3) and C5 (value 4). The final y is whichever of the two takes effect last.
- A2 can read 0, 3 or 4 from y. A4 then writes that value to z.

**Q1: the value C3 returns from z**
- **0:** C3 takes effect before A1 and B2, which is allowed. The same value also comes from A4 writing 0.
- **1:** A1 or B2 takes effect before C3.
- **3:** A2 reads 3 from B4, and A4 writes 3 to z before C3. The order B1, B3, B4, A2, A3, A4, C3 works.
- **4 is impossible:** A2 would have to read 4, so C5 comes before A2. But C5 comes after C3, and A4 comes after A2, so A4 cannot take effect before C3.

**Q2: the final value of y**
- **3:** B4 takes effect after C5.
- **4:** C5 takes effect after B4.
- With Q1 = 0 or 1, both orders are possible.
- With Q1 = 3, B4 must come before A2, which comes before C3, which comes before C5. So B4 precedes C5 and the final y is 4 only.

BEGIN
0 3
0 4
1 3
1 4
3 4
END