Every pair (B2, B3) below can occur with A1 returning either 0 or 4.

**Constraints**
- Each thread's operations take effect in the listed order: A1 < A2 < A3 < A4 < A5 and B1 < B2 < B3 < B4 < B5.
- A3 returns 4, and only B1 writes 4 to y, so B1 takes effect before A3.
- A1 reads y before A3. It returns 0 if it takes effect before B1, and 4 if it takes effect after B1. Both are possible, since A1 < A2 < A3 and B1 < A3 leave their relative order open.

**Values B2 and B3 can read from z**
- B5 (write 1 to z) comes after both B2 and B3, so neither read can return 1.
- z is 0 before A2 takes effect, 3 between A2 and A4, and 4 after A4.
- B2 takes effect before B3, so the stage of B3's read is at least the stage of B2's read.
- This gives the pairs (0,0), (0,3), (0,4), (3,3), (3,4) and (4,4).

**Combining with A1**
- B1 only has to precede A3, and B2 and B3 only have to follow B1.
- Each of the six (B2, B3) pairs can therefore be scheduled with A1 = 0, where A1 comes before B1.
- Each can also be scheduled with A1 = 4, where B1 comes before A1.
- Example for A1 = 4 with (0,0): B1, A1, B2, B3, A2, ...
- Example for A1 = 0 with (4,4): A1, B1, A2, A3, A4, B2, B3.

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END