The outcomes are (Q1, Q2, Q3) = (value of A4, value of B5, final x). I checked each of the 12 combinations below against an explicit interleaving.

**Key facts:**
- No block ever holds 1 in x. The first 1 written to x would have to be copied from a read that already saw 1, which is impossible. So every read of x and every x-write carries 0 or 2.
- y holds 1 only after C2 writes it. B3 copies B2's read of x, so y is 0 or 2 after B3 unless C2 overwrites it.
- B1 precedes B2 in program order, so B2 can read 0 only if A5 writes 0 between B1 and B2.
- B5 comes after B3, so y is never 0 at B5 unless B3 wrote 0. Q2 = 1 requires C2 to fall between B3 and B5.

**Feasibility by Q2:**
- **Q2 = 0:** B2 reads 0, B3 writes 0 to y, and C2 comes after B5. Q1 can be 0 or 2 and Q3 can be 0 or 2. Examples: (0,0,0) with A1–A5 first and B4 last; (2,0,0) with A4 after B1 and B4 last after C1.
- **Q2 = 1:** C2 lies between B3 and B5. Each of the four (Q1, Q3) pairs has a schedule. Example: (2,1,0) is A1–A3, B1, A4, A5, B2, B3, C1, C2, B4, B5.
- **Q2 = 2:** B2 reads 2 and C2 comes after B5. Q3 = 0 comes from A5 being the last x-write, which is possible because A5 is not ordered against B2. Example: (0,2,0) is A1–A4, B1, B2, B3, B4, B5, A5, C1, C2.

BEGIN
0 0 0
0 0 2
2 0 0
2 0 2
0 1 0
0 1 2
2 1 0
2 1 2
0 2 0
0 2 2
2 2 0
2 2 2
END