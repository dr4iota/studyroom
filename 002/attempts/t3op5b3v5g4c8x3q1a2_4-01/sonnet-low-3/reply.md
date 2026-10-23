B4 can return 0 or 4.

**What B5 forces.** B5 reads z as 0, and the only write to z is C5 (value 3). So C5 takes effect after B5. B1 and B4 both precede B5, so C5 also comes after B1 and B4. Hence B1 reads 0, and B3 writes 0 to x.

**Which writes to y can B4 see.** The writes to y are A1 (4), C4 (4) and A4 (the value A3 read).
- A3 reads z as either 0 or 3. A3 can read 3 only if C5 precedes A3, so A4 would then follow C5. C5 is after B4, so that A4 cannot affect B4. Any A4 that precedes B4 therefore writes 0.
- B2 read y as 4, so y was 4 at that moment (from A1 or C4, with C3 also reading 4).

**B4 = 4 is possible.** Order: A1, C1, C2, A2 (reads 3), C3 (reads 4), B1 (reads 0), B2 (reads 4), B4 (reads 4), B3, B5 (reads 0), and the rest afterward. Nothing overwrites y with 0 before B4.

**B4 = 0 is possible.** Order: A1, C1, C2, A2 (reads 3), C3 (reads 4), B1 (reads 0), B2 (reads 4), A3 (reads 0), A4 (writes 0 to y), B4 (reads 0), B3, B5 (reads 0). C4 and C5 then run afterward. This agrees with every known result.

**B4 = 3 is impossible.** The only source of a 3 in y would be A4 writing a 3 read from z, and that would have to happen after B4.

BEGIN
0
4
END