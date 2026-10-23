Two values are possible for B4: 0 and 4.

- **z is 0 until C5.** B5 reads z as 0, and C5 is the only write to z (of 3), so B1 and B5 both take effect before C5. Hence B1 reads 0 and B3 writes 0 to x.
- **y can only be 0, 3, or 4.** The writes to y are A1 (4), A4 (the value A3 read, 0 or 3), and C4 (4).
- **B4 cannot read 3.** A write of 3 to y needs A3 to read 3, which requires A3 after C5, and so after B4.
- **B4 can read 4.** Order: B1, A1, B2, C1, C2, A2, B3, C3, B4, A3, A4, B5, C4, C5. A1 is the last write to y when B4 runs.
- **B4 can read 0.** Order: B1, A1, B2, C1, C2, A2, B3, C3, A3, A4, B4, B5, C4, C5. A3 reads 0 and A4 writes 0 to y just before B4. The earlier reads still hold: B2 sees 4 from A1, C3 sees 4 from A1, and A2 sees 3 from C2.

BEGIN
0
4
END