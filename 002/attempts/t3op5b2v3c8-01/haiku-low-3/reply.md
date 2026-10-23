All 27 combinations of (Q1, Q2, Q3) with values in {0, 2, 3} are possible.

**Why the values are limited to {0, 2, 3}:** The only constants written are 3 (B1, B2) and 2 (B3). Every other write copies a value that some read returned, so no other value can appear.

**Why every combination is reachable:**
- **Q1 = 0:** A1 runs before any write.
- **Q1 = 3:** A1 runs between B2 and B3.
- **Q1 = 2:** A1 runs after B3, with C4 kept at the end so y stays 2.
- **Q2, Q3:** Both reads can run after B3, and each of the nine (Q2, Q3) pairs has a construction:
  - (0,0): C1 reads 0 before B1, and C2 writes 0 after B1.
  - (0,2): as (0,0), then B5 writes 2 (B4 reads y = 2) before Q3.
  - (0,3): C2 writes 0 early, then C3 reads 3 and C4 writes 3 to y after B3, so B4 reads 3 and B5 writes 3 to x before Q3.
  - (2,0): B5 writes 2, then C2 writes 0 (C1 read 0 before B1).
  - (2,2): B5 writes 2 and it stays.
  - (2,3): C1 reads 3 between B1 and B5, then C2 writes 3 after B5.
  - (3,0): x is 3 after B1, then C2 writes 0.
  - (3,2): x is 3 after B1, then B5 writes 2.
  - (3,3): x is 3 after B1 and before B5.

Each construction also works with Q1 placed at the required time before Q2.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END