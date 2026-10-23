All 12 combinations are possible. Because each operation takes effect at a single instant and each thread runs in order, every outcome comes from some interleaving of the threads' operations.

**Values that can appear**
- Only A1 and B4 write x. A1 writes 2, and B4 writes whatever B2 read from y. B1 runs before B4, so it reads 0 (before A1) or 2 (after A1), and the final x is 0 or 2.
- Every write to y carries a value read from x or y (B3 writes B1's value, C3 and C4 write C2's value). These are always 0 or 2, so y never holds anything else.
- z is written by C1 (value 3) and by A4 (value 0 or 2). The final z is 3 if C1 comes after A4, and otherwise A4's value.

**Case B1 = 0** (B1 runs before A1)
- **Final x:** it is 2 if A1 is last, or if B4 writes 2. It is 0 if B2 reads 0 and B4 runs after A1.
- **Final z = 0 or 3:** easy to arrange by ordering A4 and C1 and having A3 read 0.
- **Final z = 2:** use the order B1, A1, B2 (reads 0), C1, C2 (reads 2), C3 (y=2), A2, A3 (reads 2), A4 (z=2), B3, B4 (x=0). This gives x=0 and z=2. Reaching x=2 with z=2 is also easy.
- All six (x, z) pairs are reachable.

**Case B1 = 2** (A1 runs before B1)
- **Final x:** A1 precedes B4, so the final x is whatever B2 read. B2 reads 0 if no write to y has happened yet. It reads 2 if C3 wrote 2 first.
- **Final z:**
  - z = 0 needs A2 and A3 to read before any write to y, with A4 after C1.
  - z = 2 needs A3 to read 2 from y, written by C3 or B3.
  - z = 3 needs C1 after A4.
- All six (x, z) pairs are reachable.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END