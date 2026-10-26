**Analysis**

- **z and A4:** B1 (write 1) must precede P, and A4 reads after P; A1 (write 6) precedes A4 in program order. So A4 reads the later of A1/B1: A4 ∈ {1, 6}.
- **A7/A8/A9:** A7 reads after A6 with no other z-writer able to intervene (B8 is after R, after A9), so A7 = A4. Hence A8 writes A4 to y and A9 writes A4 to z.
- **Final y:** A8 is the only write to y → final y = A4.
- **B2:** reads y before Q; A8 may land before or after B2 (A8 isn't forced after Q). So B2 ∈ {0, A4}.
- **B8/B9/final z:** B8 (after R) comes after every A write to z, so B9 = B2 and final z = B2.
- **Final x:** last write is either A2 (1) or B7 (4). A2 has no sync constraint and can occur before or after B7, so final x ∈ {1, 4}, independently of the other choices.

BEGIN
0 1 1 0
0 4 1 0
1 1 1 1
1 4 1 1
0 1 6 0
0 4 6 0
6 1 6 6
6 4 6 6
END