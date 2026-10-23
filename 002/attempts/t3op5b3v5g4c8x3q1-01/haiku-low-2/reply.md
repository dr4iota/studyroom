Only the program order within each thread constrains the interleaving, since there are no sync points. The known results prune the possibilities:

- **B1 and B5:** B5 reads z = 0, so C5 (the only write of z) must come after B5. Therefore B1 also reads 0, so B3 writes 0 to x.
- **B4 reading 3:** The only write of 3 to y is A4, and it writes the value of A3. For A4 to write 3, A3 must come after C5, which is after B5, which is after B4. But A4 must come before B4 for B4 to read it. This is a contradiction, so B4 cannot read 3.
- **B4 reading 0:** Possible. Take the order A1, B1, B2, C1, C2, C3, A2, A3, A4, B3, B4, B5, C4, C5. A4 writes 0 to y, and B4 reads it. Every known result checks out: B2 reads 4 from A1, C3 reads 4 from A1, A2 reads 3 from C2, and B5 reads 0.
- **B4 reading 4:** Possible. Take the order A1, B1, B2, B3, B4, B5, C1, C2, C3, A2, A3, A4, C4, C5. B4 reads 4 from A1, and every other known result still holds.

So the possible values of B4 are 0 and 4.

BEGIN
0
4
END