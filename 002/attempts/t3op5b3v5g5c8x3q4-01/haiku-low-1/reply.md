Every possible outcome has final y = 3 and final z equal to the value C4 read, so the combinations are (C4, y, z) = (0, 3, 0), (1, 3, 1), (2, 3, 2), and (3, 3, 3).

**Key constraints**

- **y:** B2 is the only write to y. A3 returns 3, so B2 takes effect before A3, and y's final value is always 3.
- **z:** C2 returns 3, so B3 is the last write to z before C2, which forces C1 < B3 < C2 < C3 < C4 < C5. C5 is therefore the last write to z, so the final z equals the value C4 read.
- **x:** C4 reads whichever write to x was last before it. The possible writes are A1 (2), A4 (the value A2 read, 0 or 3), and B5 (1).

**Achievability of each C4 value**

- **0:** C4 runs before A1, A4 and B5. Order: B1, B2, C1, B3, C2, C3, C4, C5, then A1, A2, A3, A4, B4, B5.
- **1:** Order: B1, A1, A2, B2, A3, A4 (writes 0, since A2 read 0), C1, B3, C2, C3, B4, B5, C4, C5. C4 reads 1 from B5.
- **2:** Order: B1, B2, C1, B3, C2, A1, A2, A3, C3, C4, A4, B4, B5, C5. C4 reads 2 from A1.
- **3:** Order: B1, B2, C1, B3, C2, A1, A2, A3, A4, C3, C4, C5, B4, B5. C4 reads 3 from A4 (A2 read 3).

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END