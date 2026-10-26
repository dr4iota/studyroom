**Analysis**

- **A4 (read z):** B1 takes effect before P, and A4 is after P; A1 precedes A4 in thread order. No other writes to z can intervene (A6 is after A4, B8 is after R which is after A9). So A4 reads whichever of A1/B1 was last: A4 ∈ {1, 6}.
- **A7 = A4:** the only z-write between A4 and A7 is A6 (which writes A4's value). So A8 writes A4's value to y, and y is written by nobody else → **final y = A4 ∈ {1, 6}**.
- **B2 (read y):** B2 is before Q, A9 is after Q, so B2 precedes A9. But A8 is unordered with respect to B2, so B2 is either 0 (before A8) or A4 (after A8).
- **B8/B9:** B8 is after R, which is after all of A's writes (including A9), so B8 is the last z-write; B9 reads it. **B9 = final z = B2 ∈ {0, A4}**.
- **Final x:** A2 precedes A9 < R < B7, so B7 (writes 4) is the last x-write. **Final x = 4**.

Combining: (A4=1, B2∈{0,1}) and (A4=6, B2∈{0,6}).

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
END