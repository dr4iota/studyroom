Only the writes to y matter, since B1 and B2 don't touch y. Order constraints: A1 < A2 < A3 < A4 and B3 < B4 < B5.

**Q1, the value returned by A2.** A1 writes 3 before A2. Writes by B can land between A1 and A2.
- 3: neither B4 nor B5 lands between them.
- 1: B4 lands between them, but B5 does not.
- 2: B5 lands between them, which also requires B4 before it.

**Q2, the value returned by B3.** B4 and B5 come after B3, so only A's writes can precede it.
- 0: B3 comes before A1.
- 3: B3 comes after A1 and before A3, or after A4.
- 4: B3 comes after A3 and before A4. A2 must then be 3, because B4 and B5 come after B3 and so after A3.

**Q3, the final value of y.** It is the later of A4 (3) and B5 (2), so it is 3 or 2. The final value is 2 only if B5 comes after A4. That is impossible when A2 returned 2, because B5 is then before A2.

**Combinations:**
- B3 = 0: A2 can be 3, 1, or 2. For A2 = 3 or 1, the final value can be 3 or 2. For A2 = 2, the final value is 3 only.
- B3 = 3: the same pattern as B3 = 0.
- B3 = 4: A2 = 3, and the final value is 3 or 2.

BEGIN
3 0 3
3 0 2
1 0 3
1 0 2
2 0 3
3 3 3
3 3 2
1 3 3
1 3 2
2 3 3
3 4 3
3 4 2
END