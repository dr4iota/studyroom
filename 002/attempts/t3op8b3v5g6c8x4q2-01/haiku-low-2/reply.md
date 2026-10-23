The possible combinations are **(Q1, Q2) = (1, 4)** and **(5, 4)**.

**Why B3 must read 4:** B7 reads 4 and comes after B5. The only 4-write that can follow B5 is A4, but A4 must precede B2, which precedes B3, which precedes B5. So the value B3 reads must itself be 4.

**Why C6 must read 4:** C3 reads 5 and C4 later reads 4, so a 4-write must land between them. C6 comes after C4, and no 5-write can be the last y-write before C6 after that 4-write, so C6 reads 4.

**Why Q1 is 1 or 5:** A3 comes after A1 and before A4. If C1 (the only other write of 5) lands before A3, A3 reads 5. Otherwise A3 reads 1. The ordering C1 < C3 < A4 allows either. In the other scheduling cases (C1 after B3), C1 must land before A3 or not at all in that window, so A3 reads 1.

**Why final z = 1 is achievable:** B1 writes 1 to z and can be placed last among the z-writes, since it only has to precede B2.

**Concrete witness for (5, 4):** A1 (y=1), C1 (y=5), A2 (x=4), A3 (reads 5), C2 (z=4), C3 (reads 5), A4 (y=4), C4 (reads 4), A5 (z=3), A6 (reads 4), C5 (x=4), C6 (reads 4), C7 (x=4), C8 (z=4), A7 (z=5), B1 (z=1), B2 through B7 (all read 4 or 4-compatible values, B6 reads x=4). Final z = 1.

BEGIN
1 4
5 4
END