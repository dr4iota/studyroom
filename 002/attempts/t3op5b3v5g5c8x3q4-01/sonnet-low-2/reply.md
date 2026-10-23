Every execution gives a final y of 3, and the final z always equals the value C4 returned. C4 itself can return 0, 1, 2 or 3.

**Constraints from the known results**
- B1 returned 0, so A1 (the only write of 2 to x) takes effect after B1.
- B2 is the only write to y, and it writes 3. A3 returned 3, so B2 takes effect before A3. A2 therefore reads either 0 or 3, and A4 writes that value to x.
- C2 returned 3, so the last write to z before C2 is B3. This means C1 < B3 < C2.
- C3 comes after C2, and C5 comes after C4, so C5 is the last write to z. The final z is therefore whatever C4 read.
- The only write to y is B2's 3, so the final y is 3.

**Values C4 can read from x** (the writes to x are A1 = 2, A4 = 0 or 3, and B5 = 1)
- **0:** C4 runs before A1, which is allowed because A1 only has to come after B1.
- **2:** A1 happens, and C4 reads before A4 and B5.
- **1:** B5 is the last write to x before C4. This is possible, for example with A4 after C4.
- **3:** A2 reads 3, A4 writes 3 and is the last write before C4, and B5 comes after C4.

Each value has a consistent ordering. Because the final z equals Q1, Q3 is the same as Q1.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END