Every combination of values from {0, 1, 3} turns out to be possible, so there are 27 outcomes. I checked this by reasoning through interleavings, not by exhaustive search, so the claim that all 27 are reachable rests on those constructions.

Only the values 0, 1 and 3 can ever appear in x or y, because every write either stores a constant (1 or 3) or copies a value that was read from a block. Since there are no sync points, any interleaving of the four threads' operations is allowed.

- **y = 1** is easy: C1 or D2 is the last write to y.
- **y = 3** needs B2 to read 3, so D1 must land after B1, and B3 must be the last write to y.
- **y = 0** needs B3 to write 0 after C1 and D2. B2 must read 0 even though B1 wrote 1, so something must reset x to 0 in between. A2 or A4 can do this if A1 read 0, or C3 can if C2 read 0.
  - Example giving A3 = 0 with C2 = 3: A1(0), D1(3), C2(3), C3 writes 3, D2, C1, B1, A2 writes 0, A3 reads 0, B2 reads 0, B3 writes 0.
  - A3 = 1 works as: A2 writes 0, B1, A3 reads 1, A4 writes 0, B2 reads 0.
  - A3 = 3 works as: A1(0), A2(0), D1, A3 reads 3, B1, A4 writes 0, B2 reads 0.
- Different A3 and C2 values can be combined with each y by placing C2 and A3 earlier or later around the resets. For example, y = 3 with A3 = 0 and C2 = 1 works as: A1(0), B1, C2(1), C3 writes 1, A2(0), A3(0), D1(3), B2(3), B3.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 3 0
0 3 1
0 3 3
1 0 0
1 0 1
1 0 3
1 1 0
1 1 1
1 1 3
1 3 0
1 3 1
1 3 3
3 0 0
3 0 1
3 0 3
3 1 0
3 1 1
3 1 3
3 3 0
3 3 1
3 3 3
END