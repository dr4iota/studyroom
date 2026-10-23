Every operation is a single instant, and no sync points constrain the order, so any interleaving of the three threads' lists is allowed. I worked out which triples (A1, B4, C4) can occur by case on A1.

**A1 can be 0, 1 or 2.** A1 reads x, and only B2 (1) and C1 (2) can write x before it, since A5 comes after A1.

**What B4 and C4 can read.** B3 and C3 both write 1 to y, and each is followed by its own thread's read. Neither read can see 0 unless A3 writes 0 to y after those writes. The value 2 can reach y after C3 only through A3 (when A1 = 2), or through B5 or C5 copying a 2 that was already read. Otherwise 2 appears only in the window between C2 and C3. A4 and B1 supply the value 3.

**Case A1 = 0.** A3 writes 0 to y, so 0 is possible for both reads.
- B4 can be 0, 1, 2 or 3.
- C4 can be 0, 1 or 3 for any B4.
- C4 = 2 needs a source of 2 after C3. Only B5 copying B4 = 2 supplies one, so C4 = 2 requires B4 = 2.
- This gives 12 combinations plus (2, 2), which is 13 in total.

**Case A1 = 1.** A3 writes 1, so y is never 0 and both reads are in {1, 2, 3}. C4 = 2 again requires B4 = 2.
- B4 = 1 allows C4 = 1 or 3.
- B4 = 2 allows C4 = 1, 2 or 3.
- B4 = 3 allows C4 = 1 or 3.

**Case A1 = 2.** A3 writes 2 after C1, which provides a source of 2 after C3, so every pairing of {1, 2, 3} with {1, 2, 3} is possible. For example, (3, 2) works with the order A3(2), C4(2), A4(3), B4(3).

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 3
1 1 1
1 1 3
1 2 1
1 2 2
1 2 3
1 3 1
1 3 3
2 1 1
2 1 2
2 1 3
2 2 1
2 2 2
2 2 3
2 3 1
2 3 2
2 3 3
END