The possible outcomes are the four combinations below, with Q1 = 2 and Q3 = 2 in every execution.

**Key facts**
- **B1 and B2 read 2.** B1 is the only read that can see a y-write of 2 before it, and the only such write is C1 (B4 comes after B1 in program order). So C1 precedes B1, and no other y-write can intervene before B2.
- **B3 writes 2 to z.** B5 must read 2, and the only z-write that can be 2 is B3. So B3 precedes B5, and neither A1 nor A4 can fall between B3 and B5.
- **Final y is always 2.** Both y-writes (C1 and B4) write 2.
- **C2 reads z = 3.** So A1 precedes C2, and neither B3 nor A4 can fall between A1 and C2.
- **C4 reads 2 or 5.** C3 (writes 5) always precedes C4. A3 (writes 2) lands between C3 and C4 or not.
- **Final z is 2 or 4.** Three orderings of A1, A4 and B3 satisfy the constraints above:
  - A1 < C2 < A4 < B3 < B5 gives final z = 2.
  - A1 < C2 < B3 < B5 < A4 gives final z = 4.
  - B3 < B5 < A1 < C2 < A4 gives final z = 4.

In each ordering, C4 can read either 2 or 5 by placing A3 before C3 or between C3 and C4. Concrete schedules exist for every combination, for example:
- (2,2,2,2): A1, C1, A2, C2, C3, A3, C4, A4, B1, B2, B3, B4, B5
- (2,5,2,2): A1, C1, A2, C2, C3, C4, A3, A4, B1, B2, B3, B4, B5
- (2,2,2,4): A1, C1, A2, C2, B1, B2, B3, B4, B5, C3, A3, C4, A4
- (2,5,2,4): A1, C1, A2, C2, B1, B2, B3, B4, B5, A3, C3, C4, A4

Values are in the order Q1 Q2 Q3 Q4.

BEGIN
2 2 2 2
2 5 2 2
2 2 2 4
2 5 2 4
END