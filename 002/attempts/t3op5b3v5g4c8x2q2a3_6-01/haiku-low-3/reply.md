Q1 is always 0 and Q2 can be 0, 1, or 5.

**Q1 (C3 reads z):** Only B5 writes z, and it writes B4's value v. C4 reads z and must return 0 (known). If B5 precedes C4, then z = v at C4, so v = 0 and C3 also reads 0. If B5 comes after C4, then C3 (which precedes C4) also reads 0. So C3 always returns 0.

**Q2 (final z):** B5 is the last write to z, so the final z equals v, the value B4 read from y. The values written to y are 2 (B1), 1 (B3), 1 (C1), and the value A1 read from x (A4). A1 reads either 0 or 5, since x is only written by B2 with value 5. Because B3 always precedes B4 and writes 1, the value 2 can never be the last write before B4, so v ∈ {0, 1, 5}. Each remaining value has a schedule:

- **v = 1:** A1, A2, B1, B2, A3, B3, B4, C1, C2, C3, C4, B5, A4, A5. B4 reads 1 from B3.
- **v = 5:** B1, B2, A1, A2, A3, B3, C1, A4, B4, C2, C3, C4, B5, A5. A1 reads 5, A4 writes 5, and B4 reads it.
- **v = 0:** A1, B1, B2, A2, A3, B3, A4, B4, C1, C2, C3, C4, B5, A5. A1 reads 0, A4 writes 0, and B4 reads it.

BEGIN
0 0
0 1
0 5
END