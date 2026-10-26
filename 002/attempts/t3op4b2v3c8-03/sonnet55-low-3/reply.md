All twelve combinations of (A3, B4, final x) are possible. No sync points constrain the threads, so every interleaving of their operations is allowed.

**Possible values.** Every value written to y is a copy of 0 or 3, so A3 and B4 can only be 0 or 3. The final x is whichever of B1 (writes 1) and C3 (writes the value C1 read, 0 or 3) takes effect last, so it is 1, 0 or 3.

**Witnesses.** Each witness is an order of operations that produces the combination. A "(v)" after a read is the value it returns.

- **x = 1** (B1 takes effect after C3):
  - (3, 3, 1): all of C, then all of A, then all of B.
  - (0, 0, 1): C1(0), A1, C2, C3, C4 (y=0), A2, A3(0), then all of B.
  - (0, 3, 1): C1(0), C2, C3, B1, B2(0), B3 (y=0), A1, B4(3), C4 (y=0), A2, A3(0).
  - (3, 0, 1): B2(0), B3 (y=0), B4(0), then A1, A3(3), with C3 before B1.
- **x = 0** (C3 takes effect last and C1 read 0):
  - (3, 3, 0): C1(0), all of A and B, then C2, C3, C4.
  - (0, 0, 0): C1(0), B1, B2(0), B3, B4(0), A1, C2, C3, C4 (y=0), A2, A3(0).
  - (0, 3, 0): C1(0), B1, B2(0), B3 (y=0), A1, B4(3), C2, C3, C4 (y=0), A3(0).
  - (3, 0, 0): C1(0), B1, B2(0), B3, B4(0), A1, A3(3), then C2, C3, C4.
- **x = 3** (C3 takes effect last and C1 read 3):
  - (3, 3, 3): A1, C1(3), all of B, then C3.
  - (0, 0, 3): B1, B2(0), A1, C1(3), C2, C3 (x=3), B3 (y=0), B4(0), A3(0), C4.
  - (0, 3, 3): B1, B2(0), A1, C1(3), B3 (y=0), A2, A3(0), C2, C3 (x=3), C4 (y=3), B4(3).
  - (3, 0, 3): B1, B2(0), A1, C1(3), C2, C3 (x=3), B3 (y=0), B4(0), C4 (y=3), A3(3).

BEGIN
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 0 0
3 0 1
3 0 3
3 3 0
3 3 1
3 3 3
END