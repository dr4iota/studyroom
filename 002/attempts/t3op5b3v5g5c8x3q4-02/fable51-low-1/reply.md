**Analysis**

- **Q1 (A2):** The only write to y is A3, which comes after A2 in thread A. So A2 always returns **0**.
- **Q3 (C3):** C3 reads y, which is 0 or 4 (depending on whether A3 took effect before it).
- **Q2 (A4):** A1 returned 3, so C1 took effect before A1 and A4 can see 3 (no later write), 4 (from B1 or C4 writing 4), or 0 (from C4 writing 0, which requires C3 = 0).

Checking each combination:
- (0, 3, 0): C1, C2, C3=0, A1=3, A2, A3, A4=3, C4, B1 — valid.
- (0, 4, 0): C1, C2, A1=3, B1, A2, A3, A4=4, C3=0, ... — valid.
- (0, 0, 0): C1, A1=3, C2=3, C3=0, C4 writes 0, A2, A3, A4=0 — valid.
- (0, 3, 4): C1, C2, A1, A2, A3, A4=3, C3=4, C4, B1 — valid.
- (0, 4, 4): C1, C2, A1, A2, A3, C3=4, C4 writes 4, A4=4 — valid.
- (0, 0, 4): impossible, since C4 would write 4, not 0, and no other write of 0 exists.

BEGIN
0 0 0
0 3 0
0 4 0
0 3 4
0 4 4
END