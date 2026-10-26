I checked each case by hand. Every x-value is 0 or 2, and the only possible final z values are 1 and 5. Five combinations are feasible:

- **(B2=0, C3=0, z=1):** A1, B1, B2, C1, C2, C3, A2, A3, A4, B3, B4, A5, C4, C5
- **(B2=0, C3=0, z=5):** A1, C1, C2, C3, A2, A3, A4, C4, C5, B1, B2, B3, B4, A5
- **(B2=0, C3=2, z=1):** A1, B1, B2, A2, A3, C1, C2, C3, B3, B4, A4, A5, C4, C5. Final z=5 is impossible here because B1 must precede A3.
- **(B2=2, C3=0, z=1):** A1, B1, C1, C2, C3, A2, A3, B2, B3, B4, C4, C5, A4, A5
- **(B2=2, C3=0, z=5):** A1, C1, C2, C3, A2, A3, A4, B1, B2, B3, B4, C4, C5, A5

The case (B2=2, C3=2) is impossible. Every x-write would then be 2, so A5 would read 2, not 0.

BEGIN
0 0 1
0 0 5
0 2 1
2 0 1
2 0 5
END