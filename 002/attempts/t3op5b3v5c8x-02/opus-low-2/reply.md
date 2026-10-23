**Approach.** Blocks x and z never affect y, so only the writes to y and the reads of y matter.

**Writes to y:**
- A1 writes 4.
- C2 writes 1.
- B3 writes 5.
- B5 writes v, where v is the value B1 read.

**Constraints:**
- B1 runs before B3 and B5. So B1 can only see 0, 4 (from A1) or 1 (from C2). It can never see 5, so v ∈ {0, 4, 1}.
- B3 always comes before B5.
- C3 and C4 come after C2, and C4 comes after C3. So C3 and C4 read the values of writes at or after C2, in time order.
- The final value of y is whichever of A1, C2 or B5 takes effect last.

**Case B1 = 0** (B1 runs before both A1 and C2; B5 writes 0). There are 12 possible orders of the four writes, with 5 always before 0:
- If B5 is last, the final value is 0. Possible (C3, C4) pairs: 11, 15, 10, 55, 50, 00, 14, 44, 45, 40, 54.
- If C2 is last, both reads return 1. This gives 1 1 1.
- If A1 is last, the final value is 4. Possible pairs: 11, 15, 10, 14, 55, 50, 54, 00, 04, 44.

**Case B1 = 4** (A1 is the last write before B1; B5 writes 4). Write orders:
- 1 4 5 4 gives pairs 11, 14, 15, 44, 45, 55, 54, with final 4.
- 4 1 5 4 and 4 5 1 4 give pairs that are already covered, with final 4.
- 4 5 4 1 gives 1 1 1.

**Case B1 = 1** (C2 is the last write before B1, so A1 is either before C2 or after B1; B5 writes 1). Write orders:
- 4 1 5 1, 1 4 5 1 and 1 5 4 1 end in 1. Their pairs are 11, 15, 55, 51, 14, 44, 45, 41, 54.
- 1 5 1 4 ends in 4. Its pairs are 11, 15, 14, 55, 51, 54, 44.

BEGIN
0 0 0
1 0 0
1 1 0
1 4 0
1 5 0
4 0 0
4 4 0
4 5 0
5 0 0
5 4 0
5 5 0
1 1 1
1 4 1
1 5 1
4 1 1
4 4 1
4 5 1
5 1 1
5 4 1
5 5 1
0 0 4
0 4 4
1 0 4
1 1 4
1 4 4
1 5 4
4 4 4
4 5 4
5 0 4
5 1 4
5 4 4
5 5 4
END