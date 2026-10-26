Each answer below follows from how x and y can be written and read in any interleaving.

**Writes to x.** Only B2 (writing r1, the value B1 read) and A4 (writing 3) write x. B2 always precedes B3 and B5, so x is never 0 when B3 or B5 reads it. The result depends on where A4 falls relative to B2, B3 and B5.

**Values of r1.** B1 reads y, which can be 0 (before A1), 2 (after A1, before A2) or 1 (after A2). Each of these can occur whether A4 falls before or after B2.

**Case 1: A4 before B2.**
- B2 overwrites A4's write, so B3 = B5 = r1.
- B4 writes r1.
- The final y is whichever of A5 and B4 comes last, so it is 1 (A5 last) or r1 (B4 last).
- This gives (0,0,0), (0,0,1), (2,2,2), (2,2,1) and (1,1,1).

**Case 2: A4 after B3.**
- B3 = r1, and B5 = 3, since A4 can come before B5.
- B4 writes r1.
- The final y is 1 or r1.
- This gives (0,3,0), (0,3,1), (2,3,2), (2,3,1) and (1,3,1).

**Case 3: A4 between B2 and B3.**
- B3 = 3 and B5 = 3.
- B4 writes 3.
- The final y is 1 (A5 last) or 3 (B4 last).
- This gives (3,3,1) and (3,3,3).

BEGIN
0 0 0
0 0 1
2 2 2
2 2 1
1 1 1
0 3 0
0 3 1
2 3 2
2 3 1
1 3 1
3 3 1
3 3 3
END